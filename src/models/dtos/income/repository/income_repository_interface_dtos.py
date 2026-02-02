from typing import Tuple
from uuid import UUID

from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from pydantic import StrictStr


class CreateIncomeCommandDTO(BaseDTO):
    user_uuid: UUID
    title: StrictStr
    amount: int
    day_of_month: int
    count: int | None = None
    is_active: bool
    notes: StrictStr | None = None


class CreateIncomeResponseDTO(BaseDTO):
    income_uuid: UUID


class GetIncomeQueryDTO(BaseDTO):
    income_uuid: UUID


class GetIncomeResponseDTO(BaseDTO):
    income_uuid: UUID
    user_uuid: UUID
    title: StrictStr
    amount: int
    day_of_month: int
    count: int | None = None
    is_active: bool
    notes: StrictStr | None = None


class UpdateIncomeCommandDTO(BaseDTO):
    income_uuid: UUID
    user_uuid: UUID | None = None
    title: StrictStr | None = None
    amount: int | None = None
    day_of_month: int | None = None
    count: int | None = None
    is_active: bool | None = None
    notes: StrictStr | None = None


class DeleteIncomeCommandDTO(BaseDTO):
    income_uuid: UUID


class SearchIncomeQueryDTO(BaseDTO):
    user_uuid: UUID
    is_active: bool | None = None
    days: Tuple[int, int] | None = None
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class SearchIncomeResponseDTO(BaseDTO):
    incomes: list[GetIncomeResponseDTO]
    total: int


class GetTotalIncomeQueryDTO(BaseDTO):
    user_uuid: UUID
    is_active: bool | None = None
    days: Tuple[int, int] | None = None


class GetTotalIncomeResponseDTO(BaseDTO):
    total_income_amount: int
