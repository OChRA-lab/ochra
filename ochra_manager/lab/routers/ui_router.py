from datetime import datetime
import hashlib
import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, context

import httpx
import re
import ast

from ochra_common.connections.api_models import ObjectConstructionRequest
from ochra_common.equipment.device import Operation
from ochra_common.utils.enum import OperationStatus

from ochra_manager.lab.auth.auth import SessionToken, User, get_db
from ..lab_service import LabService

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

    def isHXRequest(self, request: Request) -> bool:
        return request.headers.get("HX-Request") == "true"
    
    def build_table_fields(self) -> list[dict]:
        stations = self.lab_service.get_all_objects(STATIONS)
        return [{
            "name": s["name"],
            "status": s["status"],
            "device_count": len(s["devices"]),
            "active_routine": "",
            "station_id": s["id"]
        } for s in stations]
    async def get_stations(self, request:Request):
        table_fields = self.build_table_fields()
        
        return self.templates.TemplateResponse("zzzstations.html",
                    {
                     "request":request, 
                     "active_link": self.prefix + "/", 
                     "table_fields": table_fields,
                     "sidepanel_view": False
                     })

    async def get_register(self, request: Request):
        return self.templates.TemplateResponse(name="zregister.html", request=request, context={})

    async def post_register(self, username: str = Form(...), email: str = Form(...), password: str = Form(...), confirm: str = Form(...), db: Session = Depends(get_db)):
        if password != confirm:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords did not match")
        
        existing_user = User.fetch_user(db, username)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
        
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
        response.set_cookie(key="session_token", value=session_token, httponly=True, secure=True)
        response.headers["HX-Location"] = "/app"
        return response

    async def post_logout(self, request: Request, db: Session = Depends(get_db)):
        session_token = request.cookies.get("session_token")
        if not session_token:
            raise HTTPException(status_code=401, detail="No session token found")

        session = SessionToken.get_session(db, session_token)
        if session != None:
            db.delete(session)
            db.commit()
            response = JSONResponse({"message": "logout successfull"})
            response.headers["HX-Location"] = "/app/login"
            return response

        raise HTTPException(status_code=404, detail=f"User session {request.cookies['session_token']} not found")

    async def get_station(self, request:Request, station_id: str):
        s = self.lab_service.get_object_by_id(station_id, "stations")
        body = await request.body()
        headers = dict(request.headers)
        method = request.method
        url=f"http://{s['station_ip']}:{s['port']}/hypermedia"


        stations = self.lab_service.get_all_objects(STATIONS)
        table_fields = self.build_table_fields()
        
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
        url=f"http://{s['station_ip']}:{s['port']}/hypermedia/devices/{device_id}"
        station_url=f"http://{s['station_ip']}:{s['port']}/hypermedia"
        stations = self.lab_service.get_all_objects(STATIONS)
        station = self.lab_service.get_object_by_id(station_id, "stations")
        table_fields = self.build_table_fields()

        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, data=body)
            decoded_html = response.content.decode("utf-8")

            station_response = await client.request(method, station_url, headers=headers, data=body)
            decoded_station_html = station_response.content.decode("utf-8")
            
            if self.isHXRequest(request):
                return HTMLResponse(content=decoded_html)
            else:
                return self.templates.TemplateResponse(
                    "zzzdevice.html", 

                    context={
                        "request": request, 
                        "active_link": self.prefix + "/", 
                        "table_fields": table_fields,
                        "device_html": decoded_html,
                        "station_html": decoded_station_html,
                        "station_id": station_id,
                        "station_name": station["name"],
                    }
                )

    async def post_command(self, request: Request, station_id: str, device_id: str):
        station = self.lab_service.get_object_by_id(station_id, "stations")
        proxy_url = f"http://{station['station_ip']}:{station['port']}/devices/{device_id}/commands"
        form = await request.form()

        args_raw = form.get("args", "").strip()

        def sanitize_dict_string(s: str) -> str:
            # Quote unquoted keys
            s = re.sub(r'([{,]\s*)(\w+)\s*:', r'\1"\2":', s)
            # Quote unquoted string values (words that are not True/False/None/numbers)
            s = re.sub(r':\s*([a-zA-Z_]\w*)\s*([,}])', r':"\1"\2', s)
            return s
        
        def convert_colon_string_to_dict(s: str) -> dict:
            result = {}
            if not s:
                return result
            try:
                for pair in s.split(","):
                    if not pair.strip():
                        continue
                    if ":" not in pair:
                        raise ValueError(f"Invalid key:value pair: {pair}")
                    key, value = map(str.strip, pair.split(":", 1))
                    if value.isdigit():
                        value = int(value)
                    else:
                        try:
                            value = float(value)
                        except ValueError:
                            value = value.strip('"').strip("'")
                    result[key] = value
                return result
            except Exception as e:
                raise ValueError(f"Failed to convert string to dict: {e}")
                    
        try:
            if args_raw == "":
                args_dict = {}
            else:
                try:
                    # Ensure keys in the args are quoted properly
                    # Use ast.literal_eval to safely parse Python-like string
                    args_dict = ast.literal_eval(args_raw)
                except (ValueError, SyntaxError, NameError):
                    try:
                        quoted = sanitize_dict_string(args_raw)
                        args_dict = ast.literal_eval(quoted)
                    except Exception:
                        args_dict = convert_colon_string_to_dict(args_raw)
                
            if not isinstance(args_dict, dict):
                raise ValueError("Parsed args is not a dictionary.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid args format: {e}")
        
        opp = Operation(
            caller_id=str(uuid.uuid4()),
            collection="operations",
            entity_id=device_id,
            entity_type="devices",
            method=str(form.get("task_name", "")),
            args=args_dict,
            status = OperationStatus.CREATED,
            start_timestamp = datetime.now(),
        )

        async with httpx.AsyncClient() as client:
            headers = {
                key: value for key, value in request.headers.items()
                if key.lower() not in ("content-length", "content-type")
            }

            station_response = await client.post(
                proxy_url,
                headers = headers,
                data=form
            )

        if station_response.is_success:
            opp.end_timestamp = datetime.now()

            self.lab_service.construct_object(
                    ObjectConstructionRequest(object_json=opp.model_dump_json()),
                    opp.collection
            )

            async with httpx.AsyncClient() as client:
                headers = {
                    key: value for key, value in request.headers.items()
                    if key.lower() not in ("content-length", "content-type")
                }

                # re-fetch the updated device HTML
                refreshed_device_html = await client.get(
                    f"http://{station['station_ip']}:{station['port']}/hypermedia/devices/{device_id}",
                    headers=headers
                )

            decoded_html = refreshed_device_html.content.decode("utf-8")
            return self.templates.TemplateResponse(
                "zzzdevice.html",
                context={
                    "request": request,
                    "active_link": self.prefix + "/",
                    "device_html": decoded_html,
                    "decoded_html": decoded_html,
                    "station_id": station_id,
                    "station_name": station["name"],
                }
            )

        # 3. Propagate station errors
        return Response(
            content=station_response.content,
            status_code=station_response.status_code,
            headers=station_response.headers,
            
        )
    async def get_device_view(self, request: Request, station_id: str, device_id: str):
        s = self.lab_service.get_object_by_id(station_id, "stations")
        body = await request.body()
        headers = dict(request.headers)
        method = request.method
        url=f"http://{s['station_ip']}:{s['port']}/hypermedia/devices/{device_id}"
        print(station_id)
        station = self.lab_service.get_object_by_id(station_id, "stations")

        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, data=body)
            decoded_html = response.content.decode("utf-8")
            print(station_id)

            if self.isHXRequest(request):
                return HTMLResponse(content=decoded_html)
            else:
                return self.templates.TemplateResponse(
                    "zzzdevice.html", 
                    context={
                        "request": request, 
                        "active_link": self.prefix + "/", 
                        "device_html": decoded_html,
                        "station_id": station_id,
                        "station_name": station["name"],
                    }
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

        if not hasattr(request.state, "user"):
            raise HTTPException(401, detail="Unauthorized")
        
        user: Optional[User] = User.fetch_user(db, request.state.user.username)
        user.username = username
        user.email = email

        db.commit()
        request.state.user = user

        return self.templates.TemplateResponse("zzzsettings.html",{"request":request, "active_link": self.prefix + "/settings", "edit": False})

    async def get_workflows(self, request:Request):
        return self.templates.TemplateResponse("zzzworkflows.html",{"request":request, "active_link": self.prefix + "/workflows"})
