from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

from src.domain.enums.withdrawal import WithdrawalSource


class WithdrawalResponse(BaseModel):
    id: int
    amount: Decimal = Decimal("0.00")
    source: WithdrawalSource
    account_id: int
    created_at: datetime


class WithdrawalCreateRequest(BaseModel):
    amount: Decimal = Decimal("0.00")
    source: WithdrawalSource
