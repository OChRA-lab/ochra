from fastapi import FastAPI
import uvicorn
import logging
import inspect
from .routers import operation_results_router

logger = logging.getLogger(__name__)


class DataServer:
    def __init__(self, host: str, port: int, folderpath: str = None) -> None:
        """Setup a data server with the given host and port optionally storing data in folderpath

        Args:
            host (str): host ip address
            port (int): port to open the server on
            folderpath (str): path to store data in
        """
        self.host = host
        self.port = port
        self.app = FastAPI()

        self.app.include_router(operation_results_router(folderpath))

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
        """launches the server on the initialized host and port
        """        
        logger.info("started server")
        app = self.get_caller_variable_name()
        uvicorn.run(app, host=self.host, port=self.port, workers=8)
