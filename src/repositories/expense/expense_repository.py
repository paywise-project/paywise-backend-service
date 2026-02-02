from src.models.dtos.expense.repository.expense_repository_interface_dtos import (
    CreateExpenseCommandDTO,
    CreateExpenseResponseDTO,
    GetExpenseQueryDTO,
    GetExpenseResponseDTO,
    UpdateExpenseCommandDTO,
    DeleteExpenseCommandDTO,
    SearchExpenseQueryDTO,
    SearchExpenseResponseDTO,
    GetTotalExpenseResponseDTO,
    GetTotalExpenseQueryDTO,
)
from src.repositories.expense.adapters.expense_postgres_adapter import ExpensePostgresAdapter


class ExpenseRepository:
    def __init__(self, postgres_adapter: ExpensePostgresAdapter):
        self._postgres_adapter: ExpensePostgresAdapter = postgres_adapter

    async def create_expense(self, input_dto: CreateExpenseCommandDTO) -> CreateExpenseResponseDTO:
        return await self._postgres_adapter.create_expense(input_dto=input_dto)

    async def get_expense(self, input_dto: GetExpenseQueryDTO) -> GetExpenseResponseDTO:
        return await self._postgres_adapter.get_expense(input_dto=input_dto)

    async def search_expenses(self, input_dto: SearchExpenseQueryDTO) -> SearchExpenseResponseDTO:
        return await self._postgres_adapter.search_expenses(input_dto=input_dto)

    async def update_expense(self, input_dto: UpdateExpenseCommandDTO) -> None:
        await self._postgres_adapter.update_expense(input_dto=input_dto)

    async def delete_expense(self, input_dto: DeleteExpenseCommandDTO) -> None:
        await self._postgres_adapter.delete_expense(input_dto=input_dto)

    async def get_total_expense(self, input_dto: GetTotalExpenseQueryDTO) -> GetTotalExpenseResponseDTO:
        return await self._postgres_adapter.get_total_expense(input_dto=input_dto)
