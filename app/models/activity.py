from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from uuid import uuid4
from datetime import datetime
from app.db.base import Base
from sqlalchemy.orm import relationship

class Activity(Base):
    __tablename__ = "activities"

    id = Column(String, default=lambda: str(uuid4()), primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    action = Column(String, nullable=False)
    activity_metadata = Column(JSON, nullable=True)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="activities")