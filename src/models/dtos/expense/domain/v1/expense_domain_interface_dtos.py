from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from archipy.models.types.sort_order_type import SortOrderType
from datetime import datetime, date, time
from decimal import Decimal
from pydantic import StrictStr
from uuid import UUID

from src.models.types.enums import *


class CreateExpenseRestInputDTOV1(BaseDTO):
    user_uuid: UUID
    title: StrictStr
    amount: int
    category: StrictStr
    day_of_month: int
    status_type: StrictStr
    count: int | None = None
    is_active: bool
    notify_week_before: bool
    notify_day_before: bool
    notify_on_day: bool
    notes: StrictStr | None = None


class CreateExpenseInputDTOV1(CreateExpenseRestInputDTOV1):
    user_uuid: UUID | None = None

    @classmethod
    def create(
        cls,
        user_uuid: UUID | None = None,
        input_dto: CreateExpenseRestInputDTOV1 = None,
    ):
        if input_dto:
            return cls(user_uuid=user_uuid, **input_dto.model_dump(mode="json"))
        return cls(user_uuid=user_uuid)


class CreateExpenseOutputDTOV1(BaseDTO):
    expense_uuid: UUID


class GetExpenseInputDTOV1(BaseDTO):
    expense_uuid: UUID


class GetExpenseOutputDTOV1(BaseDTO):
    expense_uuid: UUID
    user_uuid: UUID
    title: StrictStr
    amount: int
    category: StrictStr
    day_of_month: int
    status_type: StrictStr
    count: int | None = None
    is_active: bool
    notify_week_before: bool
    notify_day_before: bool
    notify_on_day: bool
    notes: StrictStr | None = None


class UpdateExpenseRestInputDTOV1(BaseDTO):
    user_uuid: UUID | None = None
    title: StrictStr | None = None
    amount: int | None = None
    category: StrictStr | None = None
    day_of_month: int | None = None
    status_type: StrictStr | None = None
    count: int | None = None
    is_active: bool | None = None
    notify_week_before: bool | None = None
    notify_day_before: bool | None = None
    notify_on_day: bool | None = None
    notes: StrictStr | None = None


class UpdateExpenseInputDTOV1(UpdateExpenseRestInputDTOV1):
    expense_uuid: UUID


class DeleteExpenseInputDTOV1(BaseDTO):
    expense_uuid: UUID


class SearchExpenseInputDTOV1(BaseDTO):
    # TODO: Add search fields as needed
    pagination: PaginationDTO
    sort_info: SortDTO[str]  # Replace with appropriate sort enum

    @classmethod
    def create(
        cls,
        page: int = 1,
        page_size: int = 10,
        sort_column: str = "created_at",
        sort_order: SortOrderType = SortOrderType.DESCENDING,
    ):
        pagination = PaginationDTO(page=page, page_size=page_size)
        sort_info = SortDTO[str](column=sort_column, order=sort_order)
        return cls(pagination=pagination, sort_info=sort_info)


class ExpenseItemDTOV1(BaseDTO):
    expense_uuid: UUID
    user_uuid: UUID
    title: StrictStr
    amount: int
    category: StrictStr
    day_of_month: int
    status_type: StrictStr
    count: int | None = None
    is_active: bool
    notify_week_before: bool
    notify_day_before: bool
    notify_on_day: bool
    notes: StrictStr | None = None


class SearchExpenseOutputDTOV1(BaseDTO):
    expenses: list[ExpenseItemDTOV1]
    total: int
