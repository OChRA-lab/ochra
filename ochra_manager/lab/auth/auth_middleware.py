from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .auth import SessionToken, get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException

class UserSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session_token = request.cookies.get("session_token")

        if session_token:
            try:
                db: Session = next(get_db())  # Ensure proper DB connection handling
                session = SessionToken.get_session(db, session_token)
                if session and session.user:
                    request.state.user = session.user
                else:
                    # Handle case where session is invalid or expired
                    raise HTTPException(status_code=401, detail="Invalid session or session expired")
            except Exception as e:
                # Log the error and handle database issues or invalid session errors
                raise HTTPException(status_code=500, detail="Error retrieving session: " + str(e))

        response = await call_next(request)
        return response