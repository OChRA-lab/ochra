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
        self.app = FastAPI()

        self.app.include_router(device_router)

    def run(self):
        logger.info("started server")
        uvicorn.run(self.app, host=self.host, port=self.port)

    if __name__ == "__main__":
        aa = LabBase()
        aa.run(True)
