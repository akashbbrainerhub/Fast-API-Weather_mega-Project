from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestException
from app.models import user
from app.core.security import decode_token
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.services.auth_service import regsiter_user, authenticate_user, login_user
from app.api.V1.dependencies.db import get_db

security = HTTPBearer()

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token_value = credentials.credentials

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
