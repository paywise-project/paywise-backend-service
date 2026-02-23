from datetime import datetime
from typing import Tuple
from uuid import UUID

from archipy.models.dtos.base_dtos import BaseDTO

from src.models.types.enums import *


class GetBalanceInputDTOV1(BaseDTO):
    user_uuid: UUID
    payment_type: PaymentType | None = None
    category_types: list[PaymentCategoryType] | None = None
    recurrence_types: list[PaymentRecurrenceType] | None = None
    is_active: bool | None = None
    status_type: PaymentOccurrenceStatusType | None = None
    due_datetime: Tuple[datetime, datetime] | None = None

    @classmethod
    def create(
        cls,
        user_uuid: UUID,
        payment_type: PaymentType | None = None,
        category_types: list[PaymentCategoryType] | None = None,
        recurrence_types: list[PaymentRecurrenceType] | None = None,
        is_active: bool | None = None,
        status_type: PaymentOccurrenceStatusType | None = None,
        due_datetime: Tuple[datetime, datetime] | None = None,
    ):
        return cls(
            user_uuid=user_uuid,
            payment_type=payment_type,
            category_types=category_types,
            recurrence_types=recurrence_types,
            is_active=is_active,
            status_type=status_type,
            due_datetime=due_datetime,
        )


class GetBalanceOutputDTOV1(BaseDTO):
    balance: int
    total_income: int
    total_expense: int
