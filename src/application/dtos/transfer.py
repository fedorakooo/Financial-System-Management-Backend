from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src.domain.enums.transfer import TransferStatus


@dataclass(frozen=True)
class TransferReadDTO:
    from_account_id: int
    to_account_id: int
    amount: Decimal("0.00")
    id: int
    status: TransferStatus
    updated_at: datetime
    created_at: datetime


@dataclass(frozen=True)
class TransferCreateDTO:
    from_account_id: int
    to_account_id: int
    amount: Decimal("0.00")
