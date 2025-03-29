from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

from src.domain.enums.addition import AdditionSource


class AdditionResponse(BaseModel):
    id: int
    amount: Decimal
    source: AdditionSource
    account_id: int
    created_at: datetime


class AdditionCreateRequest(BaseModel):
    amount: Decimal
    source: AdditionSource
