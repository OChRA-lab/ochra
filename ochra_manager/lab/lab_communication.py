from ochra_common.connections.db_connection import DbConnection
from fastapi import FastAPI, APIRouter, HTTPException, Request
import uvicorn
import logging

from ochra_manager.lab.lab_processor import LabProcessor

logger = logging.getLogger(__name__)


class LabCommunication(LabProcessor):
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

    def run(self):
        logger.info("started server")
        uvicorn.run(self.app, host=self.host, port=self.port)

    if __name__ == "__main__":
        aa = LabBase()
        aa.run(True)
