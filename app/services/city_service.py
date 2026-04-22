from app.models.city import City
from sqlalchemy.orm import Session

def get_or_create_city(db: Session, city_name: str, country: str):
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

    return city