from archipy.models.errors import NotFoundError
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from uuid import UUID

from src.configs.containers import ServiceContainer
from src.logics.notification.notification_logic import NotificationLogic
from src.models.dtos.notification.domain.v1.notification_domain_interface_dtos import (
    CreateNotificationInputDTOV1,
    CreateNotificationOutputDTOV1,
    CreateNotificationRestInputDTOV1,
    DeleteNotificationInputDTOV1,
    GetNotificationInputDTOV1,
    GetNotificationOutputDTOV1,
    SearchNotificationInputDTOV1,
    SearchNotificationOutputDTOV1,
    UpdateNotificationInputDTOV1,
    UpdateNotificationRestInputDTOV1,
)
from src.models.types.api_router_type import ApiRouterType
from src.utils.utils import Utils

routerV1: APIRouter = APIRouter(tags=[ApiRouterType.NOTIFICATION])


@routerV1.post(
    path="/{user_uuid}/notifications",
    response_model=CreateNotificationOutputDTOV1,
)
@inject
async def create_notification(
    user_uuid: UUID,
    input_dto: CreateNotificationRestInputDTOV1,
    logic: NotificationLogic = Depends(Provide[ServiceContainer.notification_logic]),
) -> CreateNotificationOutputDTOV1:
    input_dto = CreateNotificationInputDTOV1.create(user_uuid=user_uuid, input_dto=input_dto)
    return await logic.create_notification(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/notifications/{notification_uuid}",
    response_model=GetNotificationOutputDTOV1,
    responses=Utils.get_fastapi_exception_responses([NotFoundError]),
)
@inject
async def get_notification(
    user_uuid: UUID,
    notification_uuid: UUID,
    logic: NotificationLogic = Depends(Provide[ServiceContainer.notification_logic]),
) -> GetNotificationOutputDTOV1:
    input_dto = GetNotificationInputDTOV1(notification_uuid=notification_uuid)
    return await logic.get_notification(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/notifications",
    response_model=SearchNotificationOutputDTOV1,
)
@inject
async def search_notifications(
    user_uuid: UUID,
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    logic: NotificationLogic = Depends(Provide[ServiceContainer.notification_logic]),
) -> SearchNotificationOutputDTOV1:
    input_dto = SearchNotificationInputDTOV1.create(
        page=page,
        page_size=page_size,
    )
    return await logic.search_notifications(input_dto=input_dto)


@routerV1.put(
    path="/{user_uuid}/notifications/{notification_uuid}",
)
@inject
async def update_notification(
    user_uuid: UUID,
    notification_uuid: UUID,
    input_dto: UpdateNotificationRestInputDTOV1,
    logic: NotificationLogic = Depends(Provide[ServiceContainer.notification_logic]),
) -> None:
    update_dto = UpdateNotificationInputDTOV1(**input_dto.model_dump(), notification_uuid=notification_uuid)
    await logic.update_notification(input_dto=update_dto)


@routerV1.delete(
    path="/{user_uuid}/notifications/{notification_uuid}",
)
@inject
async def delete_notification(
    user_uuid: UUID,
    notification_uuid: UUID,
    logic: NotificationLogic = Depends(Provide[ServiceContainer.notification_logic]),
) -> None:
    input_dto = DeleteNotificationInputDTOV1(notification_uuid=notification_uuid)
    await logic.delete_notification(input_dto=input_dto)
