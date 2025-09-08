import logging
from fastapi import APIRouter
from ochra_common.connections.api_models import (
    ObjectPropertyPatchRequest,
    ObjectConstructionRequest,
    ObjectPropertyGetRequest,
)
from ..lab_service import LabService
from ochra_common.utils.misc import is_valid_uuid, convert_to_data_model

COLLECTIONS = ["consumables", "containers", "inventories", "reagents"]


class StorageRouter(APIRouter):
    def __init__(self):
        prefix = "/storage"
        super().__init__(prefix=prefix)
        self._logger = logging.getLogger(__name__)
        self.lab_service = LabService()

        # routes for containers
        self.put("/{object_type}/construct")(self.construct_storage_item)
        self.get("/{object_type}/{identifier}/get_property")(
            self.get_storage_item_property
        )
        self.patch("/{object_type}/{identifier}/modify_property")(
            self.modify_storage_item_property
        )
        self.get("/{object_type}/get")(self.get_storage_item)
        self.delete("/{object_type}/{identifier}/delete")(self.delete_storage_item)

    async def construct_storage_item(
        self, object_type: str, args: ObjectConstructionRequest
    ):
        self._logger.debug(f"Constructing {object_type} with args: {args}")
        collection = object_type if object_type in COLLECTIONS else None
        return self.lab_service.construct_object(args, collection)

    async def get_storage_item_property(
        self, object_type: str, identifier: str, args: ObjectPropertyGetRequest
    ):
        self._logger.debug(f"Getting property for {object_type} {identifier} with args: {args}")
        collection = object_type if object_type in COLLECTIONS else None
        return self.lab_service.get_object_property(identifier, collection, args)

    async def modify_storage_item_property(
        self, object_type: str, identifier: str, args: ObjectPropertyPatchRequest
    ):
        self._logger.debug(f"Modifying property for {object_type} {identifier} with args: {args}")
        collection = object_type if object_type in COLLECTIONS else None
        return self.lab_service.patch_object(identifier, collection, args)

    async def get_storage_item(self, object_type: str, identifier: str):
        collection = object_type if object_type in COLLECTIONS else None
        if is_valid_uuid(identifier):
            storage_obj = self.lab_service.get_object_by_id(identifier, collection)
        else:
            storage_obj = self.lab_service.get_object_by_name(identifier, collection)
        
        self._logger.debug(f"Getting {object_type} with identifier: {identifier}")
        return convert_to_data_model(storage_obj)

    async def delete_storage_item(self, object_type: str, identifier: str):
        collection = object_type if object_type in COLLECTIONS else None
        self._logger.debug(f"Deleting {object_type} with identifier: {identifier}")
        self.lab_service.delete_object(identifier, collection)
        return {"message": f"{object_type} deleted successfully"}
