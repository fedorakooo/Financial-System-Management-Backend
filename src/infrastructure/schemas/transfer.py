from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

from src.domain.enums.transfer import TransferStatus


class TransferResponse(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: Decimal
    id: int
    status: TransferStatus
    updated_at: datetime
    created_at: datetime


class TransferCreateRequest(BaseModel):
    amount: Decimal
    to_account_id: int
