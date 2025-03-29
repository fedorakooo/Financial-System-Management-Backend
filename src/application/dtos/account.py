from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from src.domain.enums.account import AccountStatus, AccountType


@dataclass(frozen=True)
class AccountReadDTO:
    id: int
    user_id: int
    bank_id: int
    balance: Decimal
    status: AccountStatus
    type: AccountType
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class AccountCreateDTO:
    user_id: int
    bank_id: int


@dataclass(frozen=True)
class AccountUpdateClientDTO:
    status: Optional[AccountStatus]


@dataclass(frozen=True)
class AccountUpdateStaffDTO:
    status: Optional[AccountStatus]
