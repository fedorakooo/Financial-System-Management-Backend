from datetime import datetime
from pydantic import BaseModel


class BankResponse(BaseModel):
    id: int
    name: str
    bic: str
    address: str
    created_at: datetime
    updated_at: datetime


class BankCreateRequest(BaseModel):
    name: str
    bic: str
    address: str


class BankUpdateRequest(BaseModel):
    name: str
    address: str
