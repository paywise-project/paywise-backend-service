from typing import Tuple
from uuid import UUID

from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from archipy.models.types.sort_order_type import SortOrderType
from pydantic import StrictStr


class CreateIncomeRestInputDTOV1(BaseDTO):
    title: StrictStr
    amount: int
    day_of_month: int
    count: int | None = None
    is_active: bool = True
    notes: StrictStr | None = None


class CreateIncomeInputDTOV1(CreateIncomeRestInputDTOV1):
    user_uuid: UUID | None = None

    @classmethod
    def create(
        cls,
        user_uuid: UUID | None = None,
        input_dto: CreateIncomeRestInputDTOV1 = None,
    ):
        if input_dto:
            return cls(user_uuid=user_uuid, **input_dto.model_dump(mode="json"))
        return cls(user_uuid=user_uuid)


class CreateIncomeOutputDTOV1(BaseDTO):
    income_uuid: UUID


class GetIncomeInputDTOV1(BaseDTO):
    income_uuid: UUID


class GetIncomeOutputDTOV1(BaseDTO):
    income_uuid: UUID
    user_uuid: UUID
    title: StrictStr
    amount: int
    day_of_month: int
    count: int | None = None
    is_active: bool
    notes: StrictStr | None = None


class UpdateIncomeRestInputDTOV1(BaseDTO):
    user_uuid: UUID | None = None
    title: StrictStr | None = None
    amount: int | None = None
    day_of_month: int | None = None
    count: int | None = None
    is_active: bool | None = None
    notes: StrictStr | None = None


class UpdateIncomeInputDTOV1(UpdateIncomeRestInputDTOV1):
    income_uuid: UUID


class DeleteIncomeInputDTOV1(BaseDTO):
    income_uuid: UUID


class SearchIncomeInputDTOV1(BaseDTO):
    user_uuid: UUID
    is_active: bool | None = None
    days: Tuple[int, int] | None = (None,)
    pagination: PaginationDTO
    sort_info: SortDTO[str]

    @classmethod
    def create(
        cls,
        user_uuid: UUID,
        is_active: bool | None = None,
        days: Tuple[int, int] | None = None,
        page: int = 1,
        page_size: int = 10,
        sort_column: str = "created_at",
        sort_order: SortOrderType = SortOrderType.DESCENDING,
    ):
        pagination = PaginationDTO(page=page, page_size=page_size)
        sort_info = SortDTO[str](column=sort_column, order=sort_order)
        return cls(
            user_uuid=user_uuid,
            is_active=is_active,
            days=days,
            pagination=pagination,
            sort_info=sort_info,
        )


class IncomeItemDTOV1(BaseDTO):
    income_uuid: UUID
    user_uuid: UUID
    title: StrictStr
    amount: int
    day_of_month: int
    count: int | None = None
    is_active: bool
    notes: StrictStr | None = None


class SearchIncomeOutputDTOV1(BaseDTO):
    incomes: list[IncomeItemDTOV1]
    total: int
