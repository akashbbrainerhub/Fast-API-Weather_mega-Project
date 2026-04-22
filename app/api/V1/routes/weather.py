from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.api.V1.dependencies.db import get_db
from app.api.V1.dependencies.auth import get_current_user
from app.services.city_service import get_or_create_city
from app.services.weather_service import get_weather
from app.services.activity_service import log_activity

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/search")
def search_city(
    city: str,
    country: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    city_obj = get_or_create_city(db, city, country)
    weather = get_weather(db, city_obj)
    log_activity(
        db=db,
        user_id=current_user.id,
        action="SEARCH_CITY",
        metadata={"city": city, "country": country},
        ip=request.client.host
    )

    return {
        "city": city_obj.name,
        "temperature": weather.temperature,
        "humidity": weather.humidity,
        "pressure": weather.pressure,
        "wind_speed": weather.wind_speed,
        "description": weather.description
    }