import logging
from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse



from pydantic import BaseModel
from typing import Dict, Optional, Any
from pathlib import Path, PurePath
import shutil
from os import remove
import datetime
import uvicorn
import os
import signal

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
from .station_logging import configure_station_logging, configure_device_logger

import ast
from jinja2 import Environment, FileSystemLoader
from fastapi.staticfiles import StaticFiles



def _is_path(obj: Any) -> bool:
    """Check if an object is a path.
    Args:
        obj (Any): The object to check.
    Returns:
        bool: True if the object is a path, False otherwise.
    """
    try:
        path = Path(obj)
        return path.exists()
    except (TypeError, ValueError):
        return False

#TODO what is the point of this class
class operationExecute(BaseModel):
    operation: str
    deviceName: str
    args: Optional[Dict] = None


class StationServer:
    """
    A class to represent the station server.
    """

    def __init__(
        self,
        name: str,
        location: Location,
        station_type: StationType,
        logging_path: str = ".",
        station_ip: str = "0.0.0.0",
        station_port: int = 8000,
    ):
        """
        Initialize the StationServer instance.

        Args:
            name (str): Unique name of the station for identification and frontend connection.
            location (Location): Physical or logical location of the station.
            station_type (StationType): Type of the station.
            logging_path (str, optional): Directory path for logging. Defaults to current directory.
            station_ip (str, optional): IP address to bind the server. Defaults to "0.0.0.0".
            station_port (int, optional): Port to run the server on. Defaults to 8000.
        """
        self._logging_path = Path(logging_path).resolve()
        
        configure_station_logging(log_root_path=self._logging_path)
        self._logger = logging.getLogger(__name__)

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

        station_templates = Path(__file__).resolve().parent / "templates"
        lab_templates = Path(__file__).resolve().parents[1] / "lab" / "templates"

        env = Environment(
            loader=FileSystemLoader([str(station_templates), str(lab_templates)])
        )
        self._templates = Jinja2Templates(env=env)

        lab_static = Path(__file__).resolve().parents[1] / "lab" / "static"
        self._app.mount(
            "/static", StaticFiles(directory=str(lab_static)), name="static"
        )

        self._router.add_api_route("/process_op", self.process_op, methods=["POST"])
        self._router.add_api_route("/ping", self.ping, methods=["GET"])

        # TODO: Look into the manual adding of routes in fastapi
        # self._router.add_route("/ui", self.station_ui, methods=["GET"] )

        self._app.include_router(self._router)

        self._app.get("/ping")(self.ping)
        self._app.get("/")(self.get_station)
        self._app.get("/devices")(self.get_station_devices)
        self._app.get("/devices/{device_id}")(self.get_device)
        self._app.post("/devices/{device_id}/commands")(self.perform_device_operation)

        self._app.get("/hypermedia")(self.get_pannel)

        self._app.get("/hypermedia/devices/{device_id}")(self.get_device_view)

        self._app.post("/shutdown")(self.shutdown)

        self._station_proxy = self._connect_to_lab(lab_ip) if lab_ip else None

    def add_device(self, device: Device) -> None:
        """
        add a device to the station dict

        Args:
            device (Device): device to add to the station
        """

        # TODO: str instead of pure uuid
        configure_device_logger(
            log_root_path=self._logging_path,
            device_module_path=device.__module__,
            device_name=device.name,
        )
        self._devices[str(device.id)] = device
        if self._station_proxy:
            self._station_proxy.add_device(device)

    def run(self):
        """
        start the server
        """
        self._logger.info(f"Starting station server {self._name} on {self._ip}:{self.port}")
        uvicorn.run(self._app, host=self._ip, port=self.port)

    @property
    def id(self):
        return self._station_proxy.id

    def _connect_to_lab(self, lab_ip: str) -> Station:
        """connects to the lab server and creates a station model on the db

        Args:
            lab_ip (str): ip of the lab server connection.
        """
        self._lab_conn = LabConnection(lab_ip)
        return Station(self._name, self._type, self._location, self.port)

    async def get_station(self, request: Request) -> HTMLResponse:
        """
        get the station html page
        
        Args:
            request (Request): fastapi request object

        Returns:
            HTMLResponse: the station html page
        """
        return self._templates.TemplateResponse(
            "station.html",
            {
                "request": request,
                "station_id": self.id,
                "station_name": self._name,
            },
        )

    async def get_station_devices(self, request: Request) -> HTMLResponse:
        """
        get the station devices html page
        
        Args:
            request (Request): fastapi request object

        Returns:
            HTMLResponse: the station devices html page
        """
        return self._templates.TemplateResponse(
            "devices.html",
            {
                "request": request,
                "station_id": self.id,
                "station_name": self._name,
                "devices": [
                    {
                        "uri": f"/gateway/stations/{self.id}/devices/{d.id}",
                        "name": d.name,
                    }
                    for d in self._devices.values()
                ],
            },
        )

    #######################################################
    #
    #
    #
    async def get_pannel(self, request: Request) -> HTMLResponse:
        """
        get the station side pannel html page

        Args:
            request (Request): fastapi request object

        Returns:
            HTMLResponse: the station side pannel html page
        """
        return self._templates.TemplateResponse(
            "sidepanel_station.html",
            {
                "request": request,
                "station": self,
            },
        )

    async def get_device_view(self, request: Request, device_id: str) -> HTMLResponse:
        """
        get the device view html page

        Args:
            request (Request): fastapi request object
            device_id (str): id of the device to get the view for

        Returns:
            HTMLResponse: the device view html page
        """
        device: Optional[Device] = self._devices.get(device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device does not exist")

        sidepanel = await self.get_pannel(request)
        sidepanel_html = sidepanel.body.decode("utf-8")

        return self._templates.TemplateResponse(
            "device_view.html",
            {
                "request": request,
                "station": self,
                "device": device,
                "device_html": device.to_html(),
                "station_html": sidepanel_html,
                "sidepanel_view": True,
            },
        )

    async def get_device(self, request: Request, device_id: str) -> HTMLResponse:
        """
        get the device html page

        Args:
            request (Request): fastapi request object
            device_id (str): id of the device to get the view for

        Returns:
            HTMLResponse: the device html page
        """
        device: Optional[Device] = self._devices.get(device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device does not exist")

        return self._templates.TemplateResponse(
            "device.html",
            {
                "request": request,
                "station_id": self.id,
                "station_name": self._name,
                "html_response": device.to_html(),
            },
        )

    async def perform_device_operation(self, request: Request, device_id: str) -> None:
        """
        perform a device operation from the UI

        Args:
            request (Request): fastapi request object
            device_id (str): id of the device to perform the operation on

        """
        form_data = await request.form()

        device: Optional[Device] = self._devices.get(device_id)
        if not device:
            raise HTTPException(
                status_code=404,
                detail=f"Device {device_id} does not exist",
            )

        command_name = form_data.get("command")
        if not isinstance(command_name, str):
            raise HTTPException(
                status_code=422, detail=f"Missing required parameter {command_name}"
            )

        # Get the args and remove the command one
        args = form_data._dict
        args.pop("command")

        # check if the method is on the device if not raise an error
        method_exists = hasattr(device, command_name)
        if not method_exists:
            raise HTTPException(status_code=400, detail="Method does note xist")

        if args.get("args") == "":
            args["args"] = {}
        # Only convert if it's a string
        if isinstance(args.get("args"), str):
            try:
                args["args"] = ast.literal_eval(args["args"])
            except (ValueError, SyntaxError):
                raise ValueError("Invalid dictionary string in args['args']")

        try:
            method = getattr(device, command_name)
            self._logger.debug(f"Calling method {command_name} on device {device_id} with args: {args}")
            method(**args)
            return
        except Exception as e:
            self._logger.error(f"Error occurred while calling method {command_name} on device {device_id}: {e}")
            raise HTTPException(
                status_code=500, detail="Unexpected error in running method"
            )

    def ping(self):
        self._logger.info("ping from station")

    def process_op(self, op: Operation) -> None:
        """
        Processes an operation by retrieving the target device or station and executing the specified method.

        Args:
            op (Operation): The operation to be processed.

        Raises:
            HTTPException: If the entity type or device is not found, or if the station is locked by another user.
        """
        try:
            # check if the station is not locked
            if (
                self._station_proxy.locked is not None
                and self._station_proxy.locked != []
            ):
                if str(op.caller_id) != self._station_proxy.locked:
                    raise HTTPException(403, detail="Station is locked by another user")

            if op.entity_type != "station":
                device = self._devices[str(op.entity_id)]
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
                # set appropriate state for mobile robot
                if op.entity_type == "robot" and isinstance(device, MobileRobot):
                    if op.method == "execute":
                        device.state = MobileRobotState.MANIPULATING
                    elif op.method == "go_to":
                        device.state = MobileRobotState.NAVIGATING

                result = method(**op.args)

                # process result
                if _is_path(result):
                    result = Path(result)
                    success = True
                    result_data = None
                    data_status = ResultDataStatus.UNAVAILABLE
                    if result.is_file():
                        data_type = "file"
                        data_file_name = f"{op.caller_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{result.name}"
                    else:
                        data_type = "folder"
                        data_file_name = f"{op.caller_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{result.name}.zip"
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

    def _upload_result_data(self, result: PurePath, operation_result: OperationResult) -> None:
        """
        Uploads result data (file or directory) to the lab server.

        Args:
            result (PurePath): Path to the result data (file or directory).
            operation_result (OperationResult): Operation result model instance.
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

    def shutdown(self) -> int:
        """
        Shutdown the station server and remove its entry from the lab server.

        Returns:
            int: HTTP status code indicating success (200).
        """
        self._logger.info("Shutting down station server...")
        for _, device in self._devices.items():
            if device.inventory != [] or device.inventory is None:
                device.inventory._cleanup()
            device._cleanup()
        self._station_proxy.inventory._cleanup()
        self._station_proxy._cleanup()
        os.kill(os.getpid(), signal.SIGTERM)
        return 200
        # shutdown the server
