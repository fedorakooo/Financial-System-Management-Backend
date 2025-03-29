from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from src.domain.enums.deposit import DepositTransactionType


@dataclass(frozen=True)
class DepositAccount:
    account_id: int
    interest_rate: Decimal("0.00")
    user_id: int
    from_account_id: int
    id: Optional[int] = None



@dataclass(frozen=True)
class DepositTransaction:
    deposit_account_id: int
    account_id: int
    type: DepositTransactionType
    amount: Decimal("0.00")
    id: Optional[int] = None
    created_at: Optional[datetime] = None
