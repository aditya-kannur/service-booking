from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.dependencies.auth import get_db, get_current_user
from app.dependencies.permissions import (
    ADMIN,
    PROVIDER,
    check_owner_or_admin,
    require_roles,
)
from app.schemas.service import (
    ServiceCreate,
    ServiceResponse,
    ServiceUpdate,
)
from app.services.service import (
    create_service,
    delete_service,
    get_service,
    list_services,
    update_service,
)


router = APIRouter(
    prefix="/services",
    tags=["Services"],
)


@router.post(
    "",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: ServiceCreate,
    current_user: User = Depends(
        require_roles(PROVIDER, ADMIN)
    ),
    db: Session = Depends(get_db),
):
    provider_id = current_user.id

    return create_service(
        db=db,
        provider_id=provider_id,
        data=data,
    )


@router.get(
    "",
    response_model=list[ServiceResponse],
)
def list_all(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role == PROVIDER:
        return list_services(
            db,
            provider_id=current_user.id,
        )

    return list_services(db)


@router.get(
    "/{service_id}",
    response_model=ServiceResponse,
)
def get_one(
    service_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = get_service(db, service_id)

    return service


@router.patch(
    "/{service_id}",
    response_model=ServiceResponse,
)
def update(
    service_id: int,
    data: ServiceUpdate,
    current_user: User = Depends(
        require_roles(PROVIDER, ADMIN)
    ),
    db: Session = Depends(get_db),
):
    service = get_service(db, service_id)

    check_owner_or_admin(
        current_user=current_user,
        owner_id=service.provider_id,
    )

    return update_service(
        db=db,
        service=service,
        data=data,
    )


@router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    service_id: int,
    current_user: User = Depends(
        require_roles(PROVIDER, ADMIN)
    ),
    db: Session = Depends(get_db),
):
    service = get_service(db, service_id)

    check_owner_or_admin(
        current_user=current_user,
        owner_id=service.provider_id,
    )

    delete_service(
        db=db,
        service=service,
    )

    return None