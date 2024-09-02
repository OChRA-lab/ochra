from ochra_common.connections.db_connection import DbConnection
from fastapi import FastAPI, APIRouter, HTTPException, Request
from .models.lab_request_models import ObjectSet, ObjectConstructionModel, ObjectCallModel
import uvicorn
import logging

from .lab_processor import lab_service
from .routers.device_router import device_router

logger = logging.getLogger(__name__)


class LabCommunication():
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        super().__init__()
        self.app = FastAPI()
        self.router = APIRouter()

        self.router.add_api_route(
            "/object/set/{object_id}",
            self.patch_object,
            methods=["PATCH"])

        self.router.add_api_route(
            "/object/construct",
            self.construct_object,
            methods=["POST"])

        self.router.add_api_route(
            "/object/call/{object_id}",
            self.call_on_object,
            methods=["POST"])

        self.router.add_api_route(
            "/object/get/{objectName}",
            self.get_object,
            methods=["GET"])
        self.router.add_api_route(
            "/station/create",
            self.create_station,
            methods=["POST"])

        self.router.add_api_route(
            "/object/get_property/{id}/{property}",
            self.get_object_property,
            methods=["GET"])

        self.app.include_router(self.router)
        self.app.include_router(device_router)

    def patch_object(self, object_id: str, args: ObjectSet):
        return lab_service.patch_object(object_id, args)

    def construct_object(self, args: ObjectConstructionModel):
        return lab_service.construct_object(args)

    def call_on_object(self, object_id: str, args: ObjectCallModel):
        return lab_service.call_on_object(object_id, args)

    def get_object(self, objectName: str):
        return lab_service.get_object(objectName)

    def get_object_property(self, id: str, property: str):
        return lab_service.get_object_property(id, property)

    def create_station(self, request: Request):
        return lab_service.create_station(request)

    def run(self):
        logger.info("started server")
        uvicorn.run(self.app, host=self.host, port=self.port)

    if __name__ == "__main__":
        aa = LabBase()
        aa.run(True)
