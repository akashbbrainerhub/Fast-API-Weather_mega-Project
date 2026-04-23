from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import decode_token


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        db = SessionLocal()

        response = await call_next(request)

        if request.url.path == "/login":
            auth_header = request.headers.get("Authorization")

            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                payload = decode_token(token)

                if payload:
                    user_id = payload.get("user_id")

                    user = db.query(User).filter(User.id == user_id).first()
                    if user:
                        user.last_login = datetime.utcnow()
                        db.commit()

        db.close()
        return response