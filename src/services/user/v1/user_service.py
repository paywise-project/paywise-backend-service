from uuid import UUID

from archipy.models.errors import NotFoundError
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.configs.containers import ServiceContainer
from src.logics.user.user_logic import UserLogic
from src.models.dtos.user.domain.v1.user_domain_interface_dtos import (
    GetUserInputDTOV1,
    GetUserOutputDTOV1,
    UpdateUserInputDTOV1,
    UpdateUserRestInputDTOV1,
)
from src.models.types.api_router_type import ApiRouterType
from src.utils.utils import Utils

routerV1: APIRouter = APIRouter(tags=[ApiRouterType.USER])


@routerV1.get(
    path="/{user_uuid}",
    response_model=GetUserOutputDTOV1,
    responses=Utils.get_fastapi_exception_responses(
        [
            NotFoundError,
        ],
    ),
)
@inject
async def get_user(
    user_uuid: UUID,
    logic: UserLogic = Depends(Provide[ServiceContainer.user_logic]),
) -> GetUserOutputDTOV1:
    input_dto = GetUserInputDTOV1(user_uuid=user_uuid)
    return await logic.get_user(input_dto=input_dto)


@routerV1.put(
    path="/{user_uuid}",
    responses=Utils.get_fastapi_exception_responses(
        [
            NotFoundError,
        ],
    ),
)
@inject
async def update_user(
    user_uuid: UUID,
    input_dto: UpdateUserRestInputDTOV1,
    logic: UserLogic = Depends(Provide[ServiceContainer.user_logic]),
) -> None:
    update_dto = UpdateUserInputDTOV1(**input_dto.model_dump(), user_uuid=user_uuid)
    await logic.update_user(input_dto=update_dto)
