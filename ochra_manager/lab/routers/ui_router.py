import logging
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from ..lab_service import LabService

logger = logging.getLogger(__name__)

class WebAppRouter(APIRouter):
    def __init__(self, templates: Jinja2Templates):
        self.prefix = "/app"
        super().__init__(prefix=self.prefix)
        self.lab_service = LabService()
        self.templates = templates
        self.get("/")(self.index)
        self.get("/stationui")(self.stationui)
        self.get("/settings")(self.get_settings_page)
        self.get("/workflows")(self.get_workflows_page)

    async def index(self, request:Request):
        return self.templates.TemplateResponse("stations.html",{"request":request, "active_link": self.prefix + "/"})

    async def stationui(self, request:Request):
        return self.templates.TemplateResponse("stationui.html",{"request":request, "active_link": self.prefix + "/station_ui"})

    async def get_settings_page(self, request:Request):
        return self.templates.TemplateResponse("settings.html",{"request":request, "active_link": self.prefix + "/settings"})

    async def get_workflows_page(self, request:Request):
        return self.templates.TemplateResponse("workflows.html",{"request":request, "active_link": self.prefix + "/workflows"})
