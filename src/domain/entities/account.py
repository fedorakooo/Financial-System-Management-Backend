from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src.domain.enums.account import AccountStatus, AccountType


@dataclass(frozen=True)
class Account:
    user_id: int
    bank_id: int
    type: AccountType
    status: AccountStatus
    id: int = None
    balance: Decimal("0.00") = Decimal("0.00")
    created_at: datetime = None
    updated_at: datetime = None
