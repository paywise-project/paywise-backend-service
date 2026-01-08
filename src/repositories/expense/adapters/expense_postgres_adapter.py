from archipy.adapters.base.sqlalchemy.adapters import SQLAlchemyFilterMixin
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.models.errors import NotFoundError
from archipy.models.types.base_types import FilterOperationType
from sqlalchemy import delete, select, update, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import Select, Update

from src.models.dtos.expense.repository.expense_repository_interface_dtos import (
    CreateExpenseCommandDTO,
    CreateExpenseResponseDTO,
    GetExpenseQueryDTO,
    GetExpenseResponseDTO,
    UpdateExpenseCommandDTO,
    DeleteExpenseCommandDTO,
    SearchExpenseQueryDTO,
    SearchExpenseResponseDTO,
)
from src.models.entities import ExpenseEntity


class ExpensePostgresAdapter(SQLAlchemyFilterMixin):
    def __init__(self, adapter: AsyncPostgresSQLAlchemyAdapter) -> None:
        self._adapter: AsyncPostgresSQLAlchemyAdapter = adapter

    async def create_expense(self, input_dto: CreateExpenseCommandDTO) -> CreateExpenseResponseDTO:
        _entity = ExpenseEntity(**input_dto.model_dump())
        result = await self._adapter.create(entity=_entity)
        return CreateExpenseResponseDTO.model_validate(obj=result)

    async def get_expense(self, input_dto: GetExpenseQueryDTO) -> GetExpenseResponseDTO:
        select_query = select(ExpenseEntity).where(ExpenseEntity.is_deleted.is_(False))
        _query = self._apply_filter(
            query=select_query,
            field=ExpenseEntity.expense_uuid,
            value=input_dto.expense_uuid,
            operation=FilterOperationType.EQUAL,
        )
        result = await self._adapter.execute(statement=_query)
        entity = result.scalar()

        if not entity:
            raise NotFoundError(resource_type=ExpenseEntity.__name__)

        return GetExpenseResponseDTO.model_validate(obj=entity)

    async def search_expenses(self, input_dto: SearchExpenseQueryDTO) -> SearchExpenseResponseDTO:
        query: Select = select(ExpenseEntity).where(ExpenseEntity.is_deleted.is_(False))

        if input_dto.user_uuid:
            query = self._apply_filter(
                query=query,
                field=ExpenseEntity.user_uuid,
                value=input_dto.user_uuid,
                operation=FilterOperationType.EQUAL,
            )

        entities, total = await self._adapter.execute_search_query(
            query=query,
            entity=ExpenseEntity,
            sort_info=input_dto.sort_info,
            pagination=input_dto.pagination,
        )

        return SearchExpenseResponseDTO(expenses=entities, total=total)

    async def update_expense(self, input_dto: UpdateExpenseCommandDTO) -> None:
        update_data = input_dto.model_dump(exclude={"expense_uuid"}, exclude_none=True)
        if not update_data:
            return

        update_query: Update = (
            update(ExpenseEntity)
            .where(
                ExpenseEntity.expense_uuid == input_dto.expense_uuid,
                ExpenseEntity.is_deleted.is_(False),
            )
            .values(**update_data)
        )

        result = await self._adapter.execute(statement=update_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=ExpenseEntity.__name__)

    async def delete_expense(self, input_dto: DeleteExpenseCommandDTO) -> None:
        delete_query = (
            update(ExpenseEntity)
            .where(
                ExpenseEntity.expense_uuid == input_dto.expense_uuid,
                ExpenseEntity.is_deleted.is_(False),
            )
            .values(is_deleted=True)
        )

        result = await self._adapter.execute(statement=delete_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=ExpenseEntity.__name__)
