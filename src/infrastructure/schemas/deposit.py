from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from src.domain.enums.deposit import DepositTransactionType
from src.infrastructure.schemas.account import AccountResponse


class DepositAccountCreateRequest(BaseModel):
    amount: Decimal
    interest_rate: Decimal
    from_account_id: int


class DepositAccountResponse(BaseModel):
    interest_rate: Decimal
    id: int
    account: AccountResponse
    from_account_id: int


class DepositTransactionResponse(BaseModel):
    id: int
    deposit_account_id: int
    type: DepositTransactionType
    amount: Decimal
    created_at: Optional[datetime] = None


class DepositTransactionCreateClientRequest(BaseModel):
    account_id: int
