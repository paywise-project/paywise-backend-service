import uuid
from datetime import datetime
from typing import Optional

from archipy.models.entities import UpdatableDeletableEntity
from sqlalchemy import Column, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship, Synonym


class NotificationEntity(UpdatableDeletableEntity):
    __tablename__ = "notifications"

    notification_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pk_uuid = Synonym("notification_uuid")

    user_uuid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_uuid"), nullable=False)
    expense_uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("expenses.expense_uuid"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    notification_type: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)

    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, default="PENDING")
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user = relationship("UserEntity", back_populates="notifications")
    expense = relationship("ExpenseEntity", back_populates="notifications")
