from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id"),
        index=True,
    )

    slot_id: Mapped[int] = mapped_column(
        ForeignKey("availability_slots.id"),
        unique=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )