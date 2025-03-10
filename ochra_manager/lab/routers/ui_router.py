from datetime import datetime
import logging
import html
import uuid
from fastapi import APIRouter, Request, Response, status
from fastapi.templating import Jinja2Templates
from ochra_common.connections.api_models import ObjectConstructionRequest
from ochra_common.equipment.device import Operation
from ochra_common.utils.enum import OperationStatus

from ..lab_service import LabService
import httpx

logger = logging.getLogger(__name__)
STATIONS = "stations"


class WebAppRouter(APIRouter):
    def __init__(self, templates: Jinja2Templates):
        self.prefix = "/app"
        super().__init__(prefix=self.prefix)
        self.lab_service = LabService()
        self.templates = templates
        self.get("/")(self.index)
        self.get("/settings")(self.get_settings_page)
        self.get("/workflows")(self.get_workflows_page)

        self.get("/stations/{station_id}")(self.stationui)
        self.get("/stations/{station_id}/devices/{device_id}")(self.deviceui)
        self.post("/stations/{station_id}/devices/{device_id}/commands")(self.post_device_command)

    async def index(self, request:Request):
        stations = self.lab_service.get_all_objects(STATIONS)
        table_fields = [
                { 
                     "name": station["name"], 
                     "status": station["status"], 
                     "device_count": len(station["devices"]), 
                     "active_routine": "",
                     "station_id": station["id"]
                } 
                for station in stations
        ]
        
        return self.templates.TemplateResponse("stations.html",
                    {
                     "request":request, 
                     "active_link": self.prefix + "/", 
                     "table_fields": table_fields,
                     "sidepanel_view": False
                     })





    async def stationui(self, request:Request, station_id: str):
        s = self.lab_service.get_object_by_id(station_id, "stations")
        body = await request.body()
        headers = dict(request.headers)
        method = request.method
        url=f"http://{s["station_ip"]}:{s["port"]}/hypermedia"


        stations = self.lab_service.get_all_objects(STATIONS)
        table_fields = [
                { 
                     "name": station["name"], 
                     "status": station["status"], 
                     "device_count": len(station["devices"]), 
                     "active_routine": "",
                     "station_id": station["id"]
                } 
                for station in stations
        ]
        
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, data=body)
            decoded_html = response.content.decode("utf-8")
            return self.templates.TemplateResponse(
                "stations.html", 

                context={
                    "request": request, 
                    "active_link": self.prefix + "/", 
                    "table_fields": table_fields,
                    "station_html": decoded_html,
                    "sidepanel_view": True
                }
            )




    async def deviceui(self, request:Request, station_id: str, device_id: str):
        s = self.lab_service.get_object_by_id(station_id, "stations")
        body = await request.body()
        headers = dict(request.headers)
        method = request.method
        url=f"http://{s["station_ip"]}:{s["port"]}/hypermedia/devices/{device_id}"

        stations = self.lab_service.get_all_objects(STATIONS)
        table_fields = [
                { 
                     "name": station["name"], 
                     "status": station["status"], 
                     "device_count": len(station["devices"]), 
                     "active_routine": "",
                     "station_id": station["id"],
                } 
                for station in stations
        ]
        
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, data=body)
            decoded_html = response.content.decode("utf-8")
            return self.templates.TemplateResponse(
                "stations.html", 

                context={
                    "request": request, 
                    "active_link": self.prefix + "/", 
                    "table_fields": table_fields,
                    "station_html": decoded_html,
                    "sidepanel_view": True
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
                        "HX-Location": f"/app/stations/{station["id"]}/devices/{device_id}"
                    }
            )

        # 3. Propagate station errors
        return Response(
            content=station_response.content,
            status_code=station_response.status_code,
            headers=station_response.headers
        )




    async def get_settings_page(self, request:Request):
        return self.templates.TemplateResponse("settings.html",{"request":request, "active_link": self.prefix + "/settings"})

    async def get_workflows_page(self, request:Request):
        return self.templates.TemplateResponse("workflows.html",{"request":request, "active_link": self.prefix + "/workflows"})
