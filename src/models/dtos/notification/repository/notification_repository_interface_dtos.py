from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from datetime import datetime, date, time
from decimal import Decimal
from pydantic import StrictStr
from uuid import UUID

from src.models.types.enums import *


class CreateNotificationCommandDTO(BaseDTO):
    user_uuid: UUID
    expense_uuid: UUID
    title: StrictStr
    message: StrictStr
    notification_type: StrictStr
    sent_at: datetime


class CreateNotificationResponseDTO(BaseDTO):
    notification_uuid: UUID


class GetNotificationQueryDTO(BaseDTO):
    notification_uuid: UUID


class GetNotificationResponseDTO(BaseDTO):
    notification_uuid: UUID
    user_uuid: UUID
    expense_uuid: UUID
    title: StrictStr
    message: StrictStr
    notification_type: StrictStr
    sent_at: datetime


class UpdateNotificationCommandDTO(BaseDTO):
    notification_uuid: UUID
    user_uuid: UUID | None = None
    expense_uuid: UUID | None = None
    title: StrictStr | None = None
    message: StrictStr | None = None
    notification_type: StrictStr | None = None
    sent_at: datetime | None = None


class DeleteNotificationCommandDTO(BaseDTO):
    notification_uuid: UUID


class SearchNotificationQueryDTO(BaseDTO):
    # TODO: Add search fields as needed
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class SearchNotificationResponseDTO(BaseDTO):
    notifications: list[GetNotificationResponseDTO]
    total: int
