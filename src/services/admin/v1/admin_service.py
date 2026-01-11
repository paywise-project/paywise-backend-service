from archipy.models.errors import NotFoundError
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from uuid import UUID

from src.configs.containers import ServiceContainer
from src.logics.admin.admin_logic import AdminLogic
from src.logics.user.user_logic import UserLogic
from src.models.dtos.admin.domain.v1.admin_domain_interface_dtos import (
    CreateAppConfigInputDTOV1,
    CreateAppConfigOutputDTOV1,
    CreateAppConfigRestInputDTOV1,
    DeleteAppConfigInputDTOV1,
    GetAppConfigInputDTOV1,
    GetAppConfigOutputDTOV1,
    SearchAppConfigInputDTOV1,
    SearchAppConfigOutputDTOV1,
    UpdateAppConfigInputDTOV1,
    UpdateAppConfigRestInputDTOV1,
    GetStartupConfigOutputDTOV1,
)
from src.models.dtos.user.domain.v1.user_domain_interface_dtos import (
    CreateUserOutputDTOV1,
    CreateUserRestInputDTOV1,
    CreateUserInputDTOV1,
    GetUserOutputDTOV1,
    SearchUserOutputDTOV1,
    SearchUserInputDTOV1,
    DeleteUserInputDTOV1,
)
from src.models.types.api_router_type import ApiRouterType
from src.utils.utils import Utils

routerV1: APIRouter = APIRouter(tags=[ApiRouterType.ADMIN])

AdminRouterV1: APIRouter = APIRouter(tags=[ApiRouterType.ADMIN])


@AdminRouterV1.post(
    path="/app_configs",
    response_model=CreateAppConfigOutputDTOV1,
)
@inject
async def create_app_config(
    input_dto: CreateAppConfigRestInputDTOV1,
    logic: AdminLogic = Depends(Provide[ServiceContainer.admin_logic]),
) -> CreateAppConfigOutputDTOV1:
    input_dto = CreateAppConfigInputDTOV1.model_validate(input_dto)
    return await logic.create_app_config(input_dto=input_dto)


@AdminRouterV1.get(
    path="/app_configs",
    response_model=SearchAppConfigOutputDTOV1,
)
@inject
async def search_app_configs(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    logic: AdminLogic = Depends(Provide[ServiceContainer.admin_logic]),
) -> SearchAppConfigOutputDTOV1:
    input_dto = SearchAppConfigInputDTOV1.create(
        page=page,
        page_size=page_size,
    )
    return await logic.search_app_configs(input_dto=input_dto)


@AdminRouterV1.put(
    path="/app_configs/{app_config_uuid}",
)
@inject
async def update_app_config(
    app_config_uuid: UUID,
    input_dto: UpdateAppConfigRestInputDTOV1,
    logic: AdminLogic = Depends(Provide[ServiceContainer.admin_logic]),
) -> None:
    update_dto = UpdateAppConfigInputDTOV1(**input_dto.model_dump(), app_config_uuid=app_config_uuid)
    await logic.update_app_config(input_dto=update_dto)


@routerV1.get(
    path="/startup",
    response_model=GetStartupConfigOutputDTOV1,
)
@inject
async def get_startup_config(
    version: str = "0.0.1",
    logic: AdminLogic = Depends(Provide[ServiceContainer.admin_logic]),
) -> GetStartupConfigOutputDTOV1:
    return await logic.get_startup_config(version)


@routerV1.post(
    path="/{user_uuid}/users",
    response_model=CreateUserOutputDTOV1,
)
@inject
async def create_user(
    user_uuid: UUID,
    input_dto: CreateUserRestInputDTOV1,
    logic: UserLogic = Depends(Provide[ServiceContainer.user_logic]),
) -> CreateUserOutputDTOV1:
    input_dto = CreateUserInputDTOV1.create(user_uuid=user_uuid, input_dto=input_dto)
    return await logic.create_user(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/users",
    response_model=SearchUserOutputDTOV1,
)
@inject
async def search_users(
    user_uuid: UUID,
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    logic: UserLogic = Depends(Provide[ServiceContainer.user_logic]),
) -> SearchUserOutputDTOV1:
    input_dto = SearchUserInputDTOV1.create(
        page=page,
        page_size=page_size,
    )
    return await logic.search_users(input_dto=input_dto)


@routerV1.delete(
    path="/users/{user_uuid}",
)
@inject
async def delete_user(
    user_uuid: UUID,
    logic: UserLogic = Depends(Provide[ServiceContainer.user_logic]),
) -> None:
    input_dto = DeleteUserInputDTOV1(user_uuid=user_uuid)
    await logic.delete_user(input_dto=input_dto)
