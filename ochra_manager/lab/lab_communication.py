from fastapi import FastAPI, APIRouter, HTTPException, Request
import uvicorn
import logging
from .routers.device_router import DeviceRouter
from .routers.station_router import StationRouter
from .routers.robot_router import RobotRouter

logger = logging.getLogger(__name__)


class LabCommunication():
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.app = FastAPI()

        self.app.include_router(DeviceRouter())
        self.app.include_router(StationRouter())
        self.app.include_router(RobotRouter())

    def run(self):
        logger.info("started server")
        uvicorn.run(self.app, host=self.host, port=self.port)
