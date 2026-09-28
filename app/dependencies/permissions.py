from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.db.models.user import User
from app.dependencies.auth import get_current_user


ADMIN = "admin"
PROVIDER = "provider"
CUSTOMER = "customer"


def require_roles(*allowed_roles: str) -> Callable:
    allowed = set(allowed_roles)

    def dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        return current_user

    return dependency


def check_owner_or_admin(
    current_user: User,
    owner_id: int,
) -> None:
    if current_user.role == ADMIN:
        return

    if current_user.id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )