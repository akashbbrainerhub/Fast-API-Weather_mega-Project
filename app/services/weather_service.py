import requests
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.weather import Weather
from app.core.config import settings

CACHE_TIME = 30  # minutes


def get_weather(db: Session, city):
    weather = (
        db.query(Weather)
        .filter(Weather.city_id == city.id)
        .order_by(Weather.fetched_at.desc())
        .first()
    )

    if weather and (datetime.utcnow() - weather.fetched_at) < timedelta(minutes=CACHE_TIME):
        return weather
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={settings.WEATHER_API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    new_weather = Weather(
        city_id=city.id,
        temperature=data["main"]["temp"],
        humidity=data["main"]["humidity"],
        pressure=data["main"]["pressure"],
        wind_speed=data["wind"]["speed"],
        description=data["weather"][0]["description"]
    )

    db.add(new_weather)
    db.commit()
    db.refresh(new_weather)

    return new_weather