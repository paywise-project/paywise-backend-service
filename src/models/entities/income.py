import uuid
from datetime import datetime
from typing import Optional

from archipy.models.entities import UpdatableDeletableEntity
from sqlalchemy import Column, ForeignKey, Boolean, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship, Synonym


class IncomeEntity(UpdatableDeletableEntity):
    __tablename__ = "incomes"

    income_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pk_uuid = Synonym("income_uuid")

    user_uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_uuid"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    start_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    recurrence_type: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, default="MONTHLY")
    interval_value: Mapped[int] = mapped_column(Integer, nullable=True)
    remaining_occurrences: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    next_due_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user = relationship("UserEntity", back_populates="incomes")
