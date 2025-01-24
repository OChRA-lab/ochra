from fastapi import FastAPI, APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, Type
from pathlib import Path
from pathlib import PurePath
import shutil
from os import remove
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
        station_ip: str = "0.0.0.0",
        station_port: int = 8000,
    ):
        """initialize the station server

        Args:
            name (str): name of the station, used to identify and connect on the frontend
            location (Location): location of the station
            station_ip (str, optional): station ip to run the server on. Defaults to "127.0.0.1".
            station_port (int, optional): port to oopen the station on. Defaults to 8000.
        """
        self._name = name
        self._location = location
        self._ip = station_ip
        self.port = station_port
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
        self._router.add_api_route(
            "/process_station_op", self.process_station_op, methods=["POST"]
        )
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
        uvicorn.run(self._app, host=self._ip, port=self.port)

    @property
    def id(self):
        return self._station_proxy.id

    def _connect_to_lab(self, lab_ip: str):
        """connects to the lab server and creates a station model on the db

        Args:
            lab_ip (str): ip of the lab server connection.
        """
        self._lab_conn = LabConnection(lab_ip)
        return WorkStation(self._name, self._location, self.port)

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
            if self._station_proxy.locked is not None and self._station_proxy.locked != []:
                if str(op.caller_id) != self._station_proxy.locked:
                    raise HTTPException(403, detail="Station is locked by another user")

            device = self._devices[op.device_id]
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

            result_data = None
            data_file_name = ""
            error = ""
            data_type = ""
            data_status = -1
            try:
                result = method(**op.args)

                # checking if the result is bool
                # TODO: test this new method
                try:
                    result = Path(result)
                    success = True
                    result_data = None
                    data_status = -1
                    if (not result.is_file()) and (not result.is_dir()):
                        # raising an exception to exit the try loop
                        data_type = "string"
                        result_data = result
                        data_status = 1
                    elif result.is_file():
                        data_type = "file"
                        data_file_name = result.name
                    else:
                        data_type = "folder"
                        data_file_name = result.name + ".zip"
                except TypeError:
                    success = True
                    result_data = result
                    data_type = str(type(result))
                    data_status = 1

            except Exception as e:
                success = False
                error = str(e)
                raise Exception(e)

            finally:
                # update the operation_result to data server here
                operation_result = OperationResult(
                    success=success,
                    error=error,
                    result_data=result_data,
                    data_file_name=data_file_name,
                    data_type=data_type,
                    data_status=data_status,
                )

            if isinstance(result, PurePath):
                # if result is a directory, zip it up and convert to a file
                if result.is_dir():
                    result = shutil.make_archive(result.name, "zip", result.as_posix())
                    result = Path(result)

                # Do not make this an else or elif, this is code to upload all general files
                if result.is_file():
                    with open(str(result), "rb") as file:
                        result_data = {"file": file}

                        # upload the file as a property
                        self._lab_conn.put_data(
                            "operation_results",
                            id=operation_result.id,
                            result_data=result_data,
                        )

                        # change the data status to reflect success
                        self._lab_conn.set_property(
                            "operation_results",
                            operation_result.id,
                            "data_status",
                            1,
                        )

                    # remove the zip file when upload is done
                    if data_type == "folder":
                        remove(result.name)

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

    def process_station_op(self, op: Operation):
        if self._lab_conn:
            self._lab_conn.set_property(
                "operations",
                op.id,
                "start_timestamp",
                datetime.datetime.now().isoformat(),
            )
            # TODO change status to running

        result_data = None
        data_file_name = ""
        error = ""
        data_type = ""
        data_status = -1

        method = getattr(self._station_proxy, op.method)
        try:
            result = method(**op.args)
            try:
                result = Path(result)
                success = True
                result_data = None
                data_status = -1
                if (not result.is_file()) and (not result.is_dir()):
                    # raising an exception to exit the try loop
                    data_type = "string"
                    result_data = result
                    data_status = 1
                elif result.is_file():
                    data_type = "file"
                    data_file_name = result.name
                else:
                    data_type = "folder"
                    data_file_name = result.name + ".zip"
            except TypeError:
                success = True
                result_data = result
                data_type = str(type(result))
                data_status = 1
        except Exception as e:
            success = False
            error = str(e)
            raise Exception(e)

        finally:
            # update the operation_result to data server here
            operation_result = OperationResult(
                success=success,
                error=error,
                result_data=result_data,
                data_file_name=data_file_name,
                data_type=data_type,
                data_status=data_status,
            )
        
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
