from src.models.dtos.income.repository.income_repository_interface_dtos import (
    CreateIncomeCommandDTO,
    CreateIncomeResponseDTO,
    GetIncomeQueryDTO,
    GetIncomeResponseDTO,
    UpdateIncomeCommandDTO,
    DeleteIncomeCommandDTO,
    SearchIncomeQueryDTO,
    SearchIncomeResponseDTO,
)
from src.repositories.income.adapters.income_postgres_adapter import IncomePostgresAdapter


class IncomeRepository:
    def __init__(self, postgres_adapter: IncomePostgresAdapter):
        self._postgres_adapter: IncomePostgresAdapter = postgres_adapter

    async def create_income(self, input_dto: CreateIncomeCommandDTO) -> CreateIncomeResponseDTO:
        return await self._postgres_adapter.create_income(input_dto=input_dto)

    async def get_income(self, input_dto: GetIncomeQueryDTO) -> GetIncomeResponseDTO:
        return await self._postgres_adapter.get_income(input_dto=input_dto)

    async def search_incomes(self, input_dto: SearchIncomeQueryDTO) -> SearchIncomeResponseDTO:
        return await self._postgres_adapter.search_incomes(input_dto=input_dto)

    async def update_income(self, input_dto: UpdateIncomeCommandDTO) -> None:
        await self._postgres_adapter.update_income(input_dto=input_dto)

    async def delete_income(self, input_dto: DeleteIncomeCommandDTO) -> None:
        await self._postgres_adapter.delete_income(input_dto=input_dto)
