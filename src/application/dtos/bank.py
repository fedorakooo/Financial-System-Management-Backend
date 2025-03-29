from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class BankReadDTO:
    id: int
    name: str
    bic: str
    address: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class BankCreateDTO:
    name: str
    bic: str
    address: str


@dataclass(frozen=True)
class BankUpdateDTO:
    name: Optional[str]
    address: Optional[str]
