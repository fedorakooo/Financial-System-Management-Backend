from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src.application.dtos.account import AccountReadDTO
from src.domain.enums.loan import LoanTermMonths, LoanTransactionType


@dataclass(frozen=True)
class LoanCreateDTO:
    amount: Decimal("0.00")
    term_months: LoanTermMonths
    interest_rate: Decimal


@dataclass(frozen=True)
class LoanReadDTO:
    amount: Decimal("0.00")
    term_months: LoanTermMonths
    interest_rate: Decimal
    id: int
    updated_at: datetime
    created_at: datetime


@dataclass(frozen=True)
class LoanAccountReadDTO:
    account_id: int
    account: AccountReadDTO
    loan_id: int
    loan: LoanReadDTO
    user_id: int
    id: int


@dataclass(frozen=True)
class LoanTransactionReadDTO:
    loan_account_id: int
    type: LoanTransactionType
    amount: Decimal("0.00")
    id: int
    created_at: datetime


@dataclass(frozen=True)
class LoanTransactionCreateDTO:
    loan_account_id: int
    amount: Decimal("0.00")
