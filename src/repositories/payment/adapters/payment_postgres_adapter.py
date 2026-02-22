from archipy.adapters.base.sqlalchemy.adapters import SQLAlchemyFilterMixin
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.models.errors import NotFoundError
from archipy.models.types.base_types import FilterOperationType
from sqlalchemy import delete, select, update, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import Select, Update

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
from src.models.entities import PaymentEntity, PaymentOccurrenceEntity
from src.models.types.enums import PaymentType


class PaymentPostgresAdapter(SQLAlchemyFilterMixin):
    def __init__(self, adapter: AsyncPostgresSQLAlchemyAdapter) -> None:
        self._adapter: AsyncPostgresSQLAlchemyAdapter = adapter

    async def create_payment(self, input_dto: CreatePaymentCommandDTO) -> CreatePaymentResponseDTO:
        _entity = PaymentEntity(**input_dto.model_dump())
        result = await self._adapter.create(entity=_entity)
        return CreatePaymentResponseDTO.model_validate(obj=result)

    async def get_payment(self, input_dto: GetPaymentQueryDTO) -> GetPaymentResponseDTO:
        select_query = select(PaymentEntity).where(PaymentEntity.is_deleted.is_(False))
        _query = self._apply_filter(
            query=select_query,
            field=PaymentEntity.payment_uuid,
            value=input_dto.payment_uuid,
            operation=FilterOperationType.EQUAL,
        )
        result = await self._adapter.execute(statement=_query)
        entity = result.scalar()

        if not entity:
            raise NotFoundError(resource_type=PaymentEntity.__name__)

        return GetPaymentResponseDTO.model_validate(obj=entity)

    async def search_payments(self, input_dto: SearchPaymentQueryDTO) -> SearchPaymentResponseDTO:
        query: Select = select(PaymentEntity).where(PaymentEntity.is_deleted.is_(False))

        if input_dto.user_uuid:
            query = self._apply_filter(
                query=query,
                field=PaymentEntity.user_uuid,
                value=input_dto.user_uuid,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.payment_type:
            query = self._apply_filter(
                query=query,
                field=PaymentEntity.payment_type,
                value=input_dto.payment_type,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.category_types:
            query = self._apply_filter(
                query=query,
                field=PaymentEntity.category_type,
                value=input_dto.category_types,
                operation=FilterOperationType.IN_LIST,
            )

        if input_dto.recurrence_types:
            query = self._apply_filter(
                query=query,
                field=PaymentEntity.recurrence_type,
                value=input_dto.recurrence_types,
                operation=FilterOperationType.IN_LIST,
            )

        if input_dto.is_active is not None:
            query = self._apply_filter(
                query=query,
                field=PaymentEntity.is_active,
                value=input_dto.is_active,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.start_datetime:
            start_min, start_max = input_dto.start_datetime
            query = self._apply_filter(
                query=query,
                field=PaymentEntity.start_datetime,
                value=start_min,
                operation=FilterOperationType.GREATER_THAN_OR_EQUAL,
            )
            query = self._apply_filter(
                query=query,
                field=PaymentEntity.start_datetime,
                value=start_max,
                operation=FilterOperationType.LESS_THAN_OR_EQUAL,
            )

        entities, total = await self._adapter.execute_search_query(
            query=query,
            entity=PaymentEntity,
            sort_info=input_dto.sort_info,
            pagination=input_dto.pagination,
        )

        return SearchPaymentResponseDTO(payments=entities, total=total)

    async def update_payment(self, input_dto: UpdatePaymentCommandDTO) -> None:
        update_data = input_dto.model_dump(exclude={"payment_uuid"}, exclude_none=True)
        if not update_data:
            return

        update_query: Update = (
            update(PaymentEntity)
            .where(
                PaymentEntity.payment_uuid == input_dto.payment_uuid,
                PaymentEntity.is_deleted.is_(False),
            )
            .values(**update_data)
        )

        result = await self._adapter.execute(statement=update_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=PaymentEntity.__name__)

    async def delete_payment(self, input_dto: DeletePaymentCommandDTO) -> None:
        delete_query = (
            update(PaymentEntity)
            .where(
                PaymentEntity.payment_uuid == input_dto.payment_uuid,
                PaymentEntity.is_deleted.is_(False),
            )
            .values(is_deleted=True)
        )

        result = await self._adapter.execute(statement=delete_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=PaymentEntity.__name__)

    async def create_payment_occurrence(
        self,
        input_dto: CreatePaymentOccurrenceCommandDTO,
    ) -> CreatePaymentOccurrenceResponseDTO:
        _entity = PaymentOccurrenceEntity(**input_dto.model_dump())
        result = await self._adapter.create(entity=_entity)
        return CreatePaymentOccurrenceResponseDTO.model_validate(obj=result)

    async def get_payment_occurrence(self, input_dto: GetPaymentOccurrenceQueryDTO) -> GetPaymentOccurrenceResponseDTO:
        select_query = select(PaymentOccurrenceEntity).where(PaymentOccurrenceEntity.is_deleted.is_(False))
        _query = self._apply_filter(
            query=select_query,
            field=PaymentOccurrenceEntity.payment_occurrence_uuid,
            value=input_dto.payment_occurrence_uuid,
            operation=FilterOperationType.EQUAL,
        )
        result = await self._adapter.execute(statement=_query)
        entity = result.scalar()

        if not entity:
            raise NotFoundError(resource_type=PaymentOccurrenceEntity.__name__)

        return GetPaymentOccurrenceResponseDTO.model_validate(obj=entity)

    async def search_payment_occurrences(
        self,
        input_dto: SearchPaymentOccurrenceQueryDTO,
    ) -> SearchPaymentOccurrenceResponseDTO:
        query: Select = select(PaymentOccurrenceEntity).where(PaymentOccurrenceEntity.is_deleted.is_(False))

        if input_dto.user_uuid:
            query = self._apply_filter(
                query=query,
                field=PaymentOccurrenceEntity.user_uuid,
                value=input_dto.user_uuid,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.payment_uuid:
            query = self._apply_filter(
                query=query,
                field=PaymentOccurrenceEntity.payment_uuid,
                value=input_dto.payment_uuid,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.status_type:
            query = self._apply_filter(
                query=query,
                field=PaymentOccurrenceEntity.status_type,
                value=input_dto.status_type,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.due_datetime:
            due_min, due_max = input_dto.due_datetime
            query = self._apply_filter(
                query=query,
                field=PaymentOccurrenceEntity.due_datetime,
                value=due_min,
                operation=FilterOperationType.GREATER_THAN_OR_EQUAL,
            )
            query = self._apply_filter(
                query=query,
                field=PaymentOccurrenceEntity.due_datetime,
                value=due_max,
                operation=FilterOperationType.LESS_THAN_OR_EQUAL,
            )

        if input_dto.paid_at:
            paid_min, paid_max = input_dto.paid_at
            query = self._apply_filter(
                query=query,
                field=PaymentOccurrenceEntity.paid_at,
                value=paid_min,
                operation=FilterOperationType.GREATER_THAN_OR_EQUAL,
            )
            query = self._apply_filter(
                query=query,
                field=PaymentOccurrenceEntity.paid_at,
                value=paid_max,
                operation=FilterOperationType.LESS_THAN_OR_EQUAL,
            )

        if input_dto.pagination:
            entities, total = await self._adapter.execute_search_query(
                query=query,
                entity=PaymentOccurrenceEntity,
                sort_info=input_dto.sort_info,
                pagination=input_dto.pagination,
            )
        else:
            result = await self._adapter.execute(query)
            entities = result.scalars().all()
            total = len(entities)

        return SearchPaymentOccurrenceResponseDTO(payment_occurrences=entities, total=total)

    async def update_payment_occurrence(self, input_dto: UpdatePaymentOccurrenceCommandDTO) -> None:
        update_data = input_dto.model_dump(exclude={"payment_occurrence_uuid"}, exclude_none=True)
        if not update_data:
            return

        update_query: Update = (
            update(PaymentOccurrenceEntity)
            .where(
                PaymentOccurrenceEntity.payment_occurrence_uuid == input_dto.payment_occurrence_uuid,
                PaymentOccurrenceEntity.is_deleted.is_(False),
            )
            .values(**update_data)
        )

        result = await self._adapter.execute(statement=update_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=PaymentOccurrenceEntity.__name__)

    async def delete_payment_occurrence(self, input_dto: DeletePaymentOccurrenceCommandDTO) -> None:
        delete_query = (
            update(PaymentOccurrenceEntity)
            .where(
                PaymentOccurrenceEntity.payment_occurrence_uuid == input_dto.payment_occurrence_uuid,
                PaymentOccurrenceEntity.is_deleted.is_(False),
            )
            .values(is_deleted=True)
        )

        result = await self._adapter.execute(statement=delete_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=PaymentOccurrenceEntity.__name__)

    async def get_balance(self, input_dto: GetBalanceQueryDTO) -> GetBalanceResponseDTO:
        total_income_col = func.coalesce(
            func.sum(PaymentEntity.amount).filter(PaymentEntity.payment_type == PaymentType.INCOME),
            0,
        ).label("total_income")

        total_expense_col = func.coalesce(
            func.sum(PaymentEntity.amount).filter(PaymentEntity.payment_type == PaymentType.EXPENSE),
            0,
        ).label("total_expense")

        query = (
            select(total_income_col, total_expense_col)
            .select_from(PaymentOccurrenceEntity)
            .join(PaymentEntity, PaymentEntity.payment_uuid == PaymentOccurrenceEntity.payment_uuid)
            .where(
                PaymentOccurrenceEntity.is_deleted.is_(False),
                PaymentEntity.is_deleted.is_(False),
                PaymentEntity.user_uuid == input_dto.user_uuid,
            )
        )

        if input_dto.payment_type:
            query = query.where(PaymentEntity.payment_type == input_dto.payment_type)

        if input_dto.category_types:
            query = query.where(PaymentEntity.category_type.in_(input_dto.category_types))

        if input_dto.recurrence_types:
            query = query.where(PaymentEntity.recurrence_type.in_(input_dto.recurrence_types))

        if input_dto.is_active is not None:
            query = query.where(PaymentEntity.is_active == input_dto.is_active)

        if input_dto.status_type:
            query = query.where(PaymentOccurrenceEntity.status_type == input_dto.status_type)

        if input_dto.due_datetime:
            due_min, due_max = input_dto.due_datetime
            query = query.where(PaymentOccurrenceEntity.due_datetime >= due_min)
            query = query.where(PaymentOccurrenceEntity.due_datetime <= due_max)

        result = await self._adapter.execute(statement=query)
        row = result.one()

        return GetBalanceResponseDTO(total_income=row.total_income, total_expense=row.total_expense)
