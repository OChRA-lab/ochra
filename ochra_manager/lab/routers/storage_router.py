import logging
from fastapi import APIRouter
from typing import Any, Dict
from ochra_common.connections.api_models import (
    ObjectPropertyPatchRequest,
    ObjectConstructionRequest,
    ObjectPropertyGetRequest,
)
from ..utils.lab_service import LabService
from ochra_common.base.data_model import DataModel
from ochra_common.utils.misc import is_valid_uuid, convert_to_data_model

COLLECTIONS = ["consumables", "containers", "inventories", "reagents"]


class StorageRouter(APIRouter):
    """
    StorageRouter is responsible for handling storage-related API endpoints.
    """

    def __init__(self):
        prefix = "/storage"
        super().__init__(prefix=prefix)
        self._logger = logging.getLogger(__name__)
        self.lab_service = LabService()

        # routes for containers
        self.put("/{object_type}/")(self.construct_storage_item)
        self.get("/{object_type}/{identifier}/property")(self.get_storage_item_property)
        self.patch("/{object_type}/{identifier}/property")(
            self.modify_storage_item_property
        )
        self.get("/{object_type}/")(self.get_storage_item)
        self.delete("/{object_type}/{identifier}/")(self.delete_storage_item)

    async def construct_storage_item(
        self, object_type: str, args: ObjectConstructionRequest
    ) -> str:
        """
        Construct a new storage item in the lab.

        Args:
            args (ObjectConstructionRequest): The construction parameters for the storage item.

        Returns:
            str: The ID of the constructed storage item.
        """
        self._logger.debug(f"Constructing {object_type} with args: {args}")
        collection = object_type if object_type in COLLECTIONS else None
        return self.lab_service.construct_object(args, collection)

    async def get_storage_item_property(
        self, object_type: str, identifier: str, args: ObjectPropertyGetRequest
    ) -> Any:
        """
        Get properties of a storage item.

        Args:
            identifier (str): The ID of the storage item.
            args (ObjectPropertyGetRequest): The properties to retrieve.

        Returns:
            Any: The requested properties of the storage item.
        """
        self._logger.debug(
            f"Getting property for {object_type} {identifier} with args: {args}"
        )
        collection = object_type if object_type in COLLECTIONS else None
        return self.lab_service.get_object_property(identifier, collection, args)

    async def modify_storage_item_property(
        self, object_type: str, identifier: str, args: ObjectPropertyPatchRequest
    ) -> bool:
        """
        Modify properties of a storage item.

        Args:
            identifier (str): The ID of the storage item.
            args (ObjectPropertyPatchRequest): The properties to modify.

        Returns:
            bool: True if the modification was successful, False otherwise.
        """
        self._logger.debug(
            f"Modifying property for {object_type} {identifier} with args: {args}"
        )
        collection = object_type if object_type in COLLECTIONS else None
        return self.lab_service.patch_object(identifier, collection, args)

    async def get_storage_item(self, object_type: str, identifier: str) -> DataModel:
        """
        Get a storage item by its ID.

        Args:
            identifier (str): The ID of the storage item.

        Returns:
            DataModel: The storage item data model.
        """
        collection = object_type if object_type in COLLECTIONS else None
        if is_valid_uuid(identifier):
            storage_obj = self.lab_service.get_object_by_id(identifier, collection)
        else:
            storage_obj = self.lab_service.get_object_by_name(identifier, collection)

        self._logger.debug(f"Getting {object_type} with identifier: {identifier}")
        return convert_to_data_model(storage_obj)

    async def delete_storage_item(self, object_type: str, identifier: str) -> Dict:
        """
        Delete a storage item by its ID.
        
        Args:
            identifier (str): The ID of the storage item.
        
        Returns:
            Dict: A message indicating the result of the deletion.
        """
        collection = object_type if object_type in COLLECTIONS else None
        self._logger.debug(f"Deleting {object_type} with identifier: {identifier}")
        self.lab_service.delete_object(identifier, collection)
        return {"message": f"{object_type} deleted successfully"}
