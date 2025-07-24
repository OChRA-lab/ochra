from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import logging
from ochra_manager.lab.auth.auth import SessionToken, get_db, init_user_db
from ochra_manager.lab.routers.ui_router import WebAppRouter
from .routers.device_router import DeviceRouter
from .routers.station_router import StationRouter
from .routers.robot_router import RobotRouter
from .routers.operation_router import OperationRouter
from .routers.lab_router import LabRouter
from .routers.storage_router import StorageRouter
from .routers.operation_results_router import OperationResultRouter
from .scheduler import Scheduler
import inspect


class LabServer:
    def __init__(
        self,
        host: str,
        port: int,
        folderpath: str,
        template_path: Optional[Path] = None,
    ) -> None:
        """Setup a lab server with the given host and port optionally storing data in folderpath

        Args:
            host (str): host ip address
            port (int): port to open the server on
            folderpath (str): path to store data in
        """
        MODULE_DIRECTORY = (
            Path(__file__).resolve().parent if not template_path else template_path
        )
        self._logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.scheduler = Scheduler()
        

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            self.scheduler.run()
            yield
            self.scheduler.stop()

        self.app = FastAPI(lifespan=lifespan)

        self.templates = Jinja2Templates(directory=MODULE_DIRECTORY / "templates")
        self.app.mount(
            "/static", StaticFiles(directory=MODULE_DIRECTORY / "static"), name="static"
        )

        self.app.include_router(LabRouter())
        self.app.include_router(DeviceRouter(self.scheduler))
        self.app.include_router(StationRouter(self.scheduler))
        self.app.include_router(RobotRouter(self.scheduler))
        self.app.include_router(OperationRouter())
        self.app.include_router(StorageRouter())
        self.app.include_router(OperationResultRouter(folderpath))

        ##NOTE: NEW ADDITIONS ###################
        self.app.include_router(WebAppRouter(self.templates))
        self.app.middleware("http")(self.auth_middleware)

        init_user_db()
        #########################################

    async def auth_middleware(self, request: Request, call_next):
        with next(get_db()) as database:
            if request.url.path.startswith("/app") and request.url.path not in [
                "/app/login",
                "/app/register",
            ]:
                session_token = request.cookies.get("session_token")
                if not session_token:
                    return RedirectResponse(url="/app/login")

                user = SessionToken.get_user_from_session(session_token, database)
                if not user:
                    return RedirectResponse(url="/app/login")

                request.state.user = user

            return await call_next(request)

    def get_caller_variable_name(self):
        """Find the name of the variable that called this function

        Returns:
            str: filename:variable_name.app
        """
        frame = inspect.currentframe().f_back.f_back
        fileName: str = frame.f_locals.get("__file__")[:-3]
        fileNameSplit = fileName.split("\\")
        variableName = None
        for name, value in frame.f_locals.items():
            if value is self:
                variableName = name
        return fileNameSplit[-1] + ":" + variableName + ".app"

    def run(self) -> None:
        """launches the server on the initialized host and port"""
        self._logger.info("Starting lab server...")
        app = self.get_caller_variable_name()
        uvicorn.run(app, host=self.host, port=self.port, workers=8)
