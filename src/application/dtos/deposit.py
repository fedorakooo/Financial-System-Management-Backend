from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src.application.dtos.account import AccountReadDTO
from src.domain.enums.deposit import DepositTransactionType


@dataclass(frozen=True)
class DepositAccountCreateDTO:
    amount: Decimal
    interest_rate: Decimal
    user_id: int
    from_account_id: int


@dataclass(frozen=True)
class DepositAccountReadDTO:
    interest_rate: Decimal
    id: int
    from_account_id: int
    account: AccountReadDTO


@dataclass(frozen=True)
class DepositTransactionReadDTO:
    deposit_account_id: int
    id: int
    account_id: int
    type: DepositTransactionType
    amount: Decimal
    created_at: datetime

@dataclass(frozen=True)
class DepositTransactionCreateClientDTO:
    account_id: int
    deposit_account_id: int
