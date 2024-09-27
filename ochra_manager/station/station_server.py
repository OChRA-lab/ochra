from fastapi import FastAPI, APIRouter, Request, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any, Optional

import uvicorn.config
from ..connections.db_connection import DbConnection
from ochra_common.connections.lab_connection import LabConnection
from abc import ABC, abstractmethod
import threading
import time
import contextlib


class operationExecute(BaseModel):
    operation: str
    deviceName: str
    args: Optional[Dict] = None

class StationServer():
    def setup_server(self,
                     dbip="138.253.124.144:27017",
                     host_ip="0.0.0.0",
                     port=8000,
                     lab_ip="10.24.169.42") -> None:
        self._lab_ip = lab_ip
        self._db_ip = dbip
        self._app = FastAPI()
        self._router = APIRouter()
        self._host_ip = host_ip
        self._port = port
        self._devices = []
        self._router.add_api_route(
            "/process_op", self.process_operation, methods=["POST"])
        self._router.add_api_route("/ping", self.ping, methods=["GET"])
        self._app.include_router(self._router)
        self._start_up()

    def run(self):
        """start the communicator server

        Args:
            offline (bool, optional): if true start the station in offline mode. Defaults to False.
        """
        uvicorn.run(self._app, host=self._host_ip, port=self._port)

    def ping(self, request: Request):
        clientHost = request.client.host
        print(clientHost)
        return

    def _start_up(self):
        """Setups the lab and db connections

        Args:
            offline (bool): offline mode
        """
        self._lab_conn = LabConnection(self._lab_ip)
        self._station_id = self._lab_conn.construct_object(
            type="stations", object=self)


    def process_operation(self, args: operationExecute):
        """search the devices for a device with the given name and execute the method provided in the args

        Args:
            args (operationExecute): args.operation is the method to execute, args.deviceName is the device to execute the method on, args.args are the arguments to pass to the method

        Raises:
            HTTPException: If the device is not found or the method is not found

        Returns:
            Any: return value of the method
        """
        try:
            for i in self._devices:
                if i.name == args.deviceName:
                    method = getattr(i, args.operation)
                    return method(**args.args)
            raise Exception("Device not found")
        except Exception as e:
            raise HTTPException(500, detail=str(e))
