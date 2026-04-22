from pydantic import BaseModel
from uuid import UUID


class SavedCityResponse(BaseModel):
    id: UUID
    city_name: str

    class Config:
        from_attributes = True