from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .auth import SessionToken, get_db  # your existing code

class UserSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session_token = request.cookies.get("session_token")

        if session_token:
            db = next(get_db())
            session = SessionToken.get_session(db, session_token)
            if session and session.user:
                request.state.user = session.user

        response = await call_next(request)
        return response
