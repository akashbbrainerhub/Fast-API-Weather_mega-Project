from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, String
from datetime import datetime

from app.api.V1.dependencies.db import get_db
from app.api.V1.dependencies.rbac import require_role
from app.models.activity import Activity
from app.models.user import UserRole
from app.core.response import success_response

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/activities")
def get_activities(
    limit: int = Query(10),
    offset: int = Query(0),
    action: str = None,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
    user = Depends(require_role(UserRole.ADMIN, UserRole.ANALYST))
):
    query = db.query(Activity)

    if action:
        query = query.filter(Activity.action == action)

    if start_date:
        query = query.filter(Activity.created_at >= datetime.fromisoformat(start_date))

    if end_date:
        query = query.filter(Activity.created_at <= datetime.fromisoformat(end_date))

    total = query.count()

    activities = (
        query
        .order_by(Activity.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return success_response({
        "total": total,
        "items": [
            {
                "action": a.action,
                "metadata": a.activity_metadata,
                "time": a.created_at
            }
            for a in activities
        ]
    })
@router.get("/top-cities")
def top_cities(
    limit: int = Query(5),
    db: Session = Depends(get_db),
    user = Depends(require_role(UserRole.ADMIN, UserRole.ANALYST))
):
    city_field = Activity.activity_metadata["city"].cast(String)

    result = (
        db.query(
            city_field.label("city"),
            func.count().label("count")
        )
        .filter(Activity.action == "SEARCH_CITY")
        .group_by(city_field)
        .order_by(func.count().desc())
        .limit(limit)
        .all()
    )

    return success_response([
        {"city": r.city, "count": r.count}
        for r in result
    ])