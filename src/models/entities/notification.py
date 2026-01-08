"""
Notification related entities
"""

import uuid
from datetime import datetime

from archipy.models.entities import UpdatableDeletableEntity
from sqlalchemy import Column, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship, Synonym
from sqlalchemy.sql import func


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
    notification_type: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)

    sent_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="notifications")
    expense = relationship("Expense", back_populates="notifications")
