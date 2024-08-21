from fastapi import FastAPI, APIRouter, Request, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any, Optional
from ochra_common.connections.db_connection import DbConnection
from ochra_common.connections.lab_connection import LabConnection
from abc import ABC, abstractmethod
from ochra_common.utils.db_decorator import Offline


class operationExecute(BaseModel):
    operation: str
    deviceName: str
    args: Optional[Dict] = None


class Communicator(ABC):
    def __init__(self,
                 dbip="138.253.124.144:27017",
                 host_ip="0.0.0.0",
                 port=8000,
                 lab_ip="10.24.169.42") -> None:
        self.lab_ip = lab_ip
        self.db_ip = dbip
        self.app = FastAPI()
        self.router = APIRouter()
        self.host_ip = host_ip
        self.port = port
        self.devices = []
        self.router.add_api_route(
            "/process_op", self.process_operation, methods=["POST"])
        self.router.add_api_route("/ping", self.ping, methods=["GET"])
        self.app.include_router(self.router)

    def run(self, offline=False):
        self._start_up(offline)
        self.setup()
        uvicorn.run(self.app, host=self.host_ip, port=self.port)

    def ping(self, request: Request):
        clientHost = request.client.host
        print(clientHost)
        return

    @abstractmethod
    def setup(self):
        pass

    def _start_up(self, offline):
        if not offline:
            self.lab_conn = LabConnection(self.lab_ip)
            self.db_conn = DbConnection(self.db_ip)
            self.station_id = self.lab_conn.create_station()
        else:
            self.offline = Offline(True)
            self.station_id = None

    def process_operation(self, args: operationExecute):
        try:
            for i in self.devices:
                if i.name == args.deviceName:
                    method = getattr(i, args.operation)
                    return method(**args.args)
        except Exception as e:
            raise HTTPException(500, detail=str(e))
