from fastapi import Depends, HTTPException
from app.api.V1.dependencies.auth import get_current_user
from app.models.user import UserRole


def require_role(*roles):
    def checker(current_user = Depends(get_current_user)):
        allowed_roles = [
            role.value if isinstance(role, UserRole) else role
            for role in roles
        ]

        if current_user.role.value not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user
    return checker