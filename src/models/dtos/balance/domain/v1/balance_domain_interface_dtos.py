from archipy.models.dtos.base_dtos import BaseDTO


class GetBalanceOutputDTOV1(BaseDTO):
    monthly_balance: int
    total_income: int
    total_expense: int
