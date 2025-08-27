from ..utils.singleton_meta import SingletonMeta
from ..base import DataModel
from .rest_adapter import RestAdapter, Result, LabEngineException
from .api_models import (
    ObjectConstructionRequest,
    ObjectCallRequest,
    ObjectPropertyPatchRequest,
    ObjectPropertyGetRequest,
)
from uuid import UUID, uuid4
import logging
from typing import Any, Type, TypeVar, Union, List
import importlib
from ..equipment.operation import Operation
from ..utils.enum import OperationStatus, PatchType
from ..utils.misc import is_data_model, convert_to_data_model
import time

# TODO change the return types of get_property and get_all_objects to be more specific

class LabConnection(metaclass=SingletonMeta):
    """lab adapter built on top of RestAdapter,
    heavily coupled to lab engine api
    """

    def __init__(
        self,
        hostname: str = "127.0.0.1:8000",
        experiment_id: str = None,
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
        if experiment_id is None:
            self._session_id = str(uuid4())
        else:
            self._session_id = experiment_id

    def load_from_data_model(self, model: DataModel) -> Any:
        """load object from data model
        Args:
            model (DataModel): data model to load
        Raises:
            LabEngineException: if there is an error in loading object
        Returns:
            Any: instance of the class
        """
        try:
            module = importlib.import_module(model.module_path)
            class_to_instance = getattr(module, model.cls)
            instance = class_to_instance.from_id(model.id)
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
            f"/{type}/", data=req.model_dump(mode="json")
        )
        try:
            id = UUID(result.data)
            return id
        except ValueError:
            raise LabEngineException(f"Expected UUID, got {result.data}")
        except Exception as e:
            raise LabEngineException(f"Unexpected error: {e}")

    def get_object(self, type: str, identifier: Union[str, UUID]) -> Any:
        """get object from lab

        Args:
            type (str): type of the object to get
            identifier (Union[str, UUID]): id or name of the object

        Raises:
            LabEngineException: if there is an error in getting object

        Returns:
            Any: instance of the class
        """
        result: Result = self.rest_adapter.get(
            f"/{type}/", {"identifier": str(identifier)}
        )
        try:
            base_model = convert_to_data_model(result.data)
            return self.load_from_data_model(base_model)
        except ValueError:
            raise LabEngineException(f"Expected ObjectQueryResponse, got {result.data}")
        except Exception as e:
            raise LabEngineException(f"Unexpected error: {e}")

    def get_all_objects(self, type: str) -> List[Any]:
        """returns a list of all objects of a certain type

        Args:
            type (str): the type of the object to get

        Raises:
            LabEngineException: if there is an error in getting objects

        Returns:
            List[Any]: list of instances of the class
        """
        result: Result = self.rest_adapter.get(f"/{type}/all")
        try:
            base_models = [
                convert_to_data_model(model_dict) for model_dict in result.data
            ]
            return [self.load_from_data_model(model) for model in base_models]
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
        result: Result = self.rest_adapter.delete(f"/{type}/{str(id)}/")
        return result.data

    def call_on_object(self, type: str, id: UUID, method: str, args: dict) -> Operation:
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
        req = ObjectCallRequest(method=method, args=args, caller_id=self._session_id)
        result: Result = self.rest_adapter.post(
            f"/{type}/{str(id)}/method", data=req.model_dump(mode="json")
        )
        try:
            base_model = convert_to_data_model(result.data)
            op: Operation = self.load_from_data_model(base_model)
            while op.status != OperationStatus.COMPLETED:
                time.sleep(5)
            return op
        except Exception as e:
            raise LabEngineException(f"Unexpected error: {e}")

    def get_property(self, type: str, id: UUID, property: str) -> Any:
        """get a property of an object on the lab

        Args:
            type (str): type of the object
            id (UUID): id of the object
            property (str): name of the property to get

        Raises:
            LabEngineException: if there is an error in getting the property

        Returns:
            Any: value of the property
        """
        req = ObjectPropertyGetRequest(property=property)
        result: Result = self.rest_adapter.get(
            f"/{type}/{str(id)}/property", data=req.model_dump(mode="json")
        )
        if result.status_code == 404:
            raise LabEngineException(f"Property {property} not found for {type} {id}")
        try:
            value = result.data
            if is_data_model(value):
                base_model = convert_to_data_model(value)
                return self.load_from_data_model(base_model)
            elif isinstance(value, list):
                return [
                    self.load_from_data_model(convert_to_data_model(item))
                    if is_data_model(item)
                    else item
                    for item in value
                ]
            elif isinstance(value, dict):
                return {
                    key: self.load_from_data_model(convert_to_data_model(val))
                    if is_data_model(val)
                    else val
                    for key, val in value.items()
                }
            else:
                return value
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
        if isinstance(value, DataModel):
            value = value.get_base_model()
        elif isinstance(value, list):
            value = [
                item.get_base_model() if isinstance(item, DataModel) else item
                for item in value
            ]
        elif isinstance(value, dict):
            value = {
                key: val.get_base_model() if isinstance(val, DataModel) else val
                for key, val in value.items()
            }

        req = ObjectPropertyPatchRequest(property=property, property_value=value)
        result: Result = self.rest_adapter.patch(
            f"/{type}/{str(id)}/property", data=req.model_dump(mode="json")
        )
        return result.data

    def patch_property(
        self,
        type: str,
        id: UUID,
        property: str,
        value: Any,
        patch_type: PatchType,
        patch_args: dict = None,
    ) -> Any:
        """set a property of an object on the lab

        Args:
            type (str): type of the object to set property on
            id (UUID): id of the object
            property (str): name of the property to set
            value (Any): value to set the property to
            patch_type (PatchType): type of patch to apply
            patch_args (dict, optional): arguments for the patch. Defaults to None.

        Returns:
            Any: response from the lab
        """
        if isinstance(value, DataModel):
            value = value.get_base_model()

        req = ObjectPropertyPatchRequest(
            property=property,
            property_value=value,
            patch_type=patch_type,
            patch_args=patch_args,
        )
        result: Result = self.rest_adapter.patch(
            f"/{type}/{str(id)}/property", data=req.model_dump(mode="json")
        )
        return result.data

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
        result: Result = self.rest_adapter.get(f"/{type}/", {"identifier": name})
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
            f"/{type}/{str(id)}/data", files=result_data
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
        result: Result = self.rest_adapter.get(
            f"/{type}/{str(id)}/data", jsonify=False
        )
        return result.content
