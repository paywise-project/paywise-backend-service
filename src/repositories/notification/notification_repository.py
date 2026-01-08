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
from src.repositories.notification.adapters.notification_postgres_adapter import NotificationPostgresAdapter


class NotificationRepository:
    def __init__(self, postgres_adapter: NotificationPostgresAdapter):
        self._postgres_adapter: NotificationPostgresAdapter = postgres_adapter

    async def create_notification(self, input_dto: CreateNotificationCommandDTO) -> CreateNotificationResponseDTO:
        return await self._postgres_adapter.create_notification(input_dto=input_dto)

    async def get_notification(self, input_dto: GetNotificationQueryDTO) -> GetNotificationResponseDTO:
        return await self._postgres_adapter.get_notification(input_dto=input_dto)

    async def search_notifications(self, input_dto: SearchNotificationQueryDTO) -> SearchNotificationResponseDTO:
        return await self._postgres_adapter.search_notifications(input_dto=input_dto)

    async def update_notification(self, input_dto: UpdateNotificationCommandDTO) -> None:
        await self._postgres_adapter.update_notification(input_dto=input_dto)

    async def delete_notification(self, input_dto: DeleteNotificationCommandDTO) -> None:
        await self._postgres_adapter.delete_notification(input_dto=input_dto)
