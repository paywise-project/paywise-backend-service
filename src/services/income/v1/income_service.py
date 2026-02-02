from uuid import UUID

from archipy.models.errors import NotFoundError
from archipy.models.types import SortOrderType
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from src.configs.containers import ServiceContainer
from src.logics.income.income_logic import IncomeLogic
from src.models.dtos.income.domain.v1.income_domain_interface_dtos import (
    CreateIncomeInputDTOV1,
    CreateIncomeOutputDTOV1,
    CreateIncomeRestInputDTOV1,
    DeleteIncomeInputDTOV1,
    GetIncomeInputDTOV1,
    GetIncomeOutputDTOV1,
    SearchIncomeInputDTOV1,
    SearchIncomeOutputDTOV1,
    UpdateIncomeInputDTOV1,
    UpdateIncomeRestInputDTOV1,
    GetTotalIncomeInputDTOV1,
    GetTotalIncomeOutputDTOV1,
)
from src.models.types.api_router_type import ApiRouterType
from src.utils.utils import Utils

routerV1: APIRouter = APIRouter(tags=[ApiRouterType.INCOME])


@routerV1.post(
    path="/{user_uuid}/incomes",
    response_model=CreateIncomeOutputDTOV1,
)
@inject
async def create_income(
    user_uuid: UUID,
    input_dto: CreateIncomeRestInputDTOV1,
    logic: IncomeLogic = Depends(Provide[ServiceContainer.income_logic]),
) -> CreateIncomeOutputDTOV1:
    input_dto = CreateIncomeInputDTOV1.create(user_uuid=user_uuid, input_dto=input_dto)
    return await logic.create_income(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/incomes/{income_uuid}",
    response_model=GetIncomeOutputDTOV1,
    responses=Utils.get_fastapi_exception_responses([NotFoundError]),
)
@inject
async def get_income(
    user_uuid: UUID,
    income_uuid: UUID,
    logic: IncomeLogic = Depends(Provide[ServiceContainer.income_logic]),
) -> GetIncomeOutputDTOV1:
    input_dto = GetIncomeInputDTOV1(income_uuid=income_uuid)
    return await logic.get_income(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/incomes",
    response_model=SearchIncomeOutputDTOV1,
)
@inject
async def search_incomes(
    user_uuid: UUID,
    is_active: bool | None = Query(default=None, description="Filter by activation"),
    day_min: int | None = Query(default=None, description="Minimum day"),
    day_max: int | None = Query(default=None, description="Maximum day"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    sort_column: str = Query(default="created_at", description="Column to sort by"),
    sort_order: SortOrderType = Query(default=SortOrderType.DESCENDING),
    logic: IncomeLogic = Depends(Provide[ServiceContainer.income_logic]),
) -> SearchIncomeOutputDTOV1:
    input_dto = SearchIncomeInputDTOV1.create(
        user_uuid=user_uuid,
        is_active=is_active,
        days=(day_min, day_max) if day_min is not None and day_max is not None else None,
        page=page,
        page_size=page_size,
        sort_column=sort_column,
        sort_order=sort_order,
    )
    return await logic.search_incomes(input_dto=input_dto)


@routerV1.put(
    path="/{user_uuid}/incomes/{income_uuid}",
)
@inject
async def update_income(
    user_uuid: UUID,
    income_uuid: UUID,
    input_dto: UpdateIncomeRestInputDTOV1,
    logic: IncomeLogic = Depends(Provide[ServiceContainer.income_logic]),
) -> None:
    update_dto = UpdateIncomeInputDTOV1(**input_dto.model_dump(), income_uuid=income_uuid)
    await logic.update_income(input_dto=update_dto)


@routerV1.delete(
    path="/{user_uuid}/incomes/{income_uuid}",
)
@inject
async def delete_income(
    user_uuid: UUID,
    income_uuid: UUID,
    logic: IncomeLogic = Depends(Provide[ServiceContainer.income_logic]),
) -> None:
    input_dto = DeleteIncomeInputDTOV1(income_uuid=income_uuid)
    await logic.delete_income(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/total-income",
    response_model=GetTotalIncomeOutputDTOV1,
)
@inject
async def get_total_income(
    user_uuid: UUID,
    is_active: bool | None = Query(default=None, description="Filter by activation"),
    day_min: int | None = Query(default=None, description="Minimum day"),
    day_max: int | None = Query(default=None, description="Maximum day"),
    logic: IncomeLogic = Depends(Provide[ServiceContainer.income_logic]),
) -> GetTotalIncomeOutputDTOV1:
    input_dto = GetTotalIncomeInputDTOV1(
        user_uuid=user_uuid,
        is_active=is_active,
        days=(day_min, day_max) if day_min is not None and day_max is not None else None,
    )
    return await logic.get_total_income(input_dto=input_dto)
