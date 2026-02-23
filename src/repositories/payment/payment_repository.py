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
    GetBalanceResponseDTO,
    GetBalanceQueryDTO,
    GetCalendarQueryDTO,
    GetCalendarResponseDTO,
    GetUpcomingPaymentQueryDTO,
    GetUpcomingPaymentResponseDTO,
    GetPaymentOccurrencesForPaymentQueryDTO,
    GetPaymentOccurrencesForPaymentResponseDTO,
)
from src.repositories.payment.adapters.payment_postgres_adapter import PaymentPostgresAdapter


class PaymentRepository:
    def __init__(self, postgres_adapter: PaymentPostgresAdapter):
        self._postgres_adapter: PaymentPostgresAdapter = postgres_adapter

    async def create_payment(self, input_dto: CreatePaymentCommandDTO) -> CreatePaymentResponseDTO:
        return await self._postgres_adapter.create_payment(input_dto=input_dto)

    async def get_payment(self, input_dto: GetPaymentQueryDTO) -> GetPaymentResponseDTO:
        return await self._postgres_adapter.get_payment(input_dto=input_dto)

    async def search_payments(self, input_dto: SearchPaymentQueryDTO) -> SearchPaymentResponseDTO:
        return await self._postgres_adapter.search_payments(input_dto=input_dto)

    async def update_payment(self, input_dto: UpdatePaymentCommandDTO) -> None:
        await self._postgres_adapter.update_payment(input_dto=input_dto)

    async def delete_payment(self, input_dto: DeletePaymentCommandDTO) -> None:
        await self._postgres_adapter.delete_payment(input_dto=input_dto)

    async def create_payment_occurrence(
        self,
        input_dto: CreatePaymentOccurrenceCommandDTO,
    ) -> CreatePaymentOccurrenceResponseDTO:
        return await self._postgres_adapter.create_payment_occurrence(input_dto=input_dto)

    async def get_payment_occurrence(self, input_dto: GetPaymentOccurrenceQueryDTO) -> GetPaymentOccurrenceResponseDTO:
        return await self._postgres_adapter.get_payment_occurrence(input_dto=input_dto)

    async def search_payment_occurrences(
        self,
        input_dto: SearchPaymentOccurrenceQueryDTO,
    ) -> SearchPaymentOccurrenceResponseDTO:
        return await self._postgres_adapter.search_payment_occurrences(input_dto=input_dto)

    async def update_payment_occurrence(self, input_dto: UpdatePaymentOccurrenceCommandDTO) -> None:
        await self._postgres_adapter.update_payment_occurrence(input_dto=input_dto)

    async def delete_payment_occurrence(self, input_dto: DeletePaymentOccurrenceCommandDTO) -> None:
        await self._postgres_adapter.delete_payment_occurrence(input_dto=input_dto)

    async def get_balance(self, input_dto: GetBalanceQueryDTO) -> GetBalanceResponseDTO:
        return await self._postgres_adapter.get_balance(input_dto=input_dto)

    async def get_calendar(self, input_dto: GetCalendarQueryDTO) -> GetCalendarResponseDTO:
        return await self._postgres_adapter.get_calendar(input_dto=input_dto)

    async def get_upcoming_payment(self, input_dto: GetUpcomingPaymentQueryDTO) -> GetUpcomingPaymentResponseDTO | None:
        return await self._postgres_adapter.get_upcoming_payment(input_dto=input_dto)

    async def get_payment_occurrences_for_payment(
        self,
        input_dto: GetPaymentOccurrencesForPaymentQueryDTO,
    ) -> list[GetPaymentOccurrencesForPaymentResponseDTO]:
        return await self._postgres_adapter.get_payment_occurrences_for_payment(input_dto=input_dto)
