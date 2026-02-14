from typing import Tuple
from uuid import UUID

from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from pydantic import StrictStr

from src.models.types.enums import *


class CreateExpenseCommandDTO(BaseDTO):
    user_uuid: UUID
    title: StrictStr
    amount: int
    category: ExpenseCategoryType
    day_of_month: int
    status_type: ExpenseStatusType
    count: int | None = None
    is_active: bool
    notify_week_before: bool
    notify_day_before: bool
    notify_on_day: bool
    notes: StrictStr | None = None


class CreateExpenseResponseDTO(BaseDTO):
    expense_uuid: UUID


class GetExpenseQueryDTO(BaseDTO):
    expense_uuid: UUID


class GetExpenseResponseDTO(BaseDTO):
    expense_uuid: UUID
    user_uuid: UUID
    title: StrictStr
    amount: int
    category: ExpenseCategoryType
    day_of_month: int
    status_type: ExpenseStatusType
    count: int | None = None
    is_active: bool
    notify_week_before: bool
    notify_day_before: bool
    notify_on_day: bool
    notes: StrictStr | None = None


class UpdateExpenseCommandDTO(BaseDTO):
    expense_uuid: UUID
    user_uuid: UUID | None = None
    title: StrictStr | None = None
    amount: int | None = None
    category: ExpenseCategoryType | None = None
    day_of_month: int | None = None
    status_type: ExpenseStatusType | None = None
    count: int | None = None
    is_active: bool | None = None
    notify_week_before: bool | None = None
    notify_day_before: bool | None = None
    notify_on_day: bool | None = None
    notes: StrictStr | None = None


class DeleteExpenseCommandDTO(BaseDTO):
    expense_uuid: UUID


class SearchExpenseQueryDTO(BaseDTO):
    user_uuid: UUID | None = None
    categories: list[ExpenseCategoryType] | None = None
    status_type: ExpenseStatusType | None = None
    is_active: bool | None = None
    days: Tuple[int, int] | None = None
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class SearchExpenseResponseDTO(BaseDTO):
    expenses: list[GetExpenseResponseDTO]
    total: int


class GetTotalExpenseQueryDTO(BaseDTO):
    user_uuid: UUID
    categories: list[ExpenseCategoryType] | None = None
    status_type: ExpenseStatusType | None = None
    is_active: bool | None = None
    days: Tuple[int, int] | None = None


class GetTotalExpenseResponseDTO(BaseDTO):
    total_expense_amount: int
