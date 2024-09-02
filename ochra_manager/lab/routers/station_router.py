import logging
from fastapi import APIRouter
from ..models.lab_request_models import ObjectSet, ObjectCallModel
from ..lab_processor import lab_service

logger = logging.getLogger(__name__)
COLLECTION = "stations"
stations_router = APIRouter(prefix="/{COLLECTION}")


@stations_router.post("/construct")
async def construct_device(name: str, constructor_params: dict):
    db_entry = {"name": name, **constructor_params}
    return lab_service.construct_object(db_entry, COLLECTION)


@stations_router.get("{object_id}/get_property/{property}")
async def get_station_property(object_id: str, property: str):
    return lab_service.get_object_property(object_id, COLLECTION, property)


@stations_router.patch("{object_id}/modify_property")
async def modify_property(object_id: str, args: ObjectSet):
    return lab_service.patch_object(object_id, COLLECTION, args)


@stations_router.post("/{object_id}/call_method")
async def call_method(object_id: str, args: ObjectCallModel):
    return lab_service.call_on_object(object_id, COLLECTION, args)


@stations_router.get("/get")
async def get_station(station_name: str):
    return lab_service.get_object(station_name, COLLECTION)
