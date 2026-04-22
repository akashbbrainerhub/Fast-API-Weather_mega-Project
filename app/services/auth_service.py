from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserCreate , UserLogin ,UserResponse
from app.models.user import UserRole , User
from datetime import datetime

def regsiter_user(db: Session, user_create: UserCreate) -> UserResponse:
    existing_user = db.query(User).filter(User.email == user_create.email).first()
    if existing_user:
        raise ValueError("Email already registered")

    hashed_password = hash_password(user_create.password)

    new_user = User(
        name=user_create.name,
        email=user_create.email,
        password=hashed_password,
        role=UserRole.USER
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse.from_orm(new_user)

def authenticate_user(db: Session, user_login: UserLogin) -> User:
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user:
        raise ValueError("Invalid email or password")

    if not verify_password(user_login.password, user.password):
        raise ValueError("Invalid email or password")

    user.last_login = datetime.utcnow()
    db.commit()

    return user

def login_user(user: User):
    token = create_access_token({
        "user_id": str(user.id),
        "role": user.role.value
    })

    return token