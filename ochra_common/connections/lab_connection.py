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
from typing import Any, Type, Union, List
import importlib
from ..equipment.operation import Operation
from ..utils.enum import OperationStatus, PatchType
from ..utils.misc import is_data_model, convert_to_data_model
import time

# TODO change the return types of get_property and get_all_objects to be more specific


class LabConnection(metaclass=SingletonMeta):
    """
    Class that provides a high-level interface for interacting with the lab engine API,
    utilizing RestAdapter for communication. This class is tightly integrated with the lab engine's API structure.
    """

    def __init__(
        self,
        hostname: str = "127.0.0.1:8000",
        experiment_id: str = None,
        api_key: str = "",
        ssl_verify: bool = False,
    ):
        """
        Constructor for LabConnection class.

        Args:
            hostname (str): Address of lab API. Defaults to "127.0.0.1:8000".
            experiment_id (str, optional): ID of the experiment associated with this connection.
                If None, a new UUID will be generated. Defaults to None.
            api_key (str, optional): API key if exists. Defaults to ''.
            ssl_verify (bool, optional): If we need to verify SSL. Defaults to False.
        """
        self._logger = logging.getLogger(__name__)
        self.rest_adapter: RestAdapter = RestAdapter(
            hostname, api_key, ssl_verify, self._logger
        )
        if experiment_id is None:
            self._session_id = str(uuid4())
        else:
            self._session_id = experiment_id

    def load_from_data_model(self, model: DataModel) -> Any:
        """
        Instantiates an object from a given DataModel.

        Args:
            model (DataModel): The data model containing class and module information.

        Raises:
            LabEngineException: If the class cannot be imported or instantiated.

        Returns:
            Any: An instance of the specified class, loaded using its ID.
        """
        try:
            module = importlib.import_module(model.module_path)
            class_to_instance = getattr(module, model.cls)
            instance = class_to_instance.from_id(model.id)
            return instance
        except Exception as e:
            raise LabEngineException(f"Unexpected error in importing class: {e}")

    def construct_object(self, type: str, object: Type[DataModel]) -> UUID:
        """
        Constructs an object on the lab engine.

        Args:
            type (str): The type of the object to construct.
            object (Type[DataModel]): The data model instance representing the object to be constructed.

        Raises:
            LabEngineException: If there is an error during object construction or response parsing.

        Returns:
            UUID: The unique identifier of the constructed object.
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

    def get_object(self, type: str, identifier: str | UUID) -> Any:
        """
        Retrieve an object from the lab engine by its identifier.

        Args:
            type (str): The type of the object to retrieve.
            identifier (str | UUID): The unique ID or name of the object.

        Raises:
            LabEngineException: If the object cannot be retrieved or parsed.

        Returns:
            Any: An instance of the requested object, loaded from its data model.
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
        """
        Retrieve all objects of a specified type from the lab engine.

        Args:
            type (str): The type of objects to retrieve.

        Raises:
            LabEngineException: If retrieval or parsing fails.

        Returns:
            List[Any]: List of instantiated objects corresponding to the specified type.
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
        """
        Deletes an object from the lab engine.

        Args:
            type (str): The type of the object to delete.
            id (UUID): The unique identifier of the object.

        Raises:
            LabEngineException: If deletion fails.

        Returns:
            Any: Response from the lab engine.
        """
        result: Result = self.rest_adapter.delete(f"/{type}/{str(id)}/")
        return result.data

    def call_on_object(self, type: str, id: UUID, method: str, args: dict) -> Operation:
        """
        Initiates a method call on a specified object within the lab engine.

        Args:
            type (str): The type of the object to invoke the method on.
            id (UUID): The unique identifier of the target object.
            method (str): The name of the method to execute.
            args (dict): Arguments to pass to the method.

        Raises:
            LabEngineException: If the method invocation fails or the response cannot be parsed.

        Returns:
            Operation: An Operation instance representing the status and result of the method call.
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
        """
        Retrieves the value of a specified property from an object on the lab engine.

        Args:
            type (str): The type of the object.
            id (UUID): The unique identifier of the object.
            property (str): The name of the property to retrieve.

        Raises:
            LabEngineException: If the property cannot be retrieved or parsed.

        Returns:
            Any: The value of the requested property, which may be a primitive, DataModel instance, list, or dict.
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
        """
        Sets the value of a specified property on an object in the lab engine.

        Args:
            type (str): The type of the object to update.
            id (UUID): The unique identifier of the object.
            property (str): The name of the property to set.
            value (Any): The value to assign to the property.

        Returns:
            Any: The response from the lab engine after setting the property.

        Raises:
            LabEngineException: If the property update fails.
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
        """
        Applies a patch operation to a specified property of an object in the lab engine.

        Args:
            type (str): The type of the object whose property will be patched.
            id (UUID): The unique identifier of the object.
            property (str): The name of the property to patch.
            value (Any): The value to apply in the patch operation.
            patch_type (PatchType): The type of patch operation (e.g., ADD, REMOVE, REPLACE).
            patch_args (dict, optional): Additional arguments for the patch operation. Defaults to None.

        Returns:
            Any: The response from the lab engine after applying the patch.

        Raises:
            LabEngineException: If the patch operation fails.
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
        """
        Retrieves the unique identifier (UUID) of an object from the lab engine using its name.

        Args:
            type (str): The type of the object to retrieve.
            name (str): The name of the object.

        Raises:
            LabEngineException: If the object cannot be found or the response is invalid.

        Returns:
            UUID: The unique identifier of the object.
        """
        result: Result = self.rest_adapter.get(f"/{type}/", {"identifier": name})
        try:
            return UUID(result.data["id"])
        except ValueError:
            raise LabEngineException(f"Expected UUID, got {result.data}")
        except Exception as e:
            raise LabEngineException(f"Unexpected error: {e}")

    def put_data(self, type: str, id: str, result_data) -> UUID:
        """
        Uploads data to a OperationResult object in the lab engine.

        Args:
            type (str): The type of the object to upload data to.
            id (str): The unique identifier of the object.
            result_data (Any): The data to upload (e.g., file-like object, bytes, or dict).

        Returns:
            UUID: The unique identifier of the object after data upload.

        Raises:
            LabEngineException: If the upload fails or the response is invalid.
        """
        result: Result = self.rest_adapter.patch(
            f"/{type}/{str(id)}/data", files=result_data
        )
        return result.message

    def get_data(self, type: str, id: str) -> bytes:
        """
        Retrieves raw data from a results data object in the lab engine.

        Args:
            type (str): The type of the object to retrieve data from.
            id (str): The unique identifier of the object.

        Returns:
            bytes: The raw bytes of the object's data.

        Raises:
            LabEngineException: If data retrieval fails.
        """
        result: Result = self.rest_adapter.get(f"/{type}/{str(id)}/data", jsonify=False)
        return result.content
