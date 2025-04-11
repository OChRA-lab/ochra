from fastapi import FastAPI, APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, Type
from pathlib import Path
from pathlib import PurePath
import shutil
from os import remove
import datetime
import uvicorn

from ochra_common.connections.lab_connection import LabConnection
from ochra_common.utils.enum import (
    StationType,
    ActivityStatus,
    OperationStatus,
    ResultDataStatus,
    MobileRobotState,
)
from ochra_common.utils.misc import is_path
from ochra_common.spaces.location import Location
from ochra_common.equipment.device import Device
from ochra_common.equipment.mobile_robot import MobileRobot
from ochra_common.equipment.operation import Operation
from ..proxy_models.equipment.operation_result import OperationResult
from ..proxy_models.space.station import Station


class operationExecute(BaseModel):
    operation: str
    deviceName: str
    args: Optional[Dict] = None


class StationServer:
    def __init__(
        self,
        name: str,
        location: Location,
        station_type: StationType,
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
        self._type = station_type
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
            "/process_op", self.process_op, methods=["POST"]
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
        return Station(self._name, self._type, self._location, self.port)

    def ping(self, request: Request):
        print(f"ping from {request.client.host}")

    def process_op(self, op: Operation):
        """process the operation based on the entity type

        Args:
            op (Operation): operation to be processed

        Raises:
            HTTPException: If the entity type is not found
        """
        try:
            if op.entity_type != "station":
                device = self._devices[op.entity_id]
                method = getattr(device, op.method)
            else:
                method = getattr(self._station_proxy, op.method)

            # set status to busy
            self._station_proxy.status = ActivityStatus.BUSY
            if op.entity_type != "station":
                device.status = ActivityStatus.BUSY
            self._station_proxy.add_operation(op)

            # set operation start timestamp and status
            if self._lab_conn:
                self._lab_conn.set_property(
                    "operations",
                    op.id,
                    "start_timestamp",
                    datetime.datetime.now().isoformat(),
                )
                # change status to in progress
                self._lab_conn.set_property(
                    "operations",
                    op.id,
                    "status",
                    OperationStatus.IN_PROGRESS,
                )

            result_data = None
            data_file_name = ""
            error = ""
            data_type = ""
            data_status = ResultDataStatus.UNAVAILABLE
           
            try:
                if op.entity_type == "robot":
                    if op.method == "execute":
                        task_name = op.args.pop("task_name")
                        if isinstance(device, MobileRobot):
                            device.state = MobileRobotState.MANIPULATING
                        result = method(task_name=task_name, args=op.args)
                    elif op.method == "go_to":
                        device.state = MobileRobotState.NAVIGATING
                        result = method(op.args)
                else:
                    result = method(**op.args)

                # process result
                if is_path(result):
                    result = Path(result)
                    success = True
                    result_data = None
                    data_status = ResultDataStatus.UNAVAILABLE
                    if result.is_file():
                        data_type = "file"
                        data_file_name = result.name
                    else:
                        data_type = "folder"
                        data_file_name = result.name + ".zip"
                else:
                    success = True
                    result_data = result
                    data_type = str(type(result))
                    data_status = ResultDataStatus.AVAILABLE

            except Exception as e:
                # set status to error
                self._station_proxy.status = ActivityStatus.ERROR
                if op.entity_type != "station":
                    device.status = ActivityStatus.ERROR

                success = False
                error = str(e)
                raise Exception(e)

            finally:
                # update the operation_result in the lab server
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
                    # change status to completed
                    self._lab_conn.set_property(
                        "operations",
                        op.id,
                        "status",
                        OperationStatus.COMPLETED,
                    )

            # set status to idle
            self._station_proxy.status = ActivityStatus.IDLE
            if op.entity_type != "station":
                device.status = ActivityStatus.IDLE
                if isinstance(device, MobileRobot):
                    device.state = MobileRobotState.AVAILABLE

            # upload result data if appropriate
            if isinstance(result, PurePath):
                self._upload_result_data(result, operation_result)

        except Exception as e:
            raise HTTPException(500, detail=str(e))

    def _upload_result_data(self, result: PurePath, operation_result: OperationResult):
        """upload the result data to the lab server

        Args:
            result (PurePath): path to the result data
            operation_result (OperationResult): operation result model
        """
        # TODO to deal with nonsequential data upload
        # if result is a directory, zip it up and convert to a file
        delete_archive = False
        if result.is_dir():
            result = shutil.make_archive(result.name, "zip", result.as_posix())
            result = Path(result)
            delete_archive = True

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
                    ResultDataStatus.AVAILABLE,
                )

            # remove the zip file when upload is done
            if delete_archive:
                remove(result.name)

