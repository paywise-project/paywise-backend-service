import uuid
from typing import Optional

from archipy.models.entities import UpdatableDeletableEntity
from sqlalchemy import Column, BigInteger
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship, Synonym


class UserEntity(UpdatableDeletableEntity):
    __tablename__ = "users"

    user_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pk_uuid = Synonym("user_uuid")

    first_name: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
    last_name: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(VARCHAR(15), nullable=True, unique=True)
    telegram_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, unique=True, index=True)
    telegram_username: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)

    username: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(VARCHAR(255), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(VARCHAR(255), nullable=True)
    profile_picture_path: Mapped[Optional[str]] = mapped_column(VARCHAR(500), nullable=True)

    user_type: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, default="USER")
    user_status: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, default="ACTIVE")
    gender_type: Mapped[Optional[str]] = mapped_column(VARCHAR(30), nullable=True)

    fcm_token: Mapped[Optional[str]] = mapped_column(VARCHAR(500), nullable=True)

    referrals_given = relationship(
        "ReferralEntity",
        foreign_keys="[ReferralEntity.referer_uuid]",
        back_populates="referer",
    )
    referrals_received = relationship(
        "ReferralEntity",
        foreign_keys="[ReferralEntity.referee_uuid]",
        back_populates="referee",
    )
    created_files = relationship("FileEntity", foreign_keys="[FileEntity.created_by]")
    updated_files = relationship("FileEntity", foreign_keys="[FileEntity.updated_by]")
    incomes = relationship("IncomeEntity", back_populates="user")
    expenses = relationship("ExpenseEntity", back_populates="user")
    notifications = relationship("NotificationEntity", back_populates="user")
