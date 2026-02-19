from typing import Tuple

from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from datetime import datetime
from pydantic import StrictStr
from uuid import UUID

from src.models.types.enums import *


class CreatePaymentCommandDTO(BaseDTO):
    user_uuid: UUID
    payment_type: PaymentType
    title: StrictStr
    amount: int
    category_type: PaymentCategoryType
    notes: StrictStr | None = None
    is_active: bool
    start_datetime: datetime
    recurrence_type: PaymentRecurrenceType
    interval_days: int | None = None
    day_of_month_anchor: int | None = None
    total_occurrences: int | None = None
    notify_week_before: bool
    notify_day_before: bool
    notify_on_day: bool


class CreatePaymentResponseDTO(BaseDTO):
    payment_uuid: UUID


class GetPaymentQueryDTO(BaseDTO):
    payment_uuid: UUID
    user_uuid: UUID


class GetPaymentResponseDTO(BaseDTO):
    payment_uuid: UUID
    user_uuid: UUID
    payment_type: PaymentType
    title: StrictStr
    amount: int
    category_type: PaymentCategoryType
    notes: StrictStr | None = None
    is_active: bool
    start_datetime: datetime
    recurrence_type: PaymentRecurrenceType
    interval_days: int | None = None
    day_of_month_anchor: int | None = None
    total_occurrences: int | None = None
    processed_occurrences: int
    notify_week_before: bool
    notify_day_before: bool
    notify_on_day: bool


class UpdatePaymentCommandDTO(BaseDTO):
    payment_uuid: UUID
    user_uuid: UUID
    title: StrictStr | None = None
    category_type: PaymentCategoryType | None = None
    notes: StrictStr | None = None
    is_active: bool | None = None
    notify_week_before: bool | None = None
    notify_day_before: bool | None = None
    notify_on_day: bool | None = None


class DeletePaymentCommandDTO(BaseDTO):
    payment_uuid: UUID
    user_uuid: UUID


class SearchPaymentQueryDTO(BaseDTO):
    user_uuid: UUID
    payment_type: PaymentType | None = None
    category_types: list[PaymentCategoryType] | None = None
    recurrence_types: list[PaymentRecurrenceType] | None = None
    is_active: bool | None = None
    start_datetime: Tuple[datetime, datetime] | None = None
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class SearchPaymentResponseDTO(BaseDTO):
    payments: list[GetPaymentResponseDTO]
    total: int


class CreatePaymentOccurrenceCommandDTO(BaseDTO):
    payment_uuid: UUID
    user_uuid: UUID
    due_datetime: datetime
    status_type: PaymentOccurrenceStatusType | None = None


class CreatePaymentOccurrenceResponseDTO(BaseDTO):
    payment_occurrence_uuid: UUID


class GetPaymentOccurrenceQueryDTO(BaseDTO):
    payment_occurrence_uuid: UUID
    user_uuid: UUID


class GetPaymentOccurrenceResponseDTO(BaseDTO):
    payment_occurrence_uuid: UUID
    payment_uuid: UUID
    user_uuid: UUID
    due_datetime: datetime
    status_type: PaymentOccurrenceStatusType | None = None
    paid_at: datetime | None = None


class UpdatePaymentOccurrenceCommandDTO(BaseDTO):
    payment_occurrence_uuid: UUID
    user_uuid: UUID
    status_type: PaymentOccurrenceStatusType | None = None
    paid_at: datetime | None = None


class DeletePaymentOccurrenceCommandDTO(BaseDTO):
    payment_occurrence_uuid: UUID
    user_uuid: UUID


class SearchPaymentOccurrenceQueryDTO(BaseDTO):
    user_uuid: UUID
    payment_uuid: UUID | None = None
    status_type: PaymentOccurrenceStatusType | None = None
    due_datetime: Tuple[datetime, datetime] | None = None
    paid_at: Tuple[datetime, datetime] | None = None
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class SearchPaymentOccurrenceResponseDTO(BaseDTO):
    payment_occurrences: list[GetPaymentOccurrenceResponseDTO]
    total: int
