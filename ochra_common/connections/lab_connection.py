from ..utils.singleton_meta import SingletonMeta
from .rest_adapter import RestAdapter, Result, LabEngineException
from .api_models import ObjectConstructionRequest, ObjectQueryResponse, ObjectCallRequest, ObjectCallResponse, ObjectPropertySetRequest
from pydantic import BaseModel, ValidationError
from uuid import UUID
import logging
from typing import Any, Type, Union
import importlib


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
            hostname, api_key, ssl_verify, logger)

    def load_from_response(self, obj: ObjectQueryResponse):
        try:
            moduleNameList = obj.cls.split(".")[:-1]
            moduleName = ".".join(moduleNameList)
            module = importlib.import_module(moduleName)
            class_to_instance = getattr(module, obj.cls.split(".")[-1])
            instance = class_to_instance.from_id(obj.id)
            return instance
        except Exception as e:
            raise LabEngineException(
                f"Unexpected error in importing class: {e}")

    def construct_object(self, type: str, object: Type[BaseModel]) -> UUID:
        req = ObjectConstructionRequest(object_json=object.model_dump_json())
        result: Result = self.rest_adapter.put(
            f"/{type}/construct", data=req.model_dump())
        try:
            id = UUID(result.data)
            return id
        except ValueError:
            raise LabEngineException(
                f"Expected UUID, got {result.data}")
        except Exception as e:
            raise LabEngineException(
                f"Unexpected error: {e}")

    def get_object(self, endpoint: str, identifier: Union[str, UUID]) -> ObjectQueryResponse:
        result: Result = self.rest_adapter.get(
                f"/{endpoint}/get/{str(identifier)}")
        try:
            object = ObjectQueryResponse(**result.data)
            return self.load_from_response(object)
        except ValueError:
            raise LabEngineException(
                f"Expected ObjectQueryResponse, got {result.data}")
        except Exception as e:
            raise LabEngineException(
                f"Unexpected error: {e}")

    def delete_object(self, type: str, id: UUID):
        result: Result = self.rest_adapter.delete(f"/{type}/delete/{str(id)}")
        return result.data

    def call_on_object(self, type: str, id: UUID, method: str, args: dict) -> ObjectCallResponse:
        req = ObjectCallRequest(method=method, args=args)
        result: Result = self.rest_adapter.post(
            f"/{type}/{str(id)}/call_method", data=req.model_dump())
        try:
            return ObjectCallResponse(**result.data)
        except ValueError:
            raise LabEngineException(
                f"Expected ObjectCallResponse, got {result.data}")
        except Exception as e:
            raise LabEngineException(
                f"Unexpected error: {e}")

    def get_property(self, type: str, id: UUID, property: str) -> Union[Any, ObjectQueryResponse]:
        result: Result = self.rest_adapter.get(
            f"/{type}/{str(id)}/get_property/{property}")
        if result.status_code == 404:
            raise LabEngineException(
                f"Property {property} not found for {type} {id}")
        try:
            if isinstance(result.data, list):
                return [self._convert_to_object_query_response_possibly(data) for data in result.data]
            elif isinstance(result.data, dict):
                return self._convert_to_object_query_response_possibly(result.data)
            else:
                return result.data
        except Exception as e:
            raise LabEngineException(
                f"Unexpected error: {e}")

    def set_property(self, type: str, id: UUID, property: str, value: Any):
        req = ObjectPropertySetRequest(property=property, property_value=value)
        result: Result = self.rest_adapter.patch(
            f"/{type}/{str(id)}/modify_property", data=req.model_dump())
        return result.data

    def get_by_station(self, station_identifier: Union[str, UUID], endpoint: str, objectType: str) -> ObjectQueryResponse:
        result: Result = self.rest_adapter.get(
            f"/{endpoint}/{str(station_identifier)}/get_by_station/{objectType}")
        try:
            return ObjectQueryResponse(**result.data)
        except ValidationError:
            raise LabEngineException(
                f"Expected ObjectQueryResponse, got {result.data}")
        except Exception as e:
            raise LabEngineException(
                f"Unexpected error: {e}")

    def _convert_to_object_query_response_possibly(self, data: Any) -> Union[ObjectQueryResponse, Any]:
        try:
            return ObjectQueryResponse(**data)
        except (ValidationError, TypeError):
            return data

    def get_object_id(self, endpoint: str, name: str) -> UUID:
        result: Result = self.rest_adapter.get(
            f"/{endpoint}/get", {"name": name})
        try:
            return UUID(result.data["id"])
        except ValueError:
            raise LabEngineException(
                f"Expected UUID, got {result.data}")
        except Exception as e:
            raise LabEngineException(
                f"Unexpected error: {e}")
