from archipy.adapters.base.sqlalchemy.adapters import SQLAlchemyFilterMixin
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.models.errors import NotFoundError
from archipy.models.types.base_types import FilterOperationType
from sqlalchemy import select, update
from sqlalchemy.sql.expression import Select, Update

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
from src.models.entities import IncomeEntity


class IncomePostgresAdapter(SQLAlchemyFilterMixin):
    def __init__(self, adapter: AsyncPostgresSQLAlchemyAdapter) -> None:
        self._adapter: AsyncPostgresSQLAlchemyAdapter = adapter

    async def create_income(self, input_dto: CreateIncomeCommandDTO) -> CreateIncomeResponseDTO:
        _entity = IncomeEntity(**input_dto.model_dump())
        result = await self._adapter.create(entity=_entity)
        return CreateIncomeResponseDTO.model_validate(obj=result)

    async def get_income(self, input_dto: GetIncomeQueryDTO) -> GetIncomeResponseDTO:
        select_query = select(IncomeEntity).where(IncomeEntity.is_deleted.is_(False))
        _query = self._apply_filter(
            query=select_query,
            field=IncomeEntity.income_uuid,
            value=input_dto.income_uuid,
            operation=FilterOperationType.EQUAL,
        )
        result = await self._adapter.execute(statement=_query)
        entity = result.scalar()

        if not entity:
            raise NotFoundError(resource_type=IncomeEntity.__name__)

        return GetIncomeResponseDTO.model_validate(obj=entity)

    async def search_incomes(self, input_dto: SearchIncomeQueryDTO) -> SearchIncomeResponseDTO:
        query: Select = select(IncomeEntity).where(IncomeEntity.is_deleted.is_(False))

        if input_dto.user_uuid:
            query = self._apply_filter(
                query=query,
                field=IncomeEntity.user_uuid,
                value=input_dto.user_uuid,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.is_active:
            query = self._apply_filter(
                query=query,
                field=IncomeEntity.is_active,
                value=input_dto.is_active,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.days:
            day_min, day_max = input_dto.days
            query = self._apply_filter(
                query=query,
                field=IncomeEntity.day_of_month,
                value=day_min,
                operation=FilterOperationType.GREATER_THAN_OR_EQUAL,
            )
            query = self._apply_filter(
                query=query,
                field=IncomeEntity.day_of_month,
                value=day_max,
                operation=FilterOperationType.LESS_THAN_OR_EQUAL,
            )

        entities, total = await self._adapter.execute_search_query(
            query=query,
            entity=IncomeEntity,
            sort_info=input_dto.sort_info,
            pagination=input_dto.pagination,
        )

        return SearchIncomeResponseDTO(incomes=entities, total=total)

    async def update_income(self, input_dto: UpdateIncomeCommandDTO) -> None:
        update_data = input_dto.model_dump(exclude={"income_uuid"}, exclude_none=True)
        if not update_data:
            return

        update_query: Update = (
            update(IncomeEntity)
            .where(
                IncomeEntity.income_uuid == input_dto.income_uuid,
                IncomeEntity.is_deleted.is_(False),
            )
            .values(**update_data)
        )

        result = await self._adapter.execute(statement=update_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=IncomeEntity.__name__)

    async def delete_income(self, input_dto: DeleteIncomeCommandDTO) -> None:
        delete_query = (
            update(IncomeEntity)
            .where(
                IncomeEntity.income_uuid == input_dto.income_uuid,
                IncomeEntity.is_deleted.is_(False),
            )
            .values(is_deleted=True)
        )

        result = await self._adapter.execute(statement=delete_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=IncomeEntity.__name__)
