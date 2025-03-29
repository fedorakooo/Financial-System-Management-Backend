from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src.domain.enums.withdrawal import WithdrawalSource


@dataclass(frozen=True)
class WithdrawalReadDTO:
    id: int
    account_id: int
    amount: Decimal("0.00")
    source: WithdrawalSource
    created_at: datetime


@dataclass(frozen=True)
class WithdrawalCreateDTO:
    account_id: int
    amount: Decimal("0.00")
    source: WithdrawalSource
