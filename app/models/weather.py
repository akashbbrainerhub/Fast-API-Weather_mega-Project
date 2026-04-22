from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from datetime import datetime
from app.db.base import Base
from uuid import uuid4
from sqlalchemy.orm import relationship

class Weather(Base):
    __tablename__ = "weather"

    id = Column(String, default=lambda: str(uuid4()), primary_key=True, index=True)
    city_id = Column(String, ForeignKey("cities.id"))
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    wind_speed = Column(Float)
    description = Column(String)

    fetched_at = Column(DateTime, default=datetime.utcnow)
    city = relationship("City", back_populates="weather_records")