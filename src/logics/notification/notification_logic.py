from datetime import datetime

from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator
from uuid import UUID
from sqlalchemy.exc import IntegrityError
from src.models.dtos.notification.domain.v1.notification_domain_interface_dtos import (
    CreateNotificationInputDTOV1,
    CreateNotificationOutputDTOV1,
    GetNotificationInputDTOV1,
    GetNotificationOutputDTOV1,
    UpdateNotificationInputDTOV1,
    DeleteNotificationInputDTOV1,
    SearchNotificationInputDTOV1,
    SearchNotificationOutputDTOV1,
    UpdateNotificationStatusInputDTOV1,
)
from src.models.dtos.notification.repository.notification_repository_interface_dtos import (
    CreateNotificationCommandDTO,
    CreateNotificationResponseDTO,
    GetNotificationQueryDTO,
    GetNotificationResponseDTO,
    UpdateNotificationCommandDTO,
    DeleteNotificationCommandDTO,
    SearchNotificationQueryDTO,
    SearchNotificationResponseDTO,
)
from src.models.types.enums import NotificationStatusType
from src.repositories.notification.notification_repository import NotificationRepository


class NotificationLogic:
    def __init__(
        self,
        repository: NotificationRepository,
    ) -> None:
        self._repository: NotificationRepository = repository

    @async_postgres_sqlalchemy_atomic_decorator
    async def create_notification(
        self,
        input_dto: CreateNotificationInputDTOV1,
    ) -> CreateNotificationOutputDTOV1 | None:
        try:
            command = CreateNotificationCommandDTO.model_validate(input_dto)
            response: CreateNotificationResponseDTO = await self._repository.create_notification(input_dto=command)
            return CreateNotificationOutputDTOV1.model_validate(obj=response)
        except IntegrityError:
            return None

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_notification(self, input_dto: GetNotificationInputDTOV1) -> GetNotificationOutputDTOV1:
        query = GetNotificationQueryDTO.model_validate(obj=input_dto)
        response: GetNotificationResponseDTO = await self._repository.get_notification(input_dto=query)
        return GetNotificationOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def search_notifications(self, input_dto: SearchNotificationInputDTOV1) -> SearchNotificationOutputDTOV1:
        repository_dto = SearchNotificationQueryDTO.model_validate(input_dto)
        response: SearchNotificationResponseDTO = await self._repository.search_notifications(input_dto=repository_dto)
        return SearchNotificationOutputDTOV1.model_validate(response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def update_notification(self, input_dto: UpdateNotificationInputDTOV1) -> None:
        command = UpdateNotificationCommandDTO.model_validate(obj=input_dto)
        await self._repository.update_notification(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def delete_notification(self, input_dto: DeleteNotificationInputDTOV1) -> None:
        command = DeleteNotificationCommandDTO.model_validate(obj=input_dto)
        await self._repository.delete_notification(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def update_notification_status(self, input_dto: UpdateNotificationStatusInputDTOV1) -> None:
        command = UpdateNotificationCommandDTO(
            notification_uuid=input_dto.notification_uuid,
            status_type=input_dto.status_type,
            sent_at=datetime.now() if input_dto.status_type == NotificationStatusType.SENT else None,
        )
        await self._repository.update_notification(input_dto=command)
