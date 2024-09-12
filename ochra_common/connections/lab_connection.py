from ochra_common.utils.singleton_meta import SingletonMeta
from ochra_common.connections.rest_adapter import RestAdapter, Result, LabEngineException
from .api_models import ObjectConstructionRequest, ObjectQueryResponse, ObjectCallRequest, ObjectCallResponse, ObjectPropertySetRequest
from uuid import UUID
import logging
from typing import Any


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

    def construct_object(self, type: str, object) -> UUID:
        req = ObjectConstructionRequest(object=object.model_dump())
        result: Result = self.rest_adapter.put(
            f"/{type}/construct", req.model_dump_json())
        try:
            id = UUID(result.data)
            return id
        except ValueError:
            raise LabEngineException(
                f"Expected UUID, got {result.data}")
        except Exception as e:
            raise LabEngineException(
                f"Unexpected error: {e}")

    def get_object_by_name(self, type: str, name: str) -> ObjectQueryResponse:
        result: Result = self.rest_adapter.get(
            f"/{type}/get", {"name": name})
        try:
            return ObjectQueryResponse(**result.data)
        except ValueError:
            raise LabEngineException(
                f"Expected ObjectQueryResponse, got {result.data}")
        except Exception as e:
            raise LabEngineException(
                f"Unexpected error: {e}")

    def get_object_by_uuid(self, type: str, id: UUID) -> ObjectQueryResponse:
        result: Result = self.rest_adapter.get(f"/{type}/get_by_id/{id.hex}")
        try:
            return ObjectQueryResponse(**result.data)
        except ValueError:
            raise LabEngineException(
                f"Expected ObjectQueryResponse, got {result.data}")
        except Exception as e:
            raise LabEngineException(
                f"Unexpected error: {e}")

    def delete_object(self, type: str, id: UUID):
        result: Result = self.rest_adapter.delete(f"/{type}/delete/{id.hex}")
        return result.data

    def call_on_object(self, type: str, id: UUID, method: str, args: dict) -> ObjectCallResponse:
        req = ObjectCallRequest(method=method, args=args)
        result: Result = self.rest_adapter.post(
            f"/{type}/{id.hex}/call_method", req.model_dump_json())
        try:
            return ObjectCallResponse(**result.data)
        except ValueError:
            raise LabEngineException(
                f"Expected ObjectCallResponse, got {result.data}")
        except Exception as e:
            raise LabEngineException(
                f"Unexpected error: {e}")

    def get_property(self, type: str, id: UUID, property: str) -> Any | ObjectQueryResponse:
        result: Result = self.rest_adapter.get(
            f"/{type}/{id.hex}/get_property/{property}")
        if result.status_code == 404:
            raise LabEngineException(
                f"Property {property} not found for {type} {id}")
        try:
            return ObjectQueryResponse(**result.data)
        except TypeError:
            return result.data
        except Exception as e:
            raise LabEngineException(
                f"Unexpected error: {e}")

    def set_property(self, type: str, id: UUID, property: str, value: Any):
        req = ObjectPropertySetRequest(property=property, property_value=value)
        result: Result = self.rest_adapter.post(
            f"/{type}/{id.hex}/modify_property", req.model_dump_json())
        return result.data
