from datetime import datetime
from typing import Tuple
from uuid import UUID

from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from archipy.models.types.sort_order_type import SortOrderType
from pydantic import StrictStr, model_validator

from src.models.types.enums import *


class CreatePaymentRestInputDTOV1(BaseDTO):
    payment_type: PaymentType
    title: StrictStr
    amount: int
    category_type: PaymentCategoryType
    notes: StrictStr | None = None
    is_active: bool = True
    start_datetime: datetime
    recurrence_type: PaymentRecurrenceType
    interval_days: int | None = None
    total_occurrences: int | None = None
    notify_week_before: bool = False
    notify_day_before: bool = False
    notify_on_day: bool = False

    @model_validator(mode="after")
    def validate_payment(self):
        if self.recurrence_type == PaymentRecurrenceType.CUSTOM:
            if self.interval_days is None or not (7 <= self.interval_days <= 28):
                raise ValueError("CUSTOM recurrence requires interval_days between 7 and 28")
        if self.recurrence_type != PaymentRecurrenceType.CUSTOM and self.interval_days is not None:
            raise ValueError("interval_days is only valid for CUSTOM recurrence")
        if self.recurrence_type == PaymentRecurrenceType.ONE_TIME and self.total_occurrences is not None:
            raise ValueError("ONE_TIME payment cannot have total_occurrences")
        if self.payment_type == PaymentType.INCOME and (
            self.notify_week_before or self.notify_day_before or self.notify_on_day
        ):
            raise ValueError("INCOME payments cannot have notifications")
        return self


class CreatePaymentInputDTOV1(CreatePaymentRestInputDTOV1):
    user_uuid: UUID | None = None

    @classmethod
    def create(
        cls,
        user_uuid: UUID | None = None,
        input_dto: CreatePaymentRestInputDTOV1 = None,
    ):
        if input_dto:
            return cls(user_uuid=user_uuid, **input_dto.model_dump(mode="json"))
        return cls(user_uuid=user_uuid)


class CreatePaymentOutputDTOV1(BaseDTO):
    payment_uuid: UUID


class GetPaymentInputDTOV1(BaseDTO):
    payment_uuid: UUID


class GetPaymentOutputDTOV1(BaseDTO):
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


class UpdatePaymentRestInputDTOV1(BaseDTO):
    title: StrictStr | None = None
    category_type: PaymentCategoryType | None = None
    notes: StrictStr | None = None
    is_active: bool | None = None
    notify_week_before: bool | None = None
    notify_day_before: bool | None = None
    notify_on_day: bool | None = None


class UpdatePaymentInputDTOV1(UpdatePaymentRestInputDTOV1):
    payment_uuid: UUID


class DeletePaymentInputDTOV1(BaseDTO):
    payment_uuid: UUID


class SearchPaymentInputDTOV1(BaseDTO):
    user_uuid: UUID
    payment_type: PaymentType | None = None
    category_types: list[PaymentCategoryType] | None = None
    recurrence_types: list[PaymentRecurrenceType] | None = None
    is_active: bool | None = None
    start_datetime: Tuple[datetime, datetime] | None = None
    pagination: PaginationDTO
    sort_info: SortDTO[str]

    @classmethod
    def create(
        cls,
        user_uuid: UUID,
        payment_type: PaymentType | None = None,
        category_types: list[PaymentCategoryType] | None = None,
        recurrence_types: list[PaymentRecurrenceType] | None = None,
        is_active: bool | None = None,
        start_datetime: Tuple[datetime, datetime] | None = None,
        page: int = 1,
        page_size: int = 10,
        sort_column: str = "created_at",
        sort_order: SortOrderType = SortOrderType.DESCENDING,
    ):
        pagination = PaginationDTO(page=page, page_size=page_size)
        sort_info = SortDTO[str](column=sort_column, order=sort_order)
        return cls(
            user_uuid=user_uuid,
            payment_type=payment_type,
            category_types=category_types,
            recurrence_types=recurrence_types,
            is_active=is_active,
            start_datetime=start_datetime,
            pagination=pagination,
            sort_info=sort_info,
        )


class PaymentItemDTOV1(BaseDTO):
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


class SearchPaymentOutputDTOV1(BaseDTO):
    payments: list[PaymentItemDTOV1]
    total: int


class CreatePaymentOccurrenceRestInputDTOV1(BaseDTO):
    payment_uuid: UUID
    due_datetime: datetime
    status_type: PaymentOccurrenceStatusType | None = None
    paid_at: datetime | None = None
    occurrence_index: int


class CreatePaymentOccurrenceInputDTOV1(CreatePaymentOccurrenceRestInputDTOV1):
    user_uuid: UUID | None = None

    @classmethod
    def create(
        cls,
        user_uuid: UUID | None = None,
        input_dto: CreatePaymentOccurrenceRestInputDTOV1 = None,
    ):
        if input_dto:
            return cls(user_uuid=user_uuid, **input_dto.model_dump(mode="json"))
        return cls(user_uuid=user_uuid)


class CreatePaymentOccurrenceOutputDTOV1(BaseDTO):
    payment_occurrence_uuid: UUID


class GetPaymentOccurrenceInputDTOV1(BaseDTO):
    payment_occurrence_uuid: UUID


class GetPaymentOccurrenceOutputDTOV1(BaseDTO):
    payment_occurrence_uuid: UUID
    payment_uuid: UUID
    user_uuid: UUID
    due_datetime: datetime
    status_type: PaymentOccurrenceStatusType | None = None
    paid_at: datetime | None = None


class UpdatePaymentOccurrenceRestInputDTOV1(BaseDTO):
    status_type: PaymentOccurrenceStatusType | None = None
    paid_at: datetime | None = None


class UpdatePaymentOccurrenceInputDTOV1(UpdatePaymentOccurrenceRestInputDTOV1):
    payment_occurrence_uuid: UUID


class DeletePaymentOccurrenceInputDTOV1(BaseDTO):
    payment_occurrence_uuid: UUID


class SearchPaymentOccurrenceInputDTOV1(BaseDTO):
    user_uuid: UUID | None = None
    payment_uuid: UUID | None = None
    status_type: PaymentOccurrenceStatusType | None = None
    due_datetime: Tuple[datetime, datetime] | None = None
    paid_at: Tuple[datetime, datetime] | None = None
    pagination: PaginationDTO | None = None
    sort_info: SortDTO[str] | None = None

    @classmethod
    def create(
        cls,
        user_uuid: UUID | None = None,
        payment_uuid: UUID | None = None,
        status_type: PaymentOccurrenceStatusType | None = None,
        due_datetime: Tuple[datetime, datetime] | None = None,
        paid_at: Tuple[datetime, datetime] | None = None,
        page: int = 1,
        page_size: int = 10,
        sort_column: str = "due_datetime",
        sort_order: SortOrderType = SortOrderType.ASCENDING,
    ):
        pagination = PaginationDTO(page=page, page_size=page_size)
        sort_info = SortDTO[str](column=sort_column, order=sort_order)
        return cls(
            user_uuid=user_uuid,
            payment_uuid=payment_uuid,
            status_type=status_type,
            due_datetime=due_datetime,
            paid_at=paid_at,
            pagination=pagination,
            sort_info=sort_info,
        )


class PaymentOccurrenceItemDTOV1(BaseDTO):
    payment_occurrence_uuid: UUID
    payment_uuid: UUID
    user_uuid: UUID
    due_datetime: datetime
    status_type: PaymentOccurrenceStatusType | None = None
    paid_at: datetime | None = None
    occurrence_index: int


class SearchPaymentOccurrenceOutputDTOV1(BaseDTO):
    payment_occurrences: list[PaymentOccurrenceItemDTOV1]
    total: int


class GetCalendarInputDTOV1(BaseDTO):
    user_uuid: UUID
    start_datetime: datetime
    end_datetime: datetime
    payment_type: PaymentType | None = None


class CalendarItemDTOV1(BaseDTO):
    due_datetime: datetime
    payment_type: PaymentType
    title: str
    amount: int
    status_type: PaymentOccurrenceStatusType | None


class GetCalendarOutputDTOV1(BaseDTO):
    items: list[CalendarItemDTOV1]


class GetUpcomingPaymentInputDTOV1(BaseDTO):
    user_uuid: UUID
    payment_type: PaymentType | None = None
    category_types: list[PaymentCategoryType] | None = None


class GetUpcomingPaymentOutputDTOV1(BaseDTO):
    payment_occurrence_uuid: UUID
    payment_uuid: UUID
    payment_type: PaymentType
    title: str
    amount: int
    category_type: PaymentCategoryType
    day_of_month_anchor: int | None
    due_datetime: datetime


class GetPaymentsWithOccurrencesInputDTOV1(SearchPaymentInputDTOV1):
    occurrence_count: int = 3
    occurrence_status_type: PaymentOccurrenceStatusType | None = None

    @classmethod
    def create(
        cls,
        user_uuid: UUID,
        payment_type: PaymentType | None = None,
        category_types: list[PaymentCategoryType] | None = None,
        recurrence_types: list[PaymentRecurrenceType] | None = None,
        is_active: bool | None = None,
        start_datetime: Tuple[datetime, datetime] | None = None,
        occurrence_count: int = 3,
        occurrence_status_type: PaymentOccurrenceStatusType | None = None,
        page: int = 1,
        page_size: int = 10,
        sort_column: str = "created_at",
        sort_order: SortOrderType = SortOrderType.DESCENDING,
    ):
        pagination = PaginationDTO(page=page, page_size=page_size)
        sort_info = SortDTO[str](column=sort_column, order=sort_order)
        return cls(
            user_uuid=user_uuid,
            payment_type=payment_type,
            category_types=category_types,
            recurrence_types=recurrence_types,
            is_active=is_active,
            start_datetime=start_datetime,
            occurrence_count=occurrence_count,
            occurrence_status_type=occurrence_status_type,
            pagination=pagination,
            sort_info=sort_info,
        )


class OccurrenceSummaryDTOV1(BaseDTO):
    payment_occurrence_uuid: UUID
    due_datetime: datetime
    status_type: PaymentOccurrenceStatusType | None
    paid_at: datetime | None
    occurrence_index: int


class PaymentWithOccurrencesDTOV1(PaymentItemDTOV1):
    occurrences: list[OccurrenceSummaryDTOV1]


class GetPaymentsWithOccurrencesOutputDTOV1(BaseDTO):
    payments: list[PaymentWithOccurrencesDTOV1]
    total: int
