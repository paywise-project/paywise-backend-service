from archipy.adapters.base.sqlalchemy.adapters import SQLAlchemyFilterMixin
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.models.errors import NotFoundError
from archipy.models.types.base_types import FilterOperationType
from sqlalchemy import select, update
from sqlalchemy.sql.expression import Select, Update
from sqlalchemy.sql.functions import func

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

        if input_dto.categories:
            query = self._apply_filter(
                query=query,
                field=ExpenseEntity.category,
                value=input_dto.categories,
                operation=FilterOperationType.IN_LIST,
            )

        if input_dto.status_type:
            query = self._apply_filter(
                query=query,
                field=ExpenseEntity.status_type,
                value=input_dto.status_type,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.is_active:
            query = self._apply_filter(
                query=query,
                field=ExpenseEntity.is_active,
                value=input_dto.is_active,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.days:
            day_min, day_max = input_dto.days
            query = self._apply_filter(
                query=query,
                field=ExpenseEntity.day_of_month,
                value=day_min,
                operation=FilterOperationType.GREATER_THAN_OR_EQUAL,
            )
            query = self._apply_filter(
                query=query,
                field=ExpenseEntity.day_of_month,
                value=day_max,
                operation=FilterOperationType.LESS_THAN_OR_EQUAL,
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

    async def get_total_expense(self, input_dto: GetTotalExpenseQueryDTO) -> GetTotalExpenseResponseDTO:
        query = select(func.coalesce(func.sum(ExpenseEntity.amount), 0)).where(ExpenseEntity.is_deleted.is_(False))

        if input_dto.user_uuid:
            query = self._apply_filter(
                query=query,
                field=ExpenseEntity.user_uuid,
                value=input_dto.user_uuid,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.categories:
            query = self._apply_filter(
                query=query,
                field=ExpenseEntity.category,
                value=input_dto.categories,
                operation=FilterOperationType.IN_LIST,
            )

        if input_dto.status_type:
            query = self._apply_filter(
                query=query,
                field=ExpenseEntity.status_type,
                value=input_dto.status_type,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.is_active is not None:
            query = self._apply_filter(
                query=query,
                field=ExpenseEntity.is_active,
                value=input_dto.is_active,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.days:
            day_min, day_max = input_dto.days
            query = self._apply_filter(
                query=query,
                field=ExpenseEntity.day_of_month,
                value=day_min,
                operation=FilterOperationType.GREATER_THAN_OR_EQUAL,
            )
            query = self._apply_filter(
                query=query,
                field=ExpenseEntity.day_of_month,
                value=day_max,
                operation=FilterOperationType.LESS_THAN_OR_EQUAL,
            )

        result = await self._adapter.execute(statement=query)
        total_amount = result.scalar_one()

        return GetTotalExpenseResponseDTO(total_expense_amount=total_amount)
