from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from uuid import uuid4
from datetime import datetime
from app.db.base import Base
from sqlalchemy.orm import relationship

class City(Base):
    __tablename__ = "cities"

    id = Column(String, default=lambda: str(uuid4()), primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    country = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    weather_records = relationship("Weather", back_populates="city")
    saved_by_users = relationship("SavedCity", back_populates="city")