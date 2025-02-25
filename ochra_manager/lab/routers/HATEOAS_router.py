import logging
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
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
 
    async def get_lab(self, request: Request):
        return self.templates.TemplateResponse("/hypermedia/lab.html",{"request": request, "lab_uri": self.lab_uri})


    async def get_lab_stations(self, request: Request):
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
        s = self.lab_service.get_object_by_id(station_id, "stations")
        headers = dict(request.headers)
        form_data = await request.form()
        url = f"http://{s['station_ip']}:{s['port']}/devices/{device_id}/commands"

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=form_data)
            
        if response.status_code == 200:
            return RedirectResponse(
                url=f"/gateway/stations/{station_id}/devices/{device_id}",
                status_code=303
            )
        else:
            raise HTTPException(status_code=response.status_code)

