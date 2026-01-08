from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from archipy.models.types.sort_order_type import SortOrderType
from datetime import datetime, date, time
from decimal import Decimal
from pydantic import StrictStr
from uuid import UUID

from src.models.types.enums import *


class CreateNotificationRestInputDTOV1(BaseDTO):
    user_uuid: UUID
    expense_uuid: UUID
    title: StrictStr
    message: StrictStr
    notification_type: StrictStr
    sent_at: datetime


class CreateNotificationInputDTOV1(CreateNotificationRestInputDTOV1):
    user_uuid: UUID | None = None

    @classmethod
    def create(
        cls,
        user_uuid: UUID | None = None,
        input_dto: CreateNotificationRestInputDTOV1 = None,
    ):
        if input_dto:
            return cls(user_uuid=user_uuid, **input_dto.model_dump(mode="json"))
        return cls(user_uuid=user_uuid)


class CreateNotificationOutputDTOV1(BaseDTO):
    notification_uuid: UUID


class GetNotificationInputDTOV1(BaseDTO):
    notification_uuid: UUID


class GetNotificationOutputDTOV1(BaseDTO):
    notification_uuid: UUID
    user_uuid: UUID
    expense_uuid: UUID
    title: StrictStr
    message: StrictStr
    notification_type: StrictStr
    sent_at: datetime


class UpdateNotificationRestInputDTOV1(BaseDTO):
    user_uuid: UUID | None = None
    expense_uuid: UUID | None = None
    title: StrictStr | None = None
    message: StrictStr | None = None
    notification_type: StrictStr | None = None
    sent_at: datetime | None = None


class UpdateNotificationInputDTOV1(UpdateNotificationRestInputDTOV1):
    notification_uuid: UUID


class DeleteNotificationInputDTOV1(BaseDTO):
    notification_uuid: UUID


class SearchNotificationInputDTOV1(BaseDTO):
    # TODO: Add search fields as needed
    pagination: PaginationDTO
    sort_info: SortDTO[str]  # Replace with appropriate sort enum

    @classmethod
    def create(
        cls,
        page: int = 1,
        page_size: int = 10,
        sort_column: str = "created_at",
        sort_order: SortOrderType = SortOrderType.DESCENDING,
    ):
        pagination = PaginationDTO(page=page, page_size=page_size)
        sort_info = SortDTO[str](column=sort_column, order=sort_order)
        return cls(pagination=pagination, sort_info=sort_info)


class NotificationItemDTOV1(BaseDTO):
    notification_uuid: UUID
    user_uuid: UUID
    expense_uuid: UUID
    title: StrictStr
    message: StrictStr
    notification_type: StrictStr
    sent_at: datetime


class SearchNotificationOutputDTOV1(BaseDTO):
    notifications: list[NotificationItemDTOV1]
    total: int
