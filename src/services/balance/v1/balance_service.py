from uuid import UUID
from archipy.models.errors import NotFoundError
from archipy.models.types import SortOrderType
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from src.logics.balance.balance_logic import BalanceLogic
from src.models.dtos.balance.domain.v1.balance_domain_interface_dtos import GetBalanceOutputDTOV1
from src.models.types.api_router_type import ApiRouterType
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
    logic: BalanceLogic = Depends(Provide[ServiceContainer.balance_logic]),
) -> GetBalanceOutputDTOV1:
    return await logic.get_balance(user_uuid=user_uuid)
