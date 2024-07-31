from ochra_common.connections.db_connection import DbConnection
from fastapi import FastAPI, APIRouter, HTTPException, Request
import uvicorn
import logging

from ochra_manager.lab.lab_processor import LabProcessor

logger = logging.getLogger(__name__)


class LabCommunication(LabProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.app = FastAPI()
        self.router = APIRouter()
        logging.basicConfig(filename="labServer.log",
                            level=logging.DEBUG,
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

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

        self.app.include_router(self.router)

    def run(self):
        logger.info("started server")
        uvicorn.run(self.app, host="0.0.0.0")


if __name__ == "__main__":
    aa = LabBase()
    aa.run(True)
