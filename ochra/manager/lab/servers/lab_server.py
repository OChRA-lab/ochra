from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional, Callable
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import logging
from ochra_manager.lab.auth.auth import SessionToken, get_db, init_user_db
from ochra_manager.lab.routers.ui_router import WebAppRouter
from ..routers.device_router import DeviceRouter
from ..routers.station_router import StationRouter
from ..routers.robot_router import RobotRouter
from ..routers.operation_router import OperationRouter
from ..routers.lab_router import LabRouter
from ..routers.storage_router import StorageRouter
from ..routers.operation_results_router import OperationResultRouter
from ..utils.scheduler import Scheduler
from ..utils.lab_logging import configure_lab_logging
import inspect


class LabServer:
    """
    A class to represent the lab server.
    """
    def __init__(
        self,
        host: str,
        port: int,
        folderpath: str,
        template_path: Optional[Path] = None,
    ) -> None:
        """
        Initialize the LabServer instance.

        Args:
            host (str): The IP address to bind the server to.
            port (int): The port number to listen on.
            folderpath (str): Directory path for storing lab data and logs.
            template_path (Path, optional): Optional path for Jinja2 templates and static files. Default is None.
        """
        MODULE_DIRECTORY = (
            Path(__file__).resolve().parent if not template_path else template_path
        )

        configure_lab_logging(log_root_path=folderpath)

        self._logger = logging.getLogger(__name__)
        self._logger.info("Initializing lab server...")
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

    async def auth_middleware(self, request: Request, call_next: Callable):
        """
        Middleware to handle authentication for the web app.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): Function to call the next middleware or route handler.
        """
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
        """
        launches the server on the initialized host and port
        """
        self._logger.info("Starting lab server...")
        app = self.get_caller_variable_name()
        uvicorn.run(app, host=self.host, port=self.port, workers=8)
