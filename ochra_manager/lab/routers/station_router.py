import logging
from fastapi import APIRouter, Request
from ochra_common.connections.api_models import ObjectCallRequest, ObjectConstructionRequest, ObjectPropertySetRequest
from ..lab_service import LabService
import json

logger = logging.getLogger(__name__)
COLLECTION = "stations"


class StationRouter(APIRouter):
    def __init__(self):
        super().__init__(prefix=f"/{COLLECTION}")
        self.lab_service = LabService()
        self.put("/construct")(self.construct_station)
        self.get(
            "/{object_id}/get_property/{property}")(self.get_station_property)
        self.patch("/{object_id}/modify_property")(self.modify_property)
        self.post("/{object_id}/call_method")(self.call_method)
        self.get("/get")(self.get_station)

    async def construct_station(self, args: ObjectConstructionRequest, request: Request):
        print(request.client.host)
        object = json.loads(args.object_json)
        object["station_ip"] = request.client.host
        args.object_json = json.dumps(object)
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_station_property(self, object_id: str, property: str):
        return self.lab_service.get_object_property(object_id, COLLECTION, property)

    async def modify_property(self, object_id: str, args: ObjectPropertySetRequest):
        return self.lab_service.patch_object(object_id, COLLECTION, args)

    async def call_method(self, object_id: str, args: ObjectCallRequest):
        return self.lab_service.call_on_object(object_id, COLLECTION, args)

    async def get_station(self, station_name: str):
        return self.lab_service.get_object_by_name(station_name, COLLECTION)
