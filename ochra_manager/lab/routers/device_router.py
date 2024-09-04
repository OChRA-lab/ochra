import logging
from fastapi import APIRouter
from ochra_common.connections.api_models import ObjectCallRequest, ObjectPropertySetRequest, ObjectConstructionRequest, ObjectQueryResponse
from ..lab_processor import lab_service
from typing import Any

logger = logging.getLogger(__name__)
COLLECTION = "devices"


class DeviceRouter(APIRouter):
    def __init__(self):
        prefix = f"/{COLLECTION}"
        super().__init__(prefix=prefix)
        self.lab_service = lab_service()
        self.put("/{station_id}/construct")(self.construct_device)
        self.get("/{object_id}/get_property/{property}")(self.get_device_property)
        self.patch("/{object_id}/modify_property")(self.modify_device_property)
        self.post("/{station_id}/{object_id}/call_method")(self.call_device)
        self.get("/{station_id}/get")(self.get_device)

    async def construct_device(self, args: ObjectConstructionRequest):
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_device_property(self, object_id: str, property: str):
        return self.lab_service.get_object_property(object_id, COLLECTION, property)

    async def modify_device_property(self, object_id: str, args: ObjectPropertySetRequest):
        return self.lab_service.patch_object(object_id, COLLECTION, args)

    async def call_device(self, object_id: str, args: ObjectCallRequest):
        return self.lab_service.call_on_object(object_id, COLLECTION, args)

    async def get_device(self, station_id: str, device_name: str):
        return self.lab_service.get_device(station_id, device_name)
