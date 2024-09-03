import logging
from fastapi import APIRouter
from ..models.lab_request_models import ObjectSet, ObjectCallModel
from ..lab_processor import lab_service

logger = logging.getLogger(__name__)
COLLECTION = "stations"


class StationRouter(APIRouter):
    def __init__(self):
        super().__init__(prefix=f"/{COLLECTION}")

        self.post("/construct")(self.construct_station)
        self.get(
            "/{object_id}/get_property/{property}")(self.get_station_property)
        self.patch("/{object_id}/modify_property")(self.modify_property)
        self.post("/{object_id}/call_method")(self.call_method)
        self.get("/get")(self.get_station)

    async def construct_station(self, name: str, constructor_params: dict):
        db_entry = {"name": name, **constructor_params}
        return lab_service.construct_object(db_entry, COLLECTION)

    async def get_station_property(self, object_id: str, property: str):
        return lab_service.get_object_property(object_id, COLLECTION, property)

    async def modify_property(self, object_id: str, args: ObjectSet):
        return lab_service.patch_object(object_id, COLLECTION, args)

    async def call_method(self, object_id: str, args: ObjectCallModel):
        return lab_service.call_on_object(object_id, COLLECTION, args)

    async def get_station(self, station_name: str):
        return lab_service.get_object_by_name(station_name, COLLECTION)
