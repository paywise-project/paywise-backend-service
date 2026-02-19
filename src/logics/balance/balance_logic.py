from typing import Tuple
from uuid import UUID


from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator

from src.logics.payment.payment_logic import PaymentLogic
from src.models.dtos.balance.domain.v1.balance_domain_interface_dtos import GetBalanceOutputDTOV1


from src.utils.date_utils import DateUtils


class BalanceLogic:
    def __init__(
        self,
        payment_logic: PaymentLogic,
    ) -> None:
        self.payment_logic = payment_logic

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_balance(self, user_uuid: UUID) -> GetBalanceOutputDTOV1:
        income_input_dto = GetTotalIncomeInputDTOV1(
            user_uuid=user_uuid,
            is_active=True,
        )
        total_income_dto = await self.income_logic.get_total_income(input_dto=income_input_dto)
        total_income = total_income_dto.total_income_amount
        expense_input_dto = GetTotalExpenseInputDTOV1(
            user_uuid=user_uuid,
            is_active=True,
        )
        total_expense_dto = await self.expense_logic.get_total_expense(input_dto=expense_input_dto)
        total_expense = total_expense_dto.total_expense_amount
        monthly_balance = total_income - total_expense
        return GetBalanceOutputDTOV1(
            monthly_balance=monthly_balance,
            total_expense=total_expense,
            total_income=total_income,
        )

        # min_day = DateUtils.get_today_day_in_jalali()
        # max_day = min_day + 7
        # max_day = max_day if max_day <= 29 else max_day - 29
        # days = (min_day, max_day),
