from typing import Tuple
from uuid import UUID


from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator

from src.logics.payment.payment_logic import PaymentLogic
from src.models.dtos.balance.domain.v1.balance_domain_interface_dtos import GetBalanceOutputDTOV1, GetBalanceInputDTOV1

from src.utils.date_utils import DateUtils


class BalanceLogic:
    def __init__(
        self,
        payment_logic: PaymentLogic,
    ) -> None:
        self._payment_logic = payment_logic

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_balance(self, input_dto: GetBalanceInputDTOV1) -> GetBalanceOutputDTOV1:
        response = await self._payment_logic.get_balance(input_dto=input_dto)
        return GetBalanceOutputDTOV1(
            total_income=response.total_income,
            total_expense=response.total_expense,
            balance=response.total_income - response.total_expense,
        )
