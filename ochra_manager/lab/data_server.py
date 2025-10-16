from fastapi import FastAPI
import uvicorn
import inspect
from .routers import operation_results_router


class DataServer:
    """
    A class to represent the data server to handle results data.
    """
    def __init__(
        self,
        host: str,
        port: int,
        folderpath: str = None,
    ) -> None:
        """
        Initializes the DataServer instance.

        Args:
            host (str): The IP address to bind the server.
            port (int): The port number to listen on.
            folderpath (str, optional): Directory path for storing data. Defaults to None.
        """
        self._logger = logging.getLogger(__name__)
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
        """
        launches the server on the initialized host and port
        """
        self._logger.info("Starting data server...")
        app = self.get_caller_variable_name()
        uvicorn.run(app, host=self.host, port=self.port, workers=8)
