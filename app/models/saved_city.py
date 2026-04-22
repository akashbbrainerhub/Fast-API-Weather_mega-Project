from sqlalchemy import Column, Integer, ForeignKey, String
from app.db.base import Base
from uuid import uuid4
from sqlalchemy.orm import relationship

class SavedCity(Base):
    __tablename__ = "saved_cities"

    id = Column(String, default=lambda: str(uuid4()), primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    city_id = Column(String, ForeignKey("cities.id"))
    user = relationship("User", back_populates="saved_cities")
    city = relationship("City", back_populates="saved_by_users")
    