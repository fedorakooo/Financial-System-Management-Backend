from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

from src.domain.enums.account import AccountStatus, AccountType


class AccountCreateRequest(BaseModel):
    bank_id: int


class AccountUpdateRequest(BaseModel):
    status: AccountStatus


class AccountResponse(BaseModel):
    id: int
    user_id: int
    bank_id: int
    balance: Decimal
    status: AccountStatus
    type: AccountType
    created_at: datetime
    updated_at: datetime
