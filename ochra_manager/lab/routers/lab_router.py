import logging
from fastapi import APIRouter
from ochra_common.connections.api_models import ObjectPropertySetRequest, ObjectConstructionRequest
from ..lab_service import LabService
from ochra_common.utils.misc import is_valid_uuid
from typing import Any

logger = logging.getLogger(__name__)
COLLECTIONS = ["stations", "robots", "scientists"]


class LabRouter(APIRouter):
    def __init__(self):
        prefix = "/lab"
        super().__init__(prefix=prefix)
        self.lab_service = LabService()
        self.get("/{object_type}/get")(self.get_lab_object)
        self.get("/{object_type}/get_all")(self.get_lab_objects)

    async def get_lab_object(self, object_type:str, identifier: str):
        collection = object_type if object_type in COLLECTIONS else None
        if is_valid_uuid(identifier):
            return self.lab_service.get_object_by_id(identifier, collection)
        else:
            return self.lab_service.get_object_by_name(identifier, collection)

    async def get_lab_objects(self, object_type:str):
        collection = object_type if object_type in COLLECTIONS else None
        return self.lab_service.get_all_objects(collection)