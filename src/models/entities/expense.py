import uuid
from typing import Optional

from archipy.models.entities import UpdatableDeletableEntity
from sqlalchemy import Column, ForeignKey, Boolean, Integer, Text
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship, Synonym


class Expense(UpdatableDeletableEntity):
    __tablename__ = "expenses"

    expense_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pk_uuid = Synonym("expense_uuid")

    user_uuid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_uuid"), nullable=False)

    title: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, default="OTHER")

    day_of_month: Mapped[int] = mapped_column(Integer, nullable=False)

    status_type: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, default="UNPAID")
    count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    notify_week_before: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notify_day_before: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notify_on_day: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="expenses")
    notifications = relationship("Notification", back_populates="expense")