from uuid import uuid4

from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
import enum
from app.db.base import Base
from sqlalchemy.orm import relationship


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    ANALYST = "analyst"
    MODERATOR = "moderator"
    PREMIUM_USER = "premium_user"


class User(Base):
    __tablename__ = "users"

    id = Column(String, default=lambda: str(uuid4()), primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    activities = relationship("Activity", back_populates="user")
    saved_cities = relationship("SavedCity", back_populates="user")