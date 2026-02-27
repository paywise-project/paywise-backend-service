from archipy.adapters.base.sqlalchemy.adapters import SQLAlchemyFilterMixin
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.models.errors import NotFoundError
from archipy.models.types.base_types import FilterOperationType
from sqlalchemy import delete, select, update, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import Select, Update

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
from src.models.entities import NotificationEntity


class NotificationPostgresAdapter(SQLAlchemyFilterMixin):
    def __init__(self, adapter: AsyncPostgresSQLAlchemyAdapter) -> None:
        self._adapter: AsyncPostgresSQLAlchemyAdapter = adapter

    async def create_notification(self, input_dto: CreateNotificationCommandDTO) -> CreateNotificationResponseDTO:
        _entity = NotificationEntity(**input_dto.model_dump())
        result = await self._adapter.create(entity=_entity)
        return CreateNotificationResponseDTO.model_validate(obj=result)

    async def get_notification(self, input_dto: GetNotificationQueryDTO) -> GetNotificationResponseDTO:
        select_query = select(NotificationEntity).where(NotificationEntity.is_deleted.is_(False))
        _query = self._apply_filter(
            query=select_query,
            field=NotificationEntity.notification_uuid,
            value=input_dto.notification_uuid,
            operation=FilterOperationType.EQUAL,
        )
        result = await self._adapter.execute(statement=_query)
        entity = result.scalar()

        if not entity:
            raise NotFoundError(resource_type=NotificationEntity.__name__)

        return GetNotificationResponseDTO.model_validate(obj=entity)

    async def search_notifications(self, input_dto: SearchNotificationQueryDTO) -> SearchNotificationResponseDTO:
        query: Select = select(NotificationEntity).where(NotificationEntity.is_deleted.is_(False))

        if input_dto.user_uuid:
            query = self._apply_filter(
                query=query,
                field=NotificationEntity.user_uuid,
                value=input_dto.user_uuid,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.notification_types:
            query = self._apply_filter(
                query=query,
                field=NotificationEntity.notification_type,
                value=input_dto.notification_types,
                operation=FilterOperationType.IN_LIST,
            )

        if input_dto.status_types:
            query = self._apply_filter(
                query=query,
                field=NotificationEntity.status_type,
                value=input_dto.status_types,
                operation=FilterOperationType.IN_LIST,
            )

        if input_dto.is_read is not None:
            query = self._apply_filter(
                query=query,
                field=NotificationEntity.is_read,
                value=input_dto.is_read,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.sent_at:
            sent_at_min, sent_at_max = input_dto.sent_at
            query = self._apply_filter(
                query=query,
                field=NotificationEntity.sent_at,
                value=sent_at_min,
                operation=FilterOperationType.GREATER_THAN_OR_EQUAL,
            )
            query = self._apply_filter(
                query=query,
                field=NotificationEntity.sent_at,
                value=sent_at_max,
                operation=FilterOperationType.LESS_THAN_OR_EQUAL,
            )

        if input_dto.payment_occurrence_uuid:
            query = self._apply_filter(
                query=query,
                field=NotificationEntity.payment_occurrence_uuid,
                value=input_dto.expense_uuid,
                operation=FilterOperationType.EQUAL,
            )

        entities, total = await self._adapter.execute_search_query(
            query=query,
            entity=NotificationEntity,
            sort_info=input_dto.sort_info,
            pagination=input_dto.pagination,
        )

        return SearchNotificationResponseDTO(notifications=entities, total=total)

    async def update_notification(self, input_dto: UpdateNotificationCommandDTO) -> None:
        update_data = input_dto.model_dump(exclude={"notification_uuid"}, exclude_none=True)
        if not update_data:
            return

        update_query: Update = (
            update(NotificationEntity)
            .where(
                NotificationEntity.notification_uuid == input_dto.notification_uuid,
                NotificationEntity.is_deleted.is_(False),
            )
            .values(**update_data)
        )

        result = await self._adapter.execute(statement=update_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=NotificationEntity.__name__)

    async def delete_notification(self, input_dto: DeleteNotificationCommandDTO) -> None:
        delete_query = (
            update(NotificationEntity)
            .where(
                NotificationEntity.notification_uuid == input_dto.notification_uuid,
                NotificationEntity.is_deleted.is_(False),
            )
            .values(is_deleted=True)
        )

        result = await self._adapter.execute(statement=delete_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=NotificationEntity.__name__)
