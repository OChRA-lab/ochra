from fastapi import FastAPI, APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, Type
import uvicorn
import uvicorn.config

from ochra_common.connections.lab_connection import LabConnection
from ochra_common.spaces.location import Location
from ochra_common.equipment.device import Device
from ochra_common.equipment.operation import Operation
from .work_station import WorkStation



class operationExecute(BaseModel):
    operation: str
    deviceName: str
    args: Optional[Dict] = None

class StationServer():
    def __init__(self, name: str, location: Location, station_ip: str="127.0.0.1", station_port: int = 8000):
        self._name = name
        self._location = location
        self._ip = station_ip
        self._port = station_port
        self._devices = {}

    def setup(self, lab_ip: str = None) -> None:
        """
        setup the station server and connect to the lab server if lab_ip is provided
        
        Args:
            lab_ip (str, optional): ip of the lab server connection. Defaults to None.
        """
        
        self._app = FastAPI()
        self._router = APIRouter()
        
        self._router.add_api_route(
            "/process_op", self.process_op, methods=["POST"])
        self._router.add_api_route("/ping", self.ping, methods=["GET"])
        self._app.include_router(self._router)
        
        self._station_proxy = self._connect_to_lab(lab_ip) if lab_ip else None

    def add_device(self, device: Type[Device]):
        """
        add a device to the station dict
        
        Args:
            device (Device): device to add to the station
        """
        self._devices[device.id] = device
        if self._station_proxy:
            print(f"/////////////adding device {device}")
            self._station_proxy.add_device(device)
        

    def run(self):
        """
        start the server
        """
        uvicorn.run(self._app, host=self._ip, port=self._port)

    def _connect_to_lab(self, lab_ip: str):
        """connects to the lab server and creates a station model on the db

        Args:
            lab_ip (str): ip of the lab server connection.
        """
        self._lab_conn = LabConnection(lab_ip)
        return WorkStation(self._name, self._location)

    def ping(self, request: Request):
        print(f"ping from {request.client.host}")

    def process_op(self, op: Operation):
        """retrieve the device from the device dict and execute the method

        Args:
            op (Operation): operation details to be executed on the device

        Raises:
            HTTPException: If the device is not found or the method is not found

        Returns:
            Any: return value of the method
        """
        try:
            # need to add star timestamp to the operation
            device = self._devices[op.caller_id]
            method = getattr(device, op.method)
            return method(**op.args)
        except Exception as e:
            raise HTTPException(500, detail=str(e))
