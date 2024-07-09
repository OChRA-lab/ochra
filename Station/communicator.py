from fastapi import FastAPI, APIRouter, Request, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any, Optional
from OChRA_Common.connections.db_connection import DbConnection
from OChRA_Common.connections.lab_connection import LabConnection
from OChRA_Common.operations import *


class operationExecute(BaseModel):
    operation: str
    deviceName: str
    args: Optional[Dict] = None


class Communicator:
    def __init__(self,
                 dbip="138.253.124.144:27017",
                 host_ip="0.0.0.0",
                 port=8000,
                 lab_ip="10.24.169.42") -> None:
        self.lab_conn: LabConnection = LabConnection(lab_ip)
        self.app = FastAPI()
        self.router = APIRouter()
        self.host_ip = host_ip
        self.port = port
        self.devices = []
        self.router.add_api_route(
            "/process_op", self.process_operation, methods=["POST"])
        self.router.add_api_route("/ping", self.ping, methods=["GET"])
        self.app.include_router(self.router)
        self.db_conn = DbConnection(dbip)

    def run(self):
        self.start_up()
        uvicorn.run(self.app, host=self.host_ip, port=self.port)

    def ping(self, request: Request):
        clientHost = request.client.host
        print(clientHost)
        return

    def start_up(self):
        station_id = self.lab_conn.create_station()
        for device in self.devices:
            device_dict: dict = device.__dict__
            keys_to_pop = []
            for key in device_dict.keys():
                if key[0] =="_":
                    keys_to_pop.append(key)
            [device_dict.pop(key) for key in keys_to_pop]
            self.lab_conn.construct_object(
                device.__class__, "devices",
                station_conn=station_id, **device_dict)

    def process_operation(self, args: operationExecute):
        try:
            for i in self.devices:
                if i.name == args.deviceName:
                    op = eval(f"{args.operation}()")
                    return i.execute(op, **args.args)
        except Exception as e:
            raise HTTPException(500, detail=str(e))
