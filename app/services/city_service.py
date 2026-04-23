from app.models.city import City
from sqlalchemy.orm import Session

from app.services.activity_service import log_activity

def get_or_create_city(db: Session, city_name: str, country: str, user_id: int):
    city_name = city_name.strip()
    country = country.strip()
    city = db.query(City).filter(City.name == city_name).first()

    if city:
        if city.country != country:
            city.country = country
            db.commit()
            db.refresh(city)
        return city

    city = City(name=city_name, country=country)
    db.add(city)
    db.commit()
    db.refresh(city)
    log_activity(
        db=db,
        user_id=user_id,
        action="SAVE_CITY",
        metadata={
            "city_id": city.id,
            "city_name": city.name,
            "country": city.country
        }
    )
    return city