from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.V1.dependencies.db import get_db
from app.api.V1.dependencies.rbac import require_role
from app.core.response import success_response
from app.core.security import hash_password
from app.models.activity import Activity
from app.models.user import User, UserRole
from app.schemas.user import AdminManagedUserCreate
from sqlalchemy import String, func
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    admin = Depends(require_role(UserRole.ADMIN))
):
    users = db.query(User).all()

    return [
        {
            "id": str(u.id),
            "name": u.name,
            "email": u.email,
            "role": u.role.value,
            "last_login": u.last_login
        }
        for u in users
    ]
    
@router.get("/activities")
def get_activities(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    action: str = None,
    user_id: str = None,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
    user = Depends(require_role(UserRole.ADMIN, UserRole.ANALYST))
):
    query = db.query(Activity)

    if action:
        query = query.filter(Activity.action == action)

    if user_id:
        query = query.filter(Activity.user_id == user_id)

    if start_date:
        query = query.filter(
            Activity.created_at >= datetime.fromisoformat(start_date)
        )

    if end_date:
        query = query.filter(
            Activity.created_at <= datetime.fromisoformat(end_date)
        )

    total = query.count()
    activities = (
        query
        .order_by(Activity.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    data = [
        {
            "id": str(a.id),
            "user_id": str(a.user_id),
            "action": a.action,
            "metadata": a.activity_metadata,
            "ip": a.ip_address,
            "created_at": a.created_at
        }
        for a in activities
    ]

    return success_response({
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": data
    })


@router.get("/analytics/top-cities")
def top_cities(
    db: Session = Depends(get_db),
    admin = Depends(require_role(UserRole.ADMIN))
):
    result = (
        db.query(
            Activity.activity_metadata["city"].cast(String).label("city"),
            func.count().label("count")
        )
        .filter(Activity.action == "SEARCH_CITY")
        .group_by(Activity.activity_metadata["city"].cast(String))
        .order_by(func.count().desc())
        .all()
    )

    return [
        {
            "city": r.city,
            "search_count": r.count
        }
        for r in result
    ]


@router.post("/users")
def create_managed_user(
    payload: AdminManagedUserCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_role(UserRole.ADMIN))
):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=payload.name,
        email=payload.email,
        password=hash_password(payload.password),
        role=UserRole(payload.role)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return success_response(
        {
            "id": str(new_user.id),
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role.value,
        },
        message="User created successfully"
    )


@router.delete("/users/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin=Depends(require_role(UserRole.ADMIN))
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role not in (UserRole.ANALYST, UserRole.MODERATOR):
        raise HTTPException(
            status_code=403,
            detail="Only analyst and moderator users can be deleted with this endpoint"
        )

    db.delete(user)
    db.commit()

    return success_response({"message": "User deleted successfully"})