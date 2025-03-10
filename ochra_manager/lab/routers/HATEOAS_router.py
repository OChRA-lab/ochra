from datetime import datetime
import logging
import uuid
from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from ochra_common.connections.api_models import ObjectConstructionRequest
from ochra_common.equipment.operation import Operation
from ochra_common.utils.enum import OperationStatus
from ..lab_service import LabService
import httpx

logger = logging.getLogger(__name__)


class HATEOASRouter(APIRouter):
    def __init__(self, templates: Jinja2Templates, lab_uri: str):
        prefix = "/gateway"
        super().__init__(prefix=prefix)
        self.lab_service = LabService()
        self.lab_uri = lab_uri
        self.templates = templates
        self.get("/")(self.get_lab)
        self.get("/stations")(self.get_lab_stations)
        self.get("/stations/{station_id}")(self.get_station)
        self.get("/stations/{station_id}/devices")(self.get_station_devices)
        self.get("/stations/{station_id}/devices/{device_id}")(self.get_device)
        self.post("/stations/{station_id}/devices/{device_id}/commands")(self.post_device_command)
        self.get("/operations")(self.get_operation_audits)
        self.get("/operations/{operation_id}")(self.get_operation_audit)
 
    async def get_lab(self, request: Request):
        return self.templates.TemplateResponse("/hypermedia/lab.html",{"request": request, "lab_uri": self.lab_uri})


    async def get_lab_stations(self, request: Request):
        """
        Fetch a list of all the station from the database and list them
        """
        stations = self.lab_service.get_all_objects("stations")
        stations = [
                {
                    "name": s["name"], 
                    "uri": f"/gateway/stations/{s['id']}"
                } 
                for s in self.lab_service.get_all_objects("stations")
        ]

        return self.templates.TemplateResponse(
                "/hypermedia/stations.html",
                {
                    "request":request,
                    "lab_uri": self.lab_uri, 
                    "stations": stations
                }
            )


    async def get_station(self, request: Request, station_id: str):
        """
        Get a specific station by its ID from the database
        This will proxy the station view from the station server itself
        """
        s = self.lab_service.get_object_by_id(station_id, "stations")
        body = await request.body()
        headers = dict(request.headers)
        method = request.method
        url = f"http://{s['station_ip']}:{s['port']}/"

        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, data=body)
            decoded_html = response.content.decode("utf-8")
            return self.templates.TemplateResponse(
                    "/hypermedia/station.html", 
                    {
                        "request":request,
                        "html_response": decoded_html,
                    }
                )

    async def get_station_devices(self, request: Request, station_id: str):
        """
        Get a list of all the curretly connected devices to the station
        This will proxy the devices view from the station itself. This way it always represents the devices in the station
        """
        s = self.lab_service.get_object_by_id(station_id, "stations")
        body = await request.body()
        headers = dict(request.headers)
        method = request.method
        url = f"http://{s['station_ip']}:{s['port']}/devices"

        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, data=body)
            decoded_html = response.content.decode("utf-8")
            return self.templates.TemplateResponse(
                    "/hypermedia/devices.html", 
                    {
                        "request":request,
                        "html_response": decoded_html,
                    }
                )

    async def get_device(self, request: Request, station_id: str, device_id: str):
        """
        Get a specific device from a station
        This will proxy the device view from the station itself. 
        """
        s = self.lab_service.get_object_by_id(station_id, "stations")
        body = await request.body()
        headers = dict(request.headers)
        method = request.method
        url = f"http://{s['station_ip']}:{s['port']}/devices/{device_id}"

        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, data=body)
            decoded_html = response.content.decode("utf-8")
            return self.templates.TemplateResponse(
                    "/hypermedia/device.html", 
                    {
                        "request":request,
                        "html_response": decoded_html,
                    }
                )


    async def post_device_command(self, request: Request, station_id: str, device_id: str):
        """
        This posts a command to a device through a proxy post to the station
        """
        station = self.lab_service.get_object_by_id(station_id, "stations")
        proxy_url = f"http://{station['station_ip']}:{station['port']}/devices/{device_id}/commands"
        form = await request.form()

        opp = Operation(
            caller_id=uuid.uuid4(),
            collection="operations",
            method=str(""),
            args={},
            status = OperationStatus.CREATED,
            start_timestamp = datetime.now(),
        )

        async with httpx.AsyncClient() as client:
            station_response = await client.post(
                proxy_url,
                headers = dict(request.headers),
                data=form
            )

        if station_response.is_success:
            opp.end_timestamp = datetime.now()

            self.lab_service.construct_object(
                    ObjectConstructionRequest(object_json=opp.model_dump_json()),
                    opp.collection
            )

            return Response(
                    status_code=status.HTTP_202_ACCEPTED,
                    headers={
                        "Location": f"/gateway/operations/{opp.id}",
                        "HX-Location": f"/gateway/operations/{opp.id}"
                    }
            )

        # 3. Propagate station errors
        return Response(
            content=station_response.content,
            status_code=station_response.status_code,
            headers=station_response.headers
        )



    async def get_operation_audits(self, request: Request):
        #TODO: Add html return
        return self.lab_service.get_all_objects("operations")


    async def get_operation_audit(self, request: Request, operation_id: str):
        #TODO: Add html return
        opp = self.lab_service.get_object_by_id(operation_id, "operations")
        print(opp)
        return opp

