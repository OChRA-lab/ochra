import logging
import html
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from ..lab_service import LabService
from requests import get

logger = logging.getLogger(__name__)
STATIONS = "stations"


class WebAppRouter(APIRouter):
    def __init__(self, templates: Jinja2Templates):
        self.prefix = "/app"
        super().__init__(prefix=self.prefix)
        self.lab_service = LabService()
        self.templates = templates
        self.get("/")(self.index)
        self.get("/station/{station_id}")(self.stationui)
        self.get("/settings")(self.get_settings_page)
        self.get("/workflows")(self.get_workflows_page)

    async def index(self, request:Request):
        stations = self.lab_service.get_all_objects(STATIONS)
        table_fields = [
                { 
                     "name": station["name"], 
                     "status": station["status"], 
                     "device_count": len(station["devices"]), 
                     "active_routine": "",
                     "station_id": "/app/station/"+station["id"]
                } 
                for station in stations
        ]
        
        return self.templates.TemplateResponse("stations.html",{"request":request, "active_link": self.prefix + "/", "table_fields": table_fields})

    async def stationui(self, request:Request, station_id: str):
        station = self.lab_service.get_object_by_id(station_id, STATIONS)
        response = get(url=f"http://{station["station_ip"]}:{station["port"]}/hypermedia_interface")
        return self.templates.TemplateResponse("station_page.html", context={"request": request, "html_response": response.text})

    async def get_settings_page(self, request:Request):
        return self.templates.TemplateResponse("settings.html",{"request":request, "active_link": self.prefix + "/settings"})

    async def get_workflows_page(self, request:Request):
        return self.templates.TemplateResponse("workflows.html",{"request":request, "active_link": self.prefix + "/workflows"})
