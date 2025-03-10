from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from typing import Dict, Optional
from pathlib import Path, PurePath
import shutil
import traceback
from os import remove
import datetime
from starlette.types import Message
import uvicorn
import uvicorn.config

from ochra_common.connections.lab_connection import LabConnection
from ochra_common.utils.enum import (
    StationType,
    ActivityStatus,
    OperationStatus,
    ResultDataStatus,
    MobileRobotState,
)
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
        self._devices: dict[str, Device] = {}


    def setup(self, lab_ip: Optional[str] = None) -> None:
        """
        setup the station server and connect to the lab server if lab_ip is provided

        Args:
            lab_ip (str, optional): ip of the lab server connection. Defaults to None.
        """
        self._app = FastAPI()
        self._router = APIRouter()
        MODULE = Path(__file__).resolve().parent
        TEMPLATES = MODULE / "templates"


        self._app.get( "/process_device_op")(self.process_device_op)
        self._app.post( "/process_robot_op")(self.process_robot_op)
        self._app.get("/ping")(self.ping)

        self._app.get("/")(self.get_station)
        self._app.get("/devices")(self.get_station_devices)
        self._app.get("/devices/{device_id}")(self.get_device)
        self._app.post("/devices/{device_id}/commands")(self.perform_device_operation)

        self._app.get("/hypermedia")(self.get_pannel)
        self._app.get("/hypermedia/devices/{device_id}")(self.get_pannel_device)

        self._templates=Jinja2Templates(directory=TEMPLATES)
        self._station_proxy = self._connect_to_lab(lab_ip) if lab_ip else None

    def add_device(self, device):
        """
        add a device to the station dict

        Args:
            device (Device): device to add to the station
        """

        # TODO: str instead of pure uuid
        self._devices[str(device.id)] = device
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



    async def get_station(self, request: Request):
        return self._templates.TemplateResponse(
                "station.html",
                {
                    "request":request, 
                    "station_id": self.id, 
                    "station_name": self._name,
                }
        )

    async def get_station_devices(self, request: Request):
        return self._templates.TemplateResponse(
                "devices.html",
                {
                    "request":request, 
                    "station_id": self.id, 
                    "station_name": self._name,
                    "devices": [
                        {
                            "uri": f"/gateway/stations/{self.id}/devices/{d.id}", 
                            "name": d.name
                        }
                        for d in self._devices.values()
                    ]
                }
        )


    #######################################################
    #
    #
    #
    async def get_pannel(self, request: Request):
        return self._templates.TemplateResponse(
                "sidepanel_station.html",
                {
                    "request":request, 
                    "station": self, 
                }
        )


    async def get_pannel_device(self, request: Request, device_id: str):
        device: Optional[Device] = self._devices.get(device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device does not exist")

        return self._templates.TemplateResponse(
                "sidepanel_device.html",
                {
                    "request":request, 
                    "station": self, 
                    "device": device,
                    "device_html": device.to_html()
                }
        )
    #
    #
    #
    #
    #######################################################


    async def get_device(self, request: Request, device_id: str):
        device: Optional[Device] = self._devices.get(device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device does not exist")

        return self._templates.TemplateResponse(
                "device.html",
                {
                    "request":request, 
                    "station_id": self.id, 
                    "station_name": self._name,
                    "html_response": device.to_html()
                }
        )
    
    async def perform_device_operation(self, request: Request, device_id: str):
        form_data = await request.form()

        device: Optional[Device] = self._devices.get(device_id)
        if not device:
            raise HTTPException(status_code=404, detail=f"Device {device_id} does not exist",)

        command_name = form_data.get("command")
        if not isinstance(command_name, str):
            raise HTTPException(status_code=422, detail=f"Missing required parameter {command_name}")

        
        # Get the args and remove the command one
        args = form_data._dict
        args.pop("command")

        # check if the method is on the device if not raise an error
        method_exists = hasattr(device, command_name)
        if not method_exists:
            raise HTTPException(status_code=400, detail=f"Method does note xist")

        try:
            method = getattr(device, command_name)
            print(method)
            print(args)
            method(**args)
            return 
        except Exception as e:
            traceback.print_exception(e)
            raise HTTPException(status_code=500,detail="Unexpected error in running method")




    def ping(self):
        print("ping from station")

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

            # set device and station to busy
            device.status = ActivityStatus.BUSY
            self._station_proxy.status = ActivityStatus.BUSY

            # TODO crete an operation proxy to streamline setting properties
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
                result = method(**op.args)

                # checking if the result is bool
                # TODO: test this new method
                try:
                    #NOTE: WHAT IS GOING ON WITH THIS? WHY A PATH?
                    result = Path(result)
                    success = True
                    result_data = None
                    data_status = ResultDataStatus.UNAVAILABLE
                    if (not result.is_file()) and (not result.is_dir()):
                        # raising an exception to exit the try loop
                        data_type = "string"
                        result_data = result
                        data_status = ResultDataStatus.AVAILABLE
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
                    data_status = ResultDataStatus.AVAILABLE

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
                            ResultDataStatus.AVAILABLE,
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
                # change status to in progress
                self._lab_conn.set_property(
                    "operations",
                    op.id,
                    "status",
                    OperationStatus.COMPLETED,
                )

            # set device and station to busy
            device.status = ActivityStatus.IDLE
            self._station_proxy.status = ActivityStatus.IDLE

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

            if op.method not in robot.available_tasks and op.method != "go_to":
                raise HTTPException(404, detail=f"task {op.method} not found")

            # set device and station to busy
            robot.status = ActivityStatus.BUSY
            self._station_proxy.status = ActivityStatus.BUSY

            # TODO crete an operation proxy to streamline setting properties
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

            if op.method == "go_to":
                robot.state = MobileRobotState.NAVIGATING
                result = robot.go_to(op.args)
            else:
                if isinstance(robot, MobileRobot):
                    robot.state = MobileRobotState.MANIPULATING
                result = robot.execute(task_name=op.method, args=op.args)

            if self._lab_conn:
                self._lab_conn.set_property(
                    "operations",
                    op.id,
                    "end_timestamp",
                    datetime.datetime.now().isoformat(),
                )
                # change status to in progress
                self._lab_conn.set_property(
                    "operations",
                    op.id,
                    "status",
                    OperationStatus.COMPLETED,
                )

            # set device and station to busy
            robot.status = ActivityStatus.IDLE
            if isinstance(robot, MobileRobot):
                robot.state = MobileRobotState.AVAILABLE
            self._station_proxy.status = ActivityStatus.IDLE

            return result
        except Exception as e:
            raise HTTPException(500, detail=str(e))
