from datetime import datetime
from uuid import UUID
from archipy.models.errors import NotFoundError
from archipy.models.types import SortOrderType
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from src.logics.balance.balance_logic import BalanceLogic
from src.models.dtos.balance.domain.v1.balance_domain_interface_dtos import GetBalanceOutputDTOV1, GetBalanceInputDTOV1
from src.models.types.api_router_type import ApiRouterType
from src.models.types.enums import *
from src.utils.utils import Utils
from src.configs.containers import ServiceContainer

routerV1: APIRouter = APIRouter(tags=[ApiRouterType.BALANCE])


@routerV1.get(
    path="/{user_uuid}/balance",
    response_model=GetBalanceOutputDTOV1,
    responses=Utils.get_fastapi_exception_responses([NotFoundError]),
)
@inject
async def get_balance(
    user_uuid: UUID,
    payment_type: PaymentType | None = Query(default=None, description="Filter by payment type"),
    category_types: list[PaymentCategoryType] | None = Query(default=None, description="Filter by category types"),
    recurrence_types: list[PaymentRecurrenceType] | None = Query(
        default=None,
        description="Filter by recurrence types",
    ),
    is_active: bool | None = Query(default=None, description="Filter by active status"),
    status_type: PaymentOccurrenceStatusType | None = Query(default=None, description="Filter by status type"),
    due_datetime_min: datetime | None = Query(default=None, description="Minimum due datetime"),
    due_datetime_max: datetime | None = Query(default=None, description="Maximum due datetime"),
    logic: BalanceLogic = Depends(Provide[ServiceContainer.balance_logic]),
) -> GetBalanceOutputDTOV1:
    input_dto = GetBalanceInputDTOV1.create(
        user_uuid=user_uuid,
        payment_type=payment_type,
        category_types=category_types,
        recurrence_types=recurrence_types,
        is_active=is_active,
        status_type=status_type,
        due_datetime=(
            (due_datetime_min, due_datetime_max)
            if due_datetime_min is not None and due_datetime_max is not None
            else None
        ),
    )
    return await logic.get_balance(input_dto=input_dto)
