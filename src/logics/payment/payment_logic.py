from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator
from uuid import UUID
from datetime import datetime, timedelta
from uuid import UUID

import jdatetime

from src.models.dtos.balance.domain.v1.balance_domain_interface_dtos import GetBalanceInputDTOV1, GetBalanceOutputDTOV1
from src.models.dtos.payment.domain.v1.payment_domain_interface_dtos import (
    CreatePaymentInputDTOV1,
    CreatePaymentOutputDTOV1,
    GetPaymentInputDTOV1,
    GetPaymentOutputDTOV1,
    UpdatePaymentInputDTOV1,
    DeletePaymentInputDTOV1,
    SearchPaymentInputDTOV1,
    SearchPaymentOutputDTOV1,
    CreatePaymentOccurrenceInputDTOV1,
    CreatePaymentOccurrenceOutputDTOV1,
    GetPaymentOccurrenceInputDTOV1,
    GetPaymentOccurrenceOutputDTOV1,
    UpdatePaymentOccurrenceInputDTOV1,
    DeletePaymentOccurrenceInputDTOV1,
    SearchPaymentOccurrenceInputDTOV1,
    SearchPaymentOccurrenceOutputDTOV1,
)
from src.models.dtos.payment.repository.payment_repository_interface_dtos import (
    CreatePaymentCommandDTO,
    CreatePaymentResponseDTO,
    GetPaymentQueryDTO,
    GetPaymentResponseDTO,
    UpdatePaymentCommandDTO,
    DeletePaymentCommandDTO,
    SearchPaymentQueryDTO,
    SearchPaymentResponseDTO,
    CreatePaymentOccurrenceCommandDTO,
    CreatePaymentOccurrenceResponseDTO,
    GetPaymentOccurrenceQueryDTO,
    GetPaymentOccurrenceResponseDTO,
    UpdatePaymentOccurrenceCommandDTO,
    DeletePaymentOccurrenceCommandDTO,
    SearchPaymentOccurrenceQueryDTO,
    SearchPaymentOccurrenceResponseDTO,
    GetBalanceQueryDTO,
    GetBalanceResponseDTO,
)
from src.models.types.enums import *
from src.repositories.payment.payment_repository import PaymentRepository


class PaymentLogic:
    def __init__(
        self,
        repository: PaymentRepository,
    ) -> None:
        self._repository: PaymentRepository = repository

    @async_postgres_sqlalchemy_atomic_decorator
    async def create_payment(self, input_dto: CreatePaymentInputDTOV1) -> CreatePaymentOutputDTOV1:
        day_of_month_anchor = None
        if input_dto.recurrence_type == PaymentRecurrenceType.MONTHLY:
            j = jdatetime.datetime.fromgregorian(datetime=input_dto.start_datetime)
            day_of_month_anchor = j.day

        command = CreatePaymentCommandDTO(
            **input_dto.model_dump(mode="json"),
            day_of_month_anchor=day_of_month_anchor,
            processed_occurrences=0,
        )

        response: CreatePaymentResponseDTO = await self._repository.create_payment(input_dto=command)

        await self._generate_occurrences(
            payment_uuid=response.payment_uuid,
            user_uuid=command.user_uuid,
            payment_type=command.payment_type,
            recurrence_type=command.recurrence_type,
            start_datetime=command.start_datetime,
            interval_days=command.interval_days,
            day_of_month_anchor=command.day_of_month_anchor,
            total_occurrences=command.total_occurrences,
        )

        return CreatePaymentOutputDTOV1.model_validate(obj=response)

    async def _generate_occurrences(
        self,
        payment_uuid: UUID,
        user_uuid: UUID,
        payment_type: PaymentType,
        recurrence_type: PaymentRecurrenceType,
        start_datetime: datetime,
        interval_days: int | None,
        day_of_month_anchor: int | None,
        total_occurrences: int | None,
    ) -> None:
        occurrences = []
        current = start_datetime

        if recurrence_type == PaymentRecurrenceType.ONE_TIME:
            occurrences.append(current)

        elif total_occurrences is not None:
            for _ in range(total_occurrences):
                occurrences.append(current)
                current = self._compute_next_due(
                    current=current,
                    recurrence_type=recurrence_type,
                    interval_days=interval_days,
                    day_of_month_anchor=day_of_month_anchor,
                )

        else:
            one_year_ahead = start_datetime + timedelta(days=365)
            while current <= one_year_ahead:
                occurrences.append(current)
                current = self._compute_next_due(
                    current=current,
                    recurrence_type=recurrence_type,
                    interval_days=interval_days,
                    day_of_month_anchor=day_of_month_anchor,
                )

        for due_datetime in occurrences:
            command = CreatePaymentOccurrenceInputDTOV1(
                payment_uuid=payment_uuid,
                user_uuid=user_uuid,
                due_datetime=due_datetime,
                status_type=PaymentOccurrenceStatusType.UNPAID if payment_type == PaymentType.EXPENSE else None,
            )
            await self.create_payment_occurrence(input_dto=command)

    def _compute_next_due(
        self,
        current: datetime,
        recurrence_type: PaymentRecurrenceType,
        interval_days: int | None,
        day_of_month_anchor: int | None,
    ) -> datetime:
        if recurrence_type == PaymentRecurrenceType.WEEKLY:
            return current + timedelta(days=7)

        elif recurrence_type == PaymentRecurrenceType.CUSTOM:
            return current + timedelta(days=interval_days)

        else:
            j = jdatetime.datetime.fromgregorian(datetime=current)
            next_month = j.month + 1
            next_year = j.year
            if next_month > 12:
                next_month = 1
                next_year += 1
            max_day = jdatetime.date(next_year, next_month, 29).day
            for d in [31, 30, 29]:
                try:
                    jdatetime.date(next_year, next_month, d)
                    max_day = d
                    break
                except ValueError:
                    continue
            day = min(day_of_month_anchor, max_day)
            return j.replace(year=next_year, month=next_month, day=day).togregorian()

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_payment(self, input_dto: GetPaymentInputDTOV1) -> GetPaymentOutputDTOV1:
        query = GetPaymentQueryDTO.model_validate(obj=input_dto)
        response: GetPaymentResponseDTO = await self._repository.get_payment(input_dto=query)
        return GetPaymentOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def search_payments(self, input_dto: SearchPaymentInputDTOV1) -> SearchPaymentOutputDTOV1:
        repository_dto = SearchPaymentQueryDTO.model_validate(input_dto)
        response: SearchPaymentResponseDTO = await self._repository.search_payments(input_dto=repository_dto)
        return SearchPaymentOutputDTOV1.model_validate(response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def update_payment(self, input_dto: UpdatePaymentInputDTOV1) -> None:
        command = UpdatePaymentCommandDTO.model_validate(obj=input_dto)
        await self._repository.update_payment(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def delete_payment(self, input_dto: DeletePaymentInputDTOV1) -> None:
        search_payment_occurrences_input_dto = SearchPaymentOccurrenceInputDTOV1(
            payment_uuid=input_dto.payment_uuid,
        )
        payment_occurrences: SearchPaymentOccurrenceOutputDTOV1 = await self.search_payment_occurrences(
            input_dto=search_payment_occurrences_input_dto,
        )
        for occurrence in payment_occurrences.payment_occurrences:
            await self.delete_payment_occurrence(
                input_dto=DeletePaymentOccurrenceInputDTOV1(
                    payment_occurrence_uuid=occurrence.payment_occurrence_uuid,
                ),
            )
        command = DeletePaymentCommandDTO.model_validate(obj=input_dto)
        await self._repository.delete_payment(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def create_payment_occurrence(
        self,
        input_dto: CreatePaymentOccurrenceInputDTOV1,
    ) -> CreatePaymentOccurrenceOutputDTOV1:
        command = CreatePaymentOccurrenceCommandDTO.model_validate(input_dto)
        response: CreatePaymentOccurrenceResponseDTO = await self._repository.create_payment_occurrence(
            input_dto=command,
        )
        return CreatePaymentOccurrenceOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_payment_occurrence(
        self,
        input_dto: GetPaymentOccurrenceInputDTOV1,
    ) -> GetPaymentOccurrenceOutputDTOV1:
        query = GetPaymentOccurrenceQueryDTO.model_validate(obj=input_dto)
        response: GetPaymentOccurrenceResponseDTO = await self._repository.get_payment_occurrence(input_dto=query)
        return GetPaymentOccurrenceOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def search_payment_occurrences(
        self,
        input_dto: SearchPaymentOccurrenceInputDTOV1,
    ) -> SearchPaymentOccurrenceOutputDTOV1:
        repository_dto = SearchPaymentOccurrenceQueryDTO.model_validate(input_dto)
        response: SearchPaymentOccurrenceResponseDTO = await self._repository.search_payment_occurrences(
            input_dto=repository_dto,
        )
        return SearchPaymentOccurrenceOutputDTOV1.model_validate(response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def update_payment_occurrence(self, input_dto: UpdatePaymentOccurrenceInputDTOV1) -> None:
        command = UpdatePaymentOccurrenceCommandDTO.model_validate(obj=input_dto)
        await self._repository.update_payment_occurrence(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def delete_payment_occurrence(self, input_dto: DeletePaymentOccurrenceInputDTOV1) -> None:
        command = DeletePaymentOccurrenceCommandDTO.model_validate(obj=input_dto)
        await self._repository.delete_payment_occurrence(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_balance(self, input_dto: GetBalanceInputDTOV1) -> GetBalanceOutputDTOV1:
        query_dto = GetBalanceQueryDTO.model_validate(input_dto)
        response: GetBalanceResponseDTO = await self._repository.get_balance(input_dto=query_dto)
        return GetBalanceOutputDTOV1(
            total_income=response.total_income,
            total_expense=response.total_expense,
            balance=response.total_income - response.total_expense,
        )
