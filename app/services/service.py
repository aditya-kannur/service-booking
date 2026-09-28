from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate


def create_service(
    db: Session,
    provider_id: int,
    data: ServiceCreate,
) -> Service:
    service = Service(
        provider_id=provider_id,
        name=data.name,
        description=data.description,
        duration_minutes=data.duration_minutes,
        price=data.price,
    )

    db.add(service)
    db.commit()
    db.refresh(service)

    return service


def get_service(
    db: Session,
    service_id: int,
) -> Service:
    service = db.get(Service, service_id)

    if service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )

    return service


def list_services(
    db: Session,
    provider_id: int | None = None,
) -> list[Service]:
    query = select(Service).order_by(Service.id)

    if provider_id is not None:
        query = query.where(
            Service.provider_id == provider_id
        )

    return list(db.scalars(query).all())


def update_service(
    db: Session,
    service: Service,
    data: ServiceUpdate,
) -> Service:
    update_data = data.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():
        setattr(service, field, value)

    db.commit()
    db.refresh(service)

    return service


def delete_service(
    db: Session,
    service: Service,
) -> None:
    db.delete(service)
    db.commit()