from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from datetime import datetime, date, time
from decimal import Decimal
from pydantic import StrictStr
from uuid import UUID

from src.models.types.enums import *


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
    # TODO: Add search fields as needed
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class SearchIncomeResponseDTO(BaseDTO):
    incomes: list[GetIncomeResponseDTO]
    total: int
