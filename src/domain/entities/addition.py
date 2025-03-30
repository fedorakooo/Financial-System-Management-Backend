from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src.domain.enums.addition import AdditionSource


@dataclass(frozen=True)
class Addition:
    account_id: int
    amount: Decimal
    source: AdditionSource
    id: int | None = None
    created_at: datetime | None = None
