from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator
from uuid import UUID

from src.models.dtos.income.domain.v1.income_domain_interface_dtos import (
    CreateIncomeInputDTOV1,
    CreateIncomeOutputDTOV1,
    GetIncomeInputDTOV1,
    GetIncomeOutputDTOV1,
    UpdateIncomeInputDTOV1,
    DeleteIncomeInputDTOV1,
    SearchIncomeInputDTOV1,
    SearchIncomeOutputDTOV1,
)
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
from src.repositories.income.income_repository import IncomeRepository


class IncomeLogic:
    def __init__(
        self,
        repository: IncomeRepository,
    ) -> None:
        self._repository: IncomeRepository = repository

    @async_postgres_sqlalchemy_atomic_decorator
    async def create_income(self, input_dto: CreateIncomeInputDTOV1) -> CreateIncomeOutputDTOV1:
        command = CreateIncomeCommandDTO.model_validate(input_dto)
        response: CreateIncomeResponseDTO = await self._repository.create_income(input_dto=command)
        return CreateIncomeOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_income(self, input_dto: GetIncomeInputDTOV1) -> GetIncomeOutputDTOV1:
        query = GetIncomeQueryDTO.model_validate(obj=input_dto)
        response: GetIncomeResponseDTO = await self._repository.get_income(input_dto=query)
        return GetIncomeOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def search_incomes(self, input_dto: SearchIncomeInputDTOV1) -> SearchIncomeOutputDTOV1:
        repository_dto = SearchIncomeQueryDTO.model_validate(input_dto)
        response: SearchIncomeResponseDTO = await self._repository.search_incomes(input_dto=repository_dto)
        return SearchIncomeOutputDTOV1.model_validate(response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def update_income(self, input_dto: UpdateIncomeInputDTOV1) -> None:
        command = UpdateIncomeCommandDTO.model_validate(obj=input_dto)
        await self._repository.update_income(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def delete_income(self, input_dto: DeleteIncomeInputDTOV1) -> None:
        command = DeleteIncomeCommandDTO.model_validate(obj=input_dto)
        await self._repository.delete_income(input_dto=command)
