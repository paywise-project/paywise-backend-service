import uuid
from datetime import datetime
from typing import Optional

from archipy.models.entities import UpdatableDeletableEntity
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship, Synonym


class PaymentEntity(UpdatableDeletableEntity):
    __tablename__ = "payments"

    payment_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pk_uuid = Synonym("payment_uuid")

    user_uuid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_uuid"), nullable=False)

    payment_type: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    title: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    category_type: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, default="OTHER")
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    start_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    recurrence_type: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, default="ONE_TIME")
    interval_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    day_of_month_anchor: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_occurrences: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    processed_occurrences: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    notify_week_before: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notify_day_before: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notify_on_day: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    user = relationship("UserEntity", back_populates="payments")
    occurrences = relationship("PaymentOccurrenceEntity", back_populates="payment")
    notifications = relationship("NotificationEntity", back_populates="payment")


class PaymentOccurrenceEntity(UpdatableDeletableEntity):
    __tablename__ = "payment_occurrences"

    payment_occurrence_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pk_uuid = Synonym("payment_occurrence_uuid")

    payment_uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("payments.payment_uuid"),
        nullable=False,
    )
    user_uuid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_uuid"), nullable=False)

    due_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status_type: Mapped[Optional[str]] = mapped_column(VARCHAR(20), nullable=True)
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    occurrence_index: Mapped[int] = mapped_column(Integer, nullable=False)

    payment = relationship("PaymentEntity", back_populates="occurrences")
    user = relationship("UserEntity", back_populates="payment_occurrences")
