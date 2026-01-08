"""
Income related entities
"""

import uuid
from typing import Optional

from archipy.models.entities import UpdatableDeletableEntity
from sqlalchemy import Column, ForeignKey, Boolean, Integer, Text
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship, Synonym


class Income(UpdatableDeletableEntity):
    __tablename__ = "incomes"

    income_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pk_uuid = Synonym("income_uuid")

    user_uuid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_uuid"), nullable=False)

    title: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)

    day_of_month: Mapped[int] = mapped_column(Integer, nullable=False)

    count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="incomes")