from datetime import datetime, timedelta
from app.models.activity import Activity
from app.models.user import UserRole

def can_access_user_data(current_user, target_user_id: int):
    if current_user.role.value == "admin":
        return True

    return current_user.id == target_user_id

def can_delete_saved_city(current_user, saved_city):
    if current_user.role.value == "admin":
        return True
    return str(saved_city.user_id) == str(current_user.id)

def can_search_city(db, user):
    # admin has no limit
    if user.role == UserRole.ADMIN:
        return True

    # premium user → higher limit
    limit = 100 if user.role == UserRole.PREMIUM_USER else 20

    today = datetime.utcnow().date()

    count = db.query(Activity).filter(
        Activity.user_id == user.id,
        Activity.action == "SEARCH_CITY",
        Activity.created_at >= today
    ).count()

    return count < limit