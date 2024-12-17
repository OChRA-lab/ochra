from fastapi import FastAPI, APIRouter, HTTPException, Request
import uvicorn
import logging
from .routers.device_router import DeviceRouter
from .routers.station_router import StationRouter
from .routers.robot_router import RobotRouter
from .routers.operation_router import OperationRouter
from .routers.lab_router import LabRouter
from .routers.storage_router import StorageRouter
from .routers.operation_results_router import OperationResultRouter
import inspect

logger = logging.getLogger(__name__)


class LabServer:
    def __init__(self, host: str, port: int, folderpath: str = "") -> None:
        self.host = host
        self.port = port
        self.app = FastAPI()

        self.app.include_router(LabRouter())
        self.app.include_router(DeviceRouter())
        self.app.include_router(StationRouter())
        self.app.include_router(RobotRouter())
        self.app.include_router(OperationRouter())
        self.app.include_router(StorageRouter())
        self.app.include_router(OperationResultRouter(folderpath))

    def get_caller_variable_name(self):
        frame = inspect.currentframe().f_back.f_back
        fileName: str = frame.f_locals.get("__file__")[:-3]
        fileNameSplit = fileName.split("\\")
        variableName = None
        for name, value in frame.f_locals.items():
            if value is self:
                variableName = name
        return fileNameSplit[-1] + ":" + variableName + ".app"

    def run(self) -> None:
        logger.info("started server")
        app = self.get_caller_variable_name()
        uvicorn.run(app, host=self.host, port=self.port, workers=8)
