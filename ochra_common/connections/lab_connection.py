from ..utils.singleton_meta import SingletonMeta
from ..base import DataModel
from .rest_adapter import RestAdapter, Result, LabEngineException
from .api_models import (
    ObjectConstructionRequest,
    ObjectQueryResponse,
    ObjectCallRequest,
    ObjectPropertySetRequest,
    ObjectPropertyGetRequest
)
from pydantic import ValidationError
from uuid import UUID
import logging
from typing import Any, Type, TypeVar, Union, List
import importlib

# TODO change the return types of get_property and get_all_objects to be more specific

class LabConnection(metaclass=SingletonMeta):
    """lab adapter built on top of RestAdapter,
    heavily coupled to lab engine api
    """

    def __init__(
        self,
        hostname: str = "127.0.0.1:8000",
        api_key: str = "",
        ssl_verify: bool = False,
        logger: logging.Logger = None,
    ):
        """constructor for labAdapter class

        Args:
            hostname (_type_, optional): address of lap api.
                Defaults to "127.0.0.1:8000".
            api_key (str, optional): api key if exists. Defaults to ''.
            ssl_verify (bool, optional): if we need to verify ssl.
                Defaults to False.
            logger (logging.Logger, optional): logger if you have one.
                Defaults to None.
        """
        self.rest_adapter: RestAdapter = RestAdapter(
            hostname, api_key, ssl_verify, logger
        )

    def _load_from_response(self, obj: ObjectQueryResponse):
        """load object from response

        Args:
            obj (ObjectQueryResponse): object information, id, cls, module_path

        Raises:
            LabEngineException: if there is an error in importing class

        Returns:
            Any: instance of the class
        """
        try:
            module = importlib.import_module(obj.module_path)
            class_to_instance = getattr(module, obj.cls)
            instance = class_to_instance.from_id(obj.id)
            return instance
        except Exception as e:
            raise LabEngineException(f"Unexpected error in importing class: {e}")

    def construct_object(self, type: str, object: Type[DataModel]) -> UUID:
        """construct object on the lab

        Args:
            type (str): type of the object to construct
            object (Type[DataModel]): object to be constructed

        Raises:
            LabEngineException: if there is an error in constructing object

        Returns:
            UUID: id of the constructed object
        """
        req = ObjectConstructionRequest(object_json=object.model_dump_json())
        result: Result = self.rest_adapter.put(
            f"/{type}/construct", data=req.model_dump(mode="json")
        )
        try:
            id = UUID(result.data)
            return id
        except ValueError:
            raise LabEngineException(f"Expected UUID, got {result.data}")
        except Exception as e:
            raise LabEngineException(f"Unexpected error: {e}")

    def get_object(
        self, type: str, identifier: Union[str, UUID]
    ) -> ObjectQueryResponse:
        """get object from lab

        Args:
            type (str): type of the object to get
            identifier (Union[str, UUID]): id or name of the object

        Raises:
            LabEngineException: if there is an error in getting object

        Returns:
            ObjectQueryResponse: object information, id, cls, module_path
        """
        result: Result = self.rest_adapter.get(
            f"/{type}/get", {"identifier": str(identifier)}
        )
        try:
            object = ObjectQueryResponse(**result.data)
            return self._load_from_response(object)
        except ValueError:
            raise LabEngineException(f"Expected ObjectQueryResponse, got {result.data}")
        except Exception as e:
            raise LabEngineException(f"Unexpected error: {e}")


    def get_all_objects(self, type: str) -> List[ObjectQueryResponse]:
        """returns a list of all objects of a certain type

        Args:
            type (str): the type of the object to get 

        Raises:
            LabEngineException: if there is an error in getting objects

        Returns:
            List[ObjectQueryResponse]: list of object information, (id, cls, module_path)
        """
        result: Result = self.rest_adapter.get(f"/{type}/get_all")
        try:
            objects = [ObjectQueryResponse(**data) for data in result.data]
            return [self._load_from_response(obj) for obj in objects]
        except ValueError:
            raise LabEngineException(f"Expected ObjectQueryResponse, got {result.data}")
        except Exception as e:
            raise LabEngineException(f"Unexpected error: {e}")

    def delete_object(self, type: str, id: UUID):
        """delete object from lab

        Args:
            type (str): type of the object
            id (UUID): id of the object

        Returns:
            Any: response from the lab
        """
        result: Result = self.rest_adapter.delete(f"/{type}/delete/{str(id)}")
        return result.data

    def call_on_object(
        self, type: str, id: UUID, method: str, args: dict
    ) -> ObjectQueryResponse:
        """make a request for the lab to run a function on an object

        Args:
            type (str): type of the object to call function on
            id (UUID): id of the object to run the function on
            method (str): name of the function to run
            args (dict): arguments to pass to the function

        Raises:
            LabEngineException: if there is an error in calling the function

        Returns:
            ObjectQueryResponse: object information, id, cls, module_path
        """
        req = ObjectCallRequest(method=method, args=args)
        result: Result = self.rest_adapter.post(
            f"/{type}/{str(id)}/call_method", data=req.model_dump(mode="json")
        )
        try:
            object = ObjectQueryResponse(**result.data)
            return self._load_from_response(object)
        except Exception as e:
            raise LabEngineException(f"Unexpected error: {e}")

    def get_property(
        self, type: str, id: UUID, property: str
    ) -> Union[Any, ObjectQueryResponse]:
        """get a property of an object on the lab

        Args:
            type (str): type of the object
            id (UUID): id of the object
            property (str): name of the property to get

        Raises:
            LabEngineException: if there is an error in getting the property

        Returns:
            Union[Any, ObjectQueryResponse]: value of the property
        """
        req = ObjectPropertyGetRequest(property=property)
        result: Result = self.rest_adapter.get(
            f"/{type}/{str(id)}/get_property",data = req.model_dump(mode="json")
        )
        if result.status_code == 404:
            raise LabEngineException(f"Property {property} not found for {type} {id}")
        try:
            if isinstance(result.data, list):
                listData = [
                    self._convert_to_object_query_response_possibly(data)
                    for data in result.data
                ]
                return [
                    self._load_from_response(data)
                    if isinstance(data, ObjectQueryResponse)
                    else data
                    for data in listData
                ]
            elif isinstance(result.data, dict):
                possibleQueryResponse = self._convert_to_object_query_response_possibly(
                    result.data
                )
                if isinstance(possibleQueryResponse, ObjectQueryResponse):
                    return self._load_from_response(possibleQueryResponse)
                else:
                    return possibleQueryResponse
            else:
                return result.data
        except Exception as e:
            raise LabEngineException(f"Unexpected error: {e}")

    def set_property(self, type: str, id: UUID, property: str, value: Any):
        """set a property of an object on the lab

        Args:
            type (str): type of the object to set property on
            id (UUID): id of the object
            property (str): name of the property to set
            value (Any): value to set the property to

        Returns:
            Any: response from the lab
        """
        req = ObjectPropertySetRequest(property=property, property_value=value)
        result: Result = self.rest_adapter.patch(
            f"/{type}/{str(id)}/modify_property", data=req.model_dump(mode="json")
        )
        return result.data

    def _convert_to_object_query_response_possibly(
        self, data: Any
    ) -> Union[ObjectQueryResponse, Any]:
        """convert data to ObjectQueryResponse if possible

        Args:
            data (Any): data to convert

        Returns:
            Union[ObjectQueryResponse, Any]: ObjectQueryResponse if possible, else data
        """
        try:
            return ObjectQueryResponse(**data)
        except (ValidationError, TypeError):
            return data

    def get_object_id(self, type: str, name: str) -> UUID:
        """get object id from lab given name

        Args:
            type (str): type of the object to get
            name (str): name of the object

        Raises:
            LabEngineException: if there is an error in getting the object id

        Returns:
            UUID: id of the object
        """
        result: Result = self.rest_adapter.get(f"/{type}/get", {"identifier": name})
        try:
            return UUID(result.data["id"])
        except ValueError:
            raise LabEngineException(f"Expected UUID, got {result.data}")
        except Exception as e:
            raise LabEngineException(f"Unexpected error: {e}")

    def put_data(self, type: str, id: str, result_data) -> UUID:
        """put data into a results data object

        Args:
            type (str): type of the object to put data into
            id (str): id of the object to put data into
            result_data (Any): data to put into the object

        Returns:
            UUID: id of the object
        """
        result: Result = self.rest_adapter.patch(
            f"/{type}/{str(id)}/put_data", files=result_data
        )
        return result.message

    def get_data(self, type: str, id: str) -> bytes:
        """get data from a results data object

        Args:
            type (str): type of the object to get data from
            id (str): id of the object to get data from

        Returns:
            bytes: raw bytes of the data
        """
        result: Result = self.rest_adapter.get(f"/{type}/{str(id)}/get_data", jsonify=False)
        return result.content
