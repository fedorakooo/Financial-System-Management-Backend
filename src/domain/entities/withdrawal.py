from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from src.domain.enums.withdrawal import WithdrawalSource


@dataclass(frozen=True)
class Withdrawal:
    account_id: int
    amount: Decimal
    source: WithdrawalSource
    id: Optional[int] = None
    created_at: Optional[datetime] = None
