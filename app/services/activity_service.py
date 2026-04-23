from sqlalchemy.orm import Session
from app.models.activity import Activity


def log_activity(db, user_id, action, metadata=None, ip=None):
    activity = Activity(
        user_id=user_id,
        action=action,
        activity_metadata=metadata,
        ip_address=ip
    )

    db.add(activity)
    db.commit()