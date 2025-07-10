import logging
from fastapi import APIRouter, Request
from ochra_common.connections.api_models import (
    ObjectCallRequest,
    ObjectConstructionRequest,
    ObjectPropertyPatchRequest,
    ObjectPropertyGetRequest
)
from ..lab_service import LabService
from ochra_common.utils.misc import is_valid_uuid, convert_to_data_model
import json

logger = logging.getLogger("routers")
COLLECTION = "stations"


class StationRouter(APIRouter):
    def __init__(self, scheduler):
        super().__init__(prefix=f"/{COLLECTION}")
        self.scheduler = scheduler
        self.lab_service = LabService()
        self.put("/construct")(self.construct_station)
        self.get("/{identifier}/get_property")(self.get_station_property)
        self.patch("/{identifier}/modify_property")(self.modify_property)
        self.post("/{identifier}/call_method")(self.call_method)
        self.get("/get")(self.get_station)
        self.delete("/{identifier}/delete")(self.delete_station)

    async def construct_station(
        self, args: ObjectConstructionRequest, request: Request
    ):
        print(request.client.host)
        object = json.loads(args.object_json)
        # TODO we can just set this as part of the station model
        object["station_ip"] = request.client.host
        args.object_json = json.dumps(object)
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_station_property(self, identifier: str, args: ObjectPropertyGetRequest):
        return self.lab_service.get_object_property(identifier, COLLECTION, args)

    async def modify_property(self, identifier: str, args: ObjectPropertyPatchRequest):
        return self.lab_service.patch_object(identifier, COLLECTION, args)

    async def call_method(self, identifier: str, args: ObjectCallRequest):
        op = self.lab_service.call_on_object(identifier, "station", args)
        self.scheduler.add_operation(op)
        return op.get_base_model().model_dump(mode="json")

    async def get_station(self, identifier: str):
        if is_valid_uuid(identifier):
            station_obj = self.lab_service.get_object_by_id(identifier, COLLECTION)
        else:
            station_obj = self.lab_service.get_object_by_name(identifier, COLLECTION)

        return convert_to_data_model(station_obj)
    
    async def delete_station(self, identifier: str):
        self.lab_service.delete_object(identifier, COLLECTION)
        return {"message": "Station deleted successfully"}
