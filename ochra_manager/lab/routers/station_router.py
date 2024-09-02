import logging
from fastapi import APIRouter
from ..models.lab_request_models import ObjectSet, ObjectConstructionModel, ObjectCallModel
from ..lab_processor import lab_service

logger = logging.getLogger(__name__)
COLLECTION = "stations"
stations_router = APIRouter(prefix="/{COLLECTION}")


@stations_router.post("/construct")
async def construct_device(args: ObjectConstructionModel):
    return lab_service.construct_object(db_entry, COLLECTION)


@stations_router.get("{object_id}/get_property/{property}")
async def get_device_property(object_id: str, property: str):
    return lab_service.get_object_property(object_id, COLLECTION, property)


@stations_router.patch("{object_id}/modify_property")
async def modify_device_property(object_id: str, args: ObjectSet):
    return lab_service.patch_object(object_id, COLLECTION, args)


@stations_router.post("{station_id}/{object_id}/call_method")
async def call_device(object_id: str, args: ObjectCallModel):
    return lab_service.call_on_object(object_id, COLLECTION, args)


@stations_router.get("{station_id}/get")
async def get_device(station_id: str, device_name: str):
    return lab_service.get_device(station_id, device_name)
