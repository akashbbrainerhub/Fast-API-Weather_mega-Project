from sqlalchemy.orm import Session
from app.models.saved_city import SavedCity
from app.models.city import City


def save_city(db: Session, user_id, city: City):
    existing = (
        db.query(SavedCity)
        .filter(
            SavedCity.user_id == user_id,
            SavedCity.city_id == city.id
        )
        .first()
    )
    if existing:
        return existing

    saved = SavedCity(user_id=user_id, city_id=city.id)
    db.add(saved)
    db.commit()
    db.refresh(saved)
    return saved


def get_saved_cities(db: Session, user_id):
    return (
        db.query(SavedCity)
        .filter(SavedCity.user_id == user_id)
        .all()
    )


def delete_saved_city(db: Session, user_id, saved_city_id):
    saved = (
        db.query(SavedCity)
        .filter(SavedCity.id == saved_city_id)
        .first()
    )

    if not saved:
        return None

    if str(saved.user_id) != str(user_id):
        return "FORBIDDEN"

    db.delete(saved)
    db.commit()
    return True