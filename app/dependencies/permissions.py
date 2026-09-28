from collections.abc import Callable

from fastapi import HTTPException, status

from app.db.models.user import User


ADMIN = "admin"
PROVIDER = "provider"
CUSTOMER = "customer"


def check_role(user: User, allowed_roles: set[str]) -> None:
    if user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action",
        )


def require_roles(*allowed_roles: str) -> Callable:
    allowed = set(allowed_roles)

    def dependency(user: User):
        check_role(user, allowed)
        return user

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