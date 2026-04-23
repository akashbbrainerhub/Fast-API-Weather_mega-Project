from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session
# from app.api.V1.dependencies.rbac import require_role
from app.core.exceptions import BadRequestException
from app.core.exceptions import BadRequestException
from app.models import user
from app.models import user
from app.core.security import decode_token
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.services.auth_service import regsiter_user, authenticate_user, login_user
from app.api.V1.dependencies.db import get_db
from app.core.exceptions import BadRequestException

router = APIRouter(prefix="/auth", tags=["Auth"])


def _extract_token(raw_value: str | None) -> str | None:
    if not raw_value:
        return None

    value = raw_value.strip()
    lower_value = value.lower()

    if lower_value.startswith("bearer "):
        return value[7:].strip()

    if lower_value.startswith("bearer"):
        return value[6:].strip()

    return value

def get_current_user(
    authorization: str | None = Header(default=None, alias="Authorization"),
    auth: str | None = Header(default=None, alias="auth"),
    token: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    token_value = _extract_token(authorization) or _extract_token(auth) or _extract_token(token)

    if not token_value:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    payload = decode_token(token_value)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("user_id")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise BadRequestException("Invalid email or password")

    return user


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db),):
    try:
        user = regsiter_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(
    user_login: UserLogin,
    db: Session = Depends(get_db)
):
    try:
        user = authenticate_user(db, user_login)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = login_user(user)

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role.value
    }
