import hashlib
from pathlib import Path
from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .db import User, get_db, init_db, SessionToken

module_dir = Path(__file__).resolve().parent
static_directory = module_dir / "static"
template_directory = module_dir / "templates"

app=FastAPI()
app.mount("/static", StaticFiles(directory=static_directory), name="static")
templates=Jinja2Templates(directory=template_directory)


# ##########################################################################
# init_db()
#
# @app.middleware("http")
# async def auth_middleware(request: Request, call_next):
#     with next(get_db()) as database:
#         if request.url.path not in ['/login','/register'] and not request.url.path.startswith('/static'):
#             session_token = request.cookies.get('session_token')
#             if not session_token:
#                 return RedirectResponse(url='/login')
#
#             user = SessionToken.get_user_from_session(session_token, database)
#             if not user:
#                 return RedirectResponse(url='/login')
#
#             request.state.user = user
#         return await call_next(request)
#
#
# @app.get("/register", response_class=HTMLResponse)
# async def register_page(request: Request):
#     return templates.TemplateResponse(name="register.html", request=request, context={})
#
#
# @app.post("/register")
# async def register(username: str = Form(...), email: str = Form(...), password: str = Form(...), confirm: str = Form(...), db: Session = Depends(get_db)):
#     existing_user = User.fetch_user(db, username)
#     if existing_user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
#
#     if password != confirm:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords did not match")
#
#     hashed_password = hashlib.sha256(password.encode()).hexdigest()
#     new_user = User( username=username, password=hashed_password, email=email)
#
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#
#     response = JSONResponse({"message": "success"})
#     response.headers["HX-Location"] = "/"
#     return response
#
#
# @app.get("/login", response_class=HTMLResponse)
# async def login_page(request: Request):
#     return templates.TemplateResponse(name="login.html", request=request, context={})
#
# @app.post("/login")
# async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
#     user = User.authenticate_user(username, password, db)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
#
#     session_token = SessionToken.create_session_token(user.username, db)
#     response = JSONResponse({"message": "success"})
#     response.set_cookie(key="session_token", value=session_token, httponly=True)
#     response.headers["HX-Location"] = "/"
#     return response
#
#
# @app.post("/logout")
# async def logout(request: Request, db: Session = Depends(get_db)):
#     session = SessionToken.get_session(db, request.cookies["session_token"])
#     if session != None:
#         db.delete(session)
#         db.commit()
#         response = JSONResponse({"message": "logout successfull"})
#         response.headers["HX-Location"] = "/login"
#         return response
#
#     raise HTTPException(status_code=404, detail=f"User session {request.cookies["session_token"]} not found")
#
#
# ##########################################################################



@app.get("/")
async def index(request:Request):
    return templates.TemplateResponse("stations.html",{"request":request, "active_link": "/ui"})

@app.get("/stationui")
async def stationui(request:Request):
    return templates.TemplateResponse("stationui.html",{"request":request, "active_link": "/ui/station_ui"})

@app.get("/settings")
async def get_settings_page(request:Request):
    return templates.TemplateResponse("settings.html",{"request":request, "active_link": "/ui/settings"})

@app.get("/workflows")
async def get_workflows_page(request:Request):
    return templates.TemplateResponse("workflows.html",{"request":request, "active_link": "/ui/workflows"})
