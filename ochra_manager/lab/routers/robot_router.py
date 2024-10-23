import logging
from fastapi import APIRouter
from ochra_common.connections.api_models import ObjectCallRequest, ObjectPropertySetRequest, ObjectConstructionRequest
from ..lab_service import LabService
from ochra_common.utils.misc import is_valid_uuid

logger = logging.getLogger(__name__)
COLLECTION = "robots"


class RobotRouter(APIRouter):
    def __init__(self):
        prefix = f"/{COLLECTION}"
        super().__init__(prefix=prefix)
        self.lab_service = LabService()
        self.put("/construct")(self.construct_robot)
        self.get("/{object_id}/get_property/{property}")(self.get_property)
        self.patch("/{object_id}/modify_property")(self.modify_property)
        self.post("/{object_id}/call_method")(self.call_robot)
        self.get("/get")(self.get_robot)

    async def construct_robot(self, args: ObjectConstructionRequest):
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_property(self, object_id: str, property: str):
        return self.lab_service.get_object_property(object_id, COLLECTION, property)

    async def modify_property(self, object_id: str, args: ObjectPropertySetRequest):
        return self.lab_service.patch_object(object_id, COLLECTION, args)

    async def call_robot(self, object_id: str, args: ObjectCallRequest):
        return self.lab_service.call_on_object(object_id, COLLECTION, args)

    async def get_robot(self, identifier: str):
        if is_valid_uuid(identifier):
            return self.lab_service.get_object_by_id(identifier, COLLECTION)
        else:
            return self.lab_service.get_object_by_name(identifier, COLLECTION)
