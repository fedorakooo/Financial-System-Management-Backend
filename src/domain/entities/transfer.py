from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src.domain.enums.transfer import TransferStatus


@dataclass(frozen=True)
class Transfer:
    from_account_id: int
    to_account_id: int
    amount: Decimal("0.00")
    id: int = None
    status: TransferStatus = TransferStatus.COMPLETED
    updated_at: datetime = None
    created_at: datetime = None
