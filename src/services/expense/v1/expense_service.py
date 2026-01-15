from uuid import UUID

from archipy.models.errors import NotFoundError
from archipy.models.types import SortOrderType
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from src.configs.containers import ServiceContainer
from src.logics.expense.expense_logic import ExpenseLogic
from src.models.dtos.expense.domain.v1.expense_domain_interface_dtos import (
    CreateExpenseInputDTOV1,
    CreateExpenseOutputDTOV1,
    CreateExpenseRestInputDTOV1,
    DeleteExpenseInputDTOV1,
    GetExpenseInputDTOV1,
    GetExpenseOutputDTOV1,
    SearchExpenseInputDTOV1,
    SearchExpenseOutputDTOV1,
    UpdateExpenseInputDTOV1,
    UpdateExpenseRestInputDTOV1,
)
from src.models.types.api_router_type import ApiRouterType
from src.models.types.enums import ExpenseCategoryType, ExpenseStatusType
from src.utils.utils import Utils

routerV1: APIRouter = APIRouter(tags=[ApiRouterType.EXPENSE])


@routerV1.post(
    path="/{user_uuid}/expenses",
    response_model=CreateExpenseOutputDTOV1,
)
@inject
async def create_expense(
    user_uuid: UUID,
    input_dto: CreateExpenseRestInputDTOV1,
    logic: ExpenseLogic = Depends(Provide[ServiceContainer.expense_logic]),
) -> CreateExpenseOutputDTOV1:
    input_dto = CreateExpenseInputDTOV1.create(user_uuid=user_uuid, input_dto=input_dto)
    return await logic.create_expense(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/expenses/{expense_uuid}",
    response_model=GetExpenseOutputDTOV1,
    responses=Utils.get_fastapi_exception_responses([NotFoundError]),
)
@inject
async def get_expense(
    user_uuid: UUID,
    expense_uuid: UUID,
    logic: ExpenseLogic = Depends(Provide[ServiceContainer.expense_logic]),
) -> GetExpenseOutputDTOV1:
    input_dto = GetExpenseInputDTOV1(expense_uuid=expense_uuid)
    return await logic.get_expense(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/expenses",
    response_model=SearchExpenseOutputDTOV1,
)
@inject
async def search_expenses(
    user_uuid: UUID,
    categories: list[ExpenseCategoryType] | None = Query(default=None, description="Filter by Categories"),
    status_type: ExpenseStatusType | None = Query(default=None, description="Filter by status type"),
    is_active: bool | None = Query(default=None, description="Filter by activation"),
    day_min: int | None = Query(default=None, description="Minimum day"),
    day_max: int | None = Query(default=None, description="Maximum day"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    sort_column: str = Query(default="created_at", description="Column to sort by"),
    sort_order: SortOrderType = Query(default=SortOrderType.DESCENDING),
    logic: ExpenseLogic = Depends(Provide[ServiceContainer.expense_logic]),
) -> SearchExpenseOutputDTOV1:
    input_dto = SearchExpenseInputDTOV1.create(
        user_uuid=user_uuid,
        categories=categories,
        status_type=status_type,
        is_active=is_active,
        days=(day_min, day_max) if day_min is not None and day_max is not None else None,
        page=page,
        page_size=page_size,
        sort_column=sort_column,
        sort_order=sort_order,
    )
    return await logic.search_expenses(input_dto=input_dto)


@routerV1.put(
    path="/{user_uuid}/expenses/{expense_uuid}",
)
@inject
async def update_expense(
    user_uuid: UUID,
    expense_uuid: UUID,
    input_dto: UpdateExpenseRestInputDTOV1,
    logic: ExpenseLogic = Depends(Provide[ServiceContainer.expense_logic]),
) -> None:
    update_dto = UpdateExpenseInputDTOV1(**input_dto.model_dump(), expense_uuid=expense_uuid)
    await logic.update_expense(input_dto=update_dto)


@routerV1.delete(
    path="/{user_uuid}/expenses/{expense_uuid}",
)
@inject
async def delete_expense(
    user_uuid: UUID,
    expense_uuid: UUID,
    logic: ExpenseLogic = Depends(Provide[ServiceContainer.expense_logic]),
) -> None:
    input_dto = DeleteExpenseInputDTOV1(expense_uuid=expense_uuid)
    await logic.delete_expense(input_dto=input_dto)
