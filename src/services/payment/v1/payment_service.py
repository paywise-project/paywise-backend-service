from datetime import datetime

from archipy.models.errors import NotFoundError
from archipy.models.types import SortOrderType
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from uuid import UUID

from src.configs.containers import ServiceContainer
from src.logics.payment.payment_logic import PaymentLogic
from src.models.dtos.payment.domain.v1.payment_domain_interface_dtos import *
from src.models.types.api_router_type import ApiRouterType
from src.models.types.enums import *
from src.utils.utils import Utils

routerV1: APIRouter = APIRouter(tags=[ApiRouterType.PAYMENT])


@routerV1.post(
    path="/{user_uuid}/payments",
    response_model=CreatePaymentOutputDTOV1,
)
@inject
async def create_payment(
    user_uuid: UUID,
    input_dto: CreatePaymentRestInputDTOV1,
    logic: PaymentLogic = Depends(Provide[ServiceContainer.payment_logic]),
) -> CreatePaymentOutputDTOV1:
    input_dto = CreatePaymentInputDTOV1.create(user_uuid=user_uuid, input_dto=input_dto)
    return await logic.create_payment(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/payments/{payment_uuid}",
    response_model=GetPaymentOutputDTOV1,
    responses=Utils.get_fastapi_exception_responses([NotFoundError]),
)
@inject
async def get_payment(
    user_uuid: UUID,
    payment_uuid: UUID,
    logic: PaymentLogic = Depends(Provide[ServiceContainer.payment_logic]),
) -> GetPaymentOutputDTOV1:
    input_dto = GetPaymentInputDTOV1(payment_uuid=payment_uuid)
    return await logic.get_payment(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/payments",
    response_model=SearchPaymentOutputDTOV1,
)
@inject
async def search_payments(
    user_uuid: UUID,
    payment_type: PaymentType | None = Query(default=None, description="Filter by payment type"),
    category_types: list[PaymentCategoryType] | None = Query(default=None, description="Filter by category types"),
    recurrence_types: list[PaymentRecurrenceType] | None = Query(
        default=None,
        description="Filter by recurrence types",
    ),
    is_active: bool | None = Query(default=None, description="Filter by active status"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    sort_column: str = Query(default="created_at", description="Column to sort by"),
    sort_order: SortOrderType = Query(default=SortOrderType.DESCENDING),
    logic: PaymentLogic = Depends(Provide[ServiceContainer.payment_logic]),
) -> SearchPaymentOutputDTOV1:
    input_dto = SearchPaymentInputDTOV1.create(
        user_uuid=user_uuid,
        payment_type=payment_type,
        category_types=category_types,
        recurrence_types=recurrence_types,
        is_active=is_active,
        page=page,
        page_size=page_size,
        sort_column=sort_column,
        sort_order=sort_order,
    )
    return await logic.search_payments(input_dto=input_dto)


@routerV1.put(
    path="/{user_uuid}/payments/{payment_uuid}",
)
@inject
async def update_payment(
    user_uuid: UUID,
    payment_uuid: UUID,
    input_dto: UpdatePaymentRestInputDTOV1,
    logic: PaymentLogic = Depends(Provide[ServiceContainer.payment_logic]),
) -> None:
    update_dto = UpdatePaymentInputDTOV1(**input_dto.model_dump(), payment_uuid=payment_uuid)
    await logic.update_payment(input_dto=update_dto)


@routerV1.delete(
    path="/{user_uuid}/payments/{payment_uuid}",
)
@inject
async def delete_payment(
    user_uuid: UUID,
    payment_uuid: UUID,
    logic: PaymentLogic = Depends(Provide[ServiceContainer.payment_logic]),
) -> None:
    input_dto = DeletePaymentInputDTOV1(payment_uuid=payment_uuid)
    await logic.delete_payment(input_dto=input_dto)


@routerV1.post(
    path="/{user_uuid}/payment-occurrences",
    response_model=CreatePaymentOccurrenceOutputDTOV1,
)
@inject
async def create_payment_occurrence(
    user_uuid: UUID,
    input_dto: CreatePaymentOccurrenceRestInputDTOV1,
    logic: PaymentLogic = Depends(Provide[ServiceContainer.payment_logic]),
) -> CreatePaymentOccurrenceOutputDTOV1:
    input_dto = CreatePaymentOccurrenceInputDTOV1.create(user_uuid=user_uuid, input_dto=input_dto)
    return await logic.create_payment_occurrence(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/payment-occurrences/{payment_occurrence_uuid}",
    response_model=GetPaymentOccurrenceOutputDTOV1,
    responses=Utils.get_fastapi_exception_responses([NotFoundError]),
)
@inject
async def get_payment_occurrence(
    user_uuid: UUID,
    payment_occurrence_uuid: UUID,
    logic: PaymentLogic = Depends(Provide[ServiceContainer.payment_logic]),
) -> GetPaymentOccurrenceOutputDTOV1:
    input_dto = GetPaymentOccurrenceInputDTOV1(payment_occurrence_uuid=payment_occurrence_uuid)
    return await logic.get_payment_occurrence(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/payment-occurrences",
    response_model=SearchPaymentOccurrenceOutputDTOV1,
)
@inject
async def search_payment_occurrences(
    user_uuid: UUID,
    payment_uuid: UUID | None = Query(default=None, description="Filter by payment"),
    status_type: PaymentOccurrenceStatusType | None = Query(default=None, description="Filter by status type"),
    due_datetime_min: datetime | None = Query(default=None, description="Minimum due datetime"),
    due_datetime_max: datetime | None = Query(default=None, description="Maximum due datetime"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    sort_column: str = Query(default="due_datetime", description="Column to sort by"),
    sort_order: SortOrderType = Query(default=SortOrderType.DESCENDING),
    logic: PaymentLogic = Depends(Provide[ServiceContainer.payment_logic]),
) -> SearchPaymentOccurrenceOutputDTOV1:
    input_dto = SearchPaymentOccurrenceInputDTOV1.create(
        user_uuid=user_uuid,
        payment_uuid=payment_uuid,
        status_type=status_type,
        due_datetime=(
            (due_datetime_min, due_datetime_max)
            if due_datetime_min is not None and due_datetime_max is not None
            else None
        ),
        page=page,
        page_size=page_size,
        sort_column=sort_column,
        sort_order=sort_order,
    )
    return await logic.search_payment_occurrences(input_dto=input_dto)


@routerV1.put(
    path="/{user_uuid}/payment-occurrences/{payment_occurrence_uuid}",
)
@inject
async def update_payment_occurrence(
    user_uuid: UUID,
    payment_occurrence_uuid: UUID,
    input_dto: UpdatePaymentOccurrenceRestInputDTOV1,
    logic: PaymentLogic = Depends(Provide[ServiceContainer.payment_logic]),
) -> None:
    update_dto = UpdatePaymentOccurrenceInputDTOV1(
        **input_dto.model_dump(),
        payment_occurrence_uuid=payment_occurrence_uuid,
    )
    await logic.update_payment_occurrence(input_dto=update_dto)


@routerV1.delete(
    path="/{user_uuid}/payment-occurrences/{payment_occurrence_uuid}",
)
@inject
async def delete_payment_occurrence(
    user_uuid: UUID,
    payment_occurrence_uuid: UUID,
    logic: PaymentLogic = Depends(Provide[ServiceContainer.payment_logic]),
) -> None:
    input_dto = DeletePaymentOccurrenceInputDTOV1(payment_occurrence_uuid=payment_occurrence_uuid)
    await logic.delete_payment_occurrence(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/calendar",
    response_model=GetCalendarOutputDTOV1,
)
@inject
async def get_calendar(
    user_uuid: UUID,
    start_datetime: datetime = Query(description="Start of date range"),
    end_datetime: datetime = Query(description="End of date range"),
    payment_type: PaymentType | None = Query(default=None, description="Filter by payment type"),
    logic: PaymentLogic = Depends(Provide[ServiceContainer.payment_logic]),
) -> GetCalendarOutputDTOV1:
    input_dto = GetCalendarInputDTOV1(
        user_uuid=user_uuid,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        payment_type=payment_type,
    )
    return await logic.get_calendar(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/upcoming-payment",
    response_model=GetUpcomingPaymentOutputDTOV1,
)
@inject
async def get_upcoming_payment(
    user_uuid: UUID,
    payment_type: PaymentType | None = Query(default=None, description="Filter by payment type"),
    category_types: list[PaymentCategoryType] | None = Query(default=None, description="Filter by category types"),
    logic: PaymentLogic = Depends(Provide[ServiceContainer.payment_logic]),
) -> GetUpcomingPaymentOutputDTOV1:
    input_dto = GetUpcomingPaymentInputDTOV1(
        user_uuid=user_uuid,
        payment_type=payment_type,
        category_types=category_types,
    )
    return await logic.get_upcoming_payment(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/payments-with-occurrences",
    response_model=GetPaymentsWithOccurrencesOutputDTOV1,
)
@inject
async def get_payments_with_occurrences(
    user_uuid: UUID,
    payment_type: PaymentType | None = Query(default=None),
    category_types: list[PaymentCategoryType] | None = Query(default=None),
    recurrence_types: list[PaymentRecurrenceType] | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    occurrence_count: int = Query(default=3, ge=1, le=10),
    occurrence_status_type: PaymentOccurrenceStatusType | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    sort_column: str = Query(default="created_at"),
    sort_order: SortOrderType = Query(default=SortOrderType.DESCENDING),
    logic: PaymentLogic = Depends(Provide[ServiceContainer.payment_logic]),
) -> GetPaymentsWithOccurrencesOutputDTOV1:
    input_dto = GetPaymentsWithOccurrencesInputDTOV1.create(
        user_uuid=user_uuid,
        payment_type=payment_type,
        category_types=category_types,
        recurrence_types=recurrence_types,
        is_active=is_active,
        occurrence_count=occurrence_count,
        occurrence_status_type=occurrence_status_type,
        page=page,
        page_size=page_size,
        sort_column=sort_column,
        sort_order=sort_order,
    )
    return await logic.get_payments_with_occurrences(input_dto=input_dto)
