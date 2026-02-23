from datetime import datetime
from typing import Tuple
from uuid import UUID

from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from pydantic import StrictStr

from src.models.types.enums import *


class CreateNotificationCommandDTO(BaseDTO):
    user_uuid: UUID
    payment_uuid: UUID
    title: StrictStr
    message: StrictStr
    notification_type: NotificationType
    sent_at: datetime | None = None
    status: NotificationStatusType
    is_read: bool


class CreateNotificationResponseDTO(BaseDTO):
    notification_uuid: UUID


class GetNotificationQueryDTO(BaseDTO):
    notification_uuid: UUID


class GetNotificationResponseDTO(BaseDTO):
    notification_uuid: UUID
    user_uuid: UUID
    payment_uuid: UUID
    title: StrictStr
    message: StrictStr
    notification_type: NotificationType
    sent_at: datetime | None = None
    status: NotificationStatusType
    is_read: bool


class UpdateNotificationCommandDTO(BaseDTO):
    notification_uuid: UUID
    user_uuid: UUID | None = None
    payment_uuid: UUID | None = None
    title: StrictStr | None = None
    message: StrictStr | None = None
    notification_type: NotificationType | None = None
    sent_at: datetime | None = None
    status: NotificationStatusType | None = None
    is_read: bool | None = None


class DeleteNotificationCommandDTO(BaseDTO):
    notification_uuid: UUID


class SearchNotificationQueryDTO(BaseDTO):
    user_uuid: UUID
    notification_types: list[str] | None = None
    status_types: list[str] | None = None
    is_read: bool | None = None
    sent_at: Tuple[datetime, datetime] | None = None
    payment_uuid: UUID | None = None
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class SearchNotificationResponseDTO(BaseDTO):
    notifications: list[GetNotificationResponseDTO]
    total: int
