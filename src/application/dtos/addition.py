from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src.domain.enums.addition import AdditionSource


@dataclass(frozen=True)
class AdditionReadDTO:
    id: int
    account_id: int
    amount: Decimal("0.00")
    source: AdditionSource
    created_at: datetime


@dataclass(frozen=True)
class AdditionCreateDTO:
    account_id: int
    amount: Decimal("0.00")
    source: AdditionSource
