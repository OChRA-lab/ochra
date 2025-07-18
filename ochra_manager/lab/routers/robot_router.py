import logging
from fastapi import APIRouter
from ochra_common.connections.api_models import (
    ObjectCallRequest,
    ObjectPropertyPatchRequest,
    ObjectConstructionRequest,
    ObjectPropertyGetRequest,
)
from ..lab_service import LabService
from ochra_common.utils.misc import is_valid_uuid, convert_to_data_model

logger = logging.getLogger(__name__)
COLLECTION = "robots"
logger.info("Test message")

class RobotRouter(APIRouter):
    def __init__(self, scheduler):
        prefix = f"/{COLLECTION}"
        super().__init__(prefix=prefix)
        self.scheduler = scheduler
        self.lab_service = LabService()
        self.put("/construct")(self.construct_robot)
        self.get("/{identifier}/get_property")(self.get_property)
        self.patch("/{identifier}/modify_property")(self.modify_property)
        self.post("/{identifier}/call_method")(self.call_robot)
        self.get("/get")(self.get_robot)
        self.delete("/{identifier}/delete")(self.delete_robot)

    async def construct_robot(self, args: ObjectConstructionRequest):
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_property(self, identifier: str, args: ObjectPropertyGetRequest):
        return self.lab_service.get_object_property(identifier, COLLECTION, args)

    async def modify_property(self, identifier: str, args: ObjectPropertyPatchRequest):
        return self.lab_service.patch_object(identifier, COLLECTION, args)

    async def call_robot(self, identifier: str, args: ObjectCallRequest):
        op = self.lab_service.call_on_object(identifier, "robot", args)
        self.scheduler.add_operation(op)
        return op.get_base_model().model_dump(mode="json")

    async def get_robot(self, identifier: str):
        if is_valid_uuid(identifier):
            robot_obj = self.lab_service.get_object_by_id(identifier, COLLECTION)
        else:
            robot_obj = self.lab_service.get_object_by_name(identifier, COLLECTION)

        return convert_to_data_model(robot_obj)

    async def delete_robot(self, identifier: str):
        self.lab_service.delete_object(identifier, COLLECTION)
        return {"message": "Robot deleted successfully"}