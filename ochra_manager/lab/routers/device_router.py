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
COLLECTION = "devices"


class DeviceRouter(APIRouter):
    def __init__(self, scheduler):
        prefix = f"/{COLLECTION}"
        super().__init__(prefix=prefix)
        self.scheduler = scheduler
        self.lab_service = LabService()
        self.put("/construct")(self.construct_device)
        self.get("/{identifier}/get_property")(self.get_device_property)
        self.patch("/{identifier}/modify_property")(self.modify_device_property)
        self.post("/{identifier}/call_method")(self.call_device)
        self.get("/get")(self.get_device)
        self.delete("/{identifier}/delete")(self.delete_device)

    async def construct_device(self, args: ObjectConstructionRequest):
        # TODO: we need to assign the object to the station somehow
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_device_property(
        self, identifier: str, args: ObjectPropertyGetRequest
    ):
        return self.lab_service.get_object_property(identifier, COLLECTION, args)

    async def modify_device_property(
        self, identifier: str, args: ObjectPropertyPatchRequest
    ):
        return self.lab_service.patch_object(identifier, COLLECTION, args)

    async def call_device(self, identifier: str, args: ObjectCallRequest):
        op = self.lab_service.call_on_object(identifier, "device", args)
        self.scheduler.add_operation(op)
        return op.get_base_model().model_dump(mode="json")

    async def get_device(self, identifier: str):
        if is_valid_uuid(identifier):
            device_obj = self.lab_service.get_object_by_id(identifier, COLLECTION)
        else:
            device_obj = self.lab_service.get_object_by_name(identifier, COLLECTION)

        return convert_to_data_model(device_obj)

    async def delete_device(self, identifier: str):
        self.lab_service.delete_object(identifier, COLLECTION)
        return {"message": "Device deleted successfully"}
