from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator
from uuid import UUID

from src.models.dtos.expense.domain.v1.expense_domain_interface_dtos import (
    CreateExpenseInputDTOV1,
    CreateExpenseOutputDTOV1,
    GetExpenseInputDTOV1,
    GetExpenseOutputDTOV1,
    UpdateExpenseInputDTOV1,
    DeleteExpenseInputDTOV1,
    SearchExpenseInputDTOV1,
    SearchExpenseOutputDTOV1,
    GetTotalExpenseInputDTOV1,
    GetTotalExpenseOutputDTOV1,
)
from src.models.dtos.expense.repository.expense_repository_interface_dtos import (
    CreateExpenseCommandDTO,
    CreateExpenseResponseDTO,
    GetExpenseQueryDTO,
    GetExpenseResponseDTO,
    UpdateExpenseCommandDTO,
    DeleteExpenseCommandDTO,
    SearchExpenseQueryDTO,
    SearchExpenseResponseDTO,
    GetTotalExpenseQueryDTO,
    GetTotalExpenseResponseDTO,
)
from src.repositories.expense.expense_repository import ExpenseRepository


class ExpenseLogic:
    def __init__(
        self,
        repository: ExpenseRepository,
    ) -> None:
        self._repository: ExpenseRepository = repository

    @async_postgres_sqlalchemy_atomic_decorator
    async def create_expense(self, input_dto: CreateExpenseInputDTOV1) -> CreateExpenseOutputDTOV1:
        command = CreateExpenseCommandDTO.model_validate(input_dto)
        response: CreateExpenseResponseDTO = await self._repository.create_expense(input_dto=command)
        return CreateExpenseOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_expense(self, input_dto: GetExpenseInputDTOV1) -> GetExpenseOutputDTOV1:
        query = GetExpenseQueryDTO.model_validate(obj=input_dto)
        response: GetExpenseResponseDTO = await self._repository.get_expense(input_dto=query)
        return GetExpenseOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def search_expenses(self, input_dto: SearchExpenseInputDTOV1) -> SearchExpenseOutputDTOV1:
        repository_dto = SearchExpenseQueryDTO.model_validate(input_dto)
        response: SearchExpenseResponseDTO = await self._repository.search_expenses(input_dto=repository_dto)
        return SearchExpenseOutputDTOV1.model_validate(response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def update_expense(self, input_dto: UpdateExpenseInputDTOV1) -> None:
        command = UpdateExpenseCommandDTO.model_validate(obj=input_dto)
        await self._repository.update_expense(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def delete_expense(self, input_dto: DeleteExpenseInputDTOV1) -> None:
        command = DeleteExpenseCommandDTO.model_validate(obj=input_dto)
        await self._repository.delete_expense(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_total_expense(self, input_dto: GetTotalExpenseInputDTOV1) -> GetTotalExpenseOutputDTOV1:
        query = GetTotalExpenseQueryDTO.model_validate(obj=input_dto)
        response: GetTotalExpenseResponseDTO = await self._repository.get_total_expense(input_dto=query)
        return GetTotalExpenseOutputDTOV1.model_validate(obj=response)
