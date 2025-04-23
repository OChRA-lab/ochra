from datetime import datetime
import hashlib
import logging
from typing import Optional
import uuid
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from ochra_common.connections.api_models import ObjectConstructionRequest
from ochra_common.equipment.device import Operation
from ochra_common.utils.enum import OperationStatus
from sqlalchemy.orm import Session, context

from ochra_manager.lab.auth.auth import SessionToken, User, get_db

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


        self.get("/")(self.get_stations)

        self.get("/register")(self.get_register)
        self.post("/register")(self.post_register)

        self.get("/login")(self.get_login)
        self.post("/login")(self.post_login)

        self.post("/logout")(self.post_logout)

        self.get("/settings")(self.get_settings)
        self.put("/settings")(self.put_settings)

        self.get("/workflows")(self.get_workflows)

        self.get("/stations")(self.get_stations)
        self.get("/stations/{station_id}")(self.get_station)
        self.get("/stations/{station_id}/devices/{device_id}")(self.get_device)
        self.post("/stations/{station_id}/devices/{device_id}/commands")(self.post_command)




    async def get_stations(self, request:Request):
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
        
        return self.templates.TemplateResponse("zzzstations.html",
                    {
                     "request":request, 
                     "active_link": self.prefix + "/", 
                     "table_fields": table_fields,
                     "sidepanel_view": False
                     })

    def isHXRequest(self, request: Request) -> bool:
        return request.headers.get("HX-Request") == "true"

    async def get_register(self, request: Request):
        return self.templates.TemplateResponse(name="zregister.html", request=request, context={})

    async def post_register(self, username: str = Form(...), email: str = Form(...), password: str = Form(...), confirm: str = Form(...), db: Session = Depends(get_db)):
        existing_user = User.fetch_user(db, username)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

        if password != confirm:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords did not match")

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        new_user = User( username=username, password=hashed_password, email=email)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        response = JSONResponse({"message": "success"})
        response.headers["HX-Location"] = "/app"
        return response


    async def get_login(self, request: Request):
        return self.templates.TemplateResponse(name="zlogin.html", request=request, context={})


    async def post_login(self, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
        user = User.authenticate_user(username, password, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

        session_token = SessionToken.create_session_token(user.username, db)
        response = JSONResponse({"message": "success"})
        response.set_cookie(key="session_token", value=session_token, httponly=True)
        response.headers["HX-Location"] = "/app"
        return response




    async def post_logout(self, request: Request, db: Session = Depends(get_db)):
        session = SessionToken.get_session(db, request.cookies["session_token"])
        if session != None:
            db.delete(session)
            db.commit()
            response = JSONResponse({"message": "logout successfull"})
            response.headers["HX-Location"] = "/app/login"
            return response

        raise HTTPException(status_code=404, detail=f"User session {request.cookies["session_token"]} not found")



    async def get_station(self, request:Request, station_id: str):
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

            if self.isHXRequest(request):
                return HTMLResponse(content=decoded_html)
            else:
                return self.templates.TemplateResponse(
                    "zzzstations.html", 

                    context={
                        "request": request, 
                        "active_link": self.prefix + "/", 
                        "table_fields": table_fields,
                        "station_html": decoded_html,
                        "sidepanel_view": True
                    }
                )


    async def get_device(self, request:Request, station_id: str, device_id: str):
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
            if self.isHXRequest(request):
                return HTMLResponse(content=decoded_html)
            else:
                return self.templates.TemplateResponse(
                    "zzzstations.html", 

                    context={
                        "request": request, 
                        "active_link": self.prefix + "/", 
                        "table_fields": table_fields,
                        "station_html": decoded_html,
                        "sidepanel_view": True
                    }
                )


    async def post_command(self, request: Request, station_id: str, device_id: str):
        station = self.lab_service.get_object_by_id(station_id, "stations")
        proxy_url = f"http://{station['station_ip']}:{station['port']}/devices/{device_id}/commands"
        form = await request.form()

        opp = Operation(
            caller_id=uuid.uuid4(),
            collection="operations",
            entity_id=device_id,
            entity_type="devices",
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




    async def get_settings(self, request:Request, edit: bool = False):
        return self.templates.TemplateResponse(
                "zzzsettings.html",
                {
                    "request":request, 
                    "active_link": self.prefix + "/settings", 
                    "edit": edit
                }
            )

    async def put_settings(self, request:Request, username: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
        user: Optional[User] = User.fetch_user(db, request.state.user.username)

        if not user:
            HTTPException(status_code=404, detail=f"User not found")
        else:
            user.username = username
            user.email = email

        db.commit()
        request.state.user = user

        return self.templates.TemplateResponse("zzzsettings.html",{"request":request, "active_link": self.prefix + "/settings", "edit": False})



    async def get_workflows(self, request:Request):
        return self.templates.TemplateResponse("zzzworkflows.html",{"request":request, "active_link": self.prefix + "/workflows"})
