from fastapi import FastAPI, APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, Type
from os.path import exists as is_file
import datetime
import uvicorn
import uvicorn.config

from ochra_common.connections.lab_connection import LabConnection
from ochra_common.spaces.location import Location
from ochra_common.equipment.device import Device
from ochra_common.equipment.operation import Operation
from ochra_manager.equipment.operation_result import OperationResult
from .work_station import WorkStation


class operationExecute(BaseModel):
    operation: str
    deviceName: str
    args: Optional[Dict] = None


class StationServer:
    def __init__(
        self,
        name: str,
        location: Location,
        station_ip: str = "127.0.0.1",
        station_port: int = 8000,
    ):
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
            "/process_device_op", self.process_device_op, methods=["POST"]
        )
        self._router.add_api_route(
            "/process_robot_op", self.process_robot_op, methods=["POST"]
        )
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
            self._station_proxy.add_device(device)

    def run(self):
        """
        start the server
        """
        uvicorn.run(self._app, host=self._ip, port=self._port)

    @property
    def id(self):
        return self._station_proxy.id

    def _connect_to_lab(self, lab_ip: str):
        """connects to the lab server and creates a station model on the db

        Args:
            lab_ip (str): ip of the lab server connection.
        """
        self._lab_conn = LabConnection(lab_ip)
        return WorkStation(self._name, self._location)

    def ping(self, request: Request):
        print(f"ping from {request.client.host}")

    def process_device_op(self, op: Operation):
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

            # TODO crete an operation proxy to streamline setting properties
            if self._lab_conn:
                self._lab_conn.set_property(
                    "operations",
                    op.id,
                    "start_timestamp",
                    datetime.datetime.now().isoformat(),
                )
                # TODO change status to running

            result = method(**op.args)

            data = None
            data_file_name = ""
            error = ""
            # checking if the result is bool
            if isinstance(result, bool):
                success = result
                data_type = "bool"
            elif not is_file(str(result)):
                success = True
                data = result
                data_type = str(type(result))
            else:
                success = True
                data_type = ""
                data = None
                # storing the file name for both linux and windows filesystems
                file = result.split("\\")[-1]
                data_file_name = file.split("\/")[-1]

            # update the operation_result to data server here
            operation_result = OperationResult(
                success=success,
                error=error,
                data=data,
                data_file_name=data_file_name,
                data_type=data_type,
            )

            if is_file(str(result)):
                with open(str(result), "rb") as file:
                    data = {"file": file}

                    # upload the file as a property
                    self._lab_conn.put_data(
                        "operation_results", id=operation_result.id, data=data
                    )

                # TODO to deal with nonsequential data upload

            if self._lab_conn:
                self._lab_conn.set_property(
                    "operations",
                    op.id,
                    "end_timestamp",
                    datetime.datetime.now().isoformat(),
                )
                self._lab_conn.set_property(
                    "operations",
                    op.id,
                    "result",
                    operation_result.id,
                )
                # TODO change status to complete

        except Exception as e:
            raise HTTPException(500, detail=str(e))

    def process_robot_op(self, op: Operation):
        """retrieve the robot from the device dict and execute the given task

        Args:
            op (Operation): operation details to be executed by the robot

        Raises:
            HTTPException: If the device is not found or the method is not found

        Returns:
            Any: return value of the method
        """
        try:
            # need to add star timestamp to the operation
            robot = self._devices[op.caller_id]

            if op.method not in robot.available_tasks:
                raise HTTPException(404, detail=f"task {op.method} not found")

            # TODO crete an operation proxy to streamline setting properties
            if self._lab_conn:
                self._lab_conn.set_property(
                    "operations",
                    op.id,
                    "start_timestamp",
                    datetime.datetime.now().isoformat(),
                )
                # TODO change status to running

            result = robot.execute(task_name=op.method, args=op.args)

            if self._lab_conn:
                self._lab_conn.set_property(
                    "operations",
                    op.id,
                    "end_timestamp",
                    datetime.datetime.now().isoformat(),
                )
                # TODO change status to complete

            return result
        except Exception as e:
            raise HTTPException(500, detail=str(e))
