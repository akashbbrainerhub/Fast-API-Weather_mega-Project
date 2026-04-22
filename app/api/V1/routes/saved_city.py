from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.V1.dependencies.db import get_db
from app.api.V1.dependencies.auth import get_current_user
from app.models import saved_city
from app.services.city_service import get_or_create_city
from app.services.saved_city_service import (
    save_city,
    get_saved_cities,
    delete_saved_city
)
from app.models.saved_city import SavedCity

router = APIRouter(prefix="/saved-cities", tags=["Saved Cities"])

@router.post("/")
def save_city_api(
    city: str,
    country: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    city_obj = get_or_create_city(db, city, country)
    saved = save_city(db, current_user.id, city_obj)

    return {
        "message": "City saved",
        "city": city_obj.name,
        "id": saved.id
    }

@router.get("/")
def get_saved_cities_api(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    saved_list = get_saved_cities(db, current_user.id)

    return [
        {
            "id": s.id,
            "city": s.city.name
        }
        for s in saved_list
    ]

@router.delete("/{saved_city_id}")
def delete_saved_city_api(
    saved_city_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = delete_saved_city(db, current_user.id, saved_city_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Not found")

    if result == "FORBIDDEN":
        raise HTTPException(status_code=403, detail="Not allowed")

    return {"message": "Deleted successfully"}