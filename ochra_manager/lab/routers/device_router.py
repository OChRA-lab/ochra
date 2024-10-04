import logging
from fastapi import APIRouter
from ochra_common.connections.api_models import ObjectCallRequest, ObjectPropertySetRequest, ObjectConstructionRequest, ObjectQueryResponse
from ..lab_service import LabService
from ochra_common.utils.misc import is_valid_uuid
from typing import Any

logger = logging.getLogger(__name__)
COLLECTION = "devices"


class DeviceRouter(APIRouter):
    def __init__(self):
        prefix = f"/{COLLECTION}"
        super().__init__(prefix=prefix)
        self.lab_service = LabService()
        self.put("/construct")(self.construct_device)
        self.get("/{object_id}/get_property/{property}")(self.get_device_property)
        self.patch("/{object_id}/modify_property")(self.modify_device_property)
        self.post("/{object_id}/call_method")(self.call_device)
        self.get("/{station_id}/get_by_station/{device_type}")(self.get_device_by_station)
        self.get("/get")(self.get_device)

    async def construct_device(self, args: ObjectConstructionRequest):
        # TODO: we need to assign the object to the station somehow
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_device_property(self, object_id: str, property: str):
        return self.lab_service.get_object_property(object_id, COLLECTION, property)

    async def modify_device_property(self, object_id: str, args: ObjectPropertySetRequest):
        return self.lab_service.patch_object(object_id, COLLECTION, args)

    async def call_device(self, object_id: str, args: ObjectCallRequest):
        return self.lab_service.call_on_object(object_id, COLLECTION, args)

    async def get_device_by_station(self, station_id: str, device_type: str):
        return self.lab_service.get_object_by_station_and_type(station_id, COLLECTION, device_type)

    async def get_device(self, identifier: str):
        if is_valid_uuid(identifier):
            return self.lab_service.get_object_by_id(identifier, COLLECTION)
        else:
            return self.lab_service.get_object_by_name(identifier, COLLECTION)
