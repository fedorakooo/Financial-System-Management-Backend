from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from src.domain.enums.loan import LoanTermMonths, LoanTransactionType


@dataclass(frozen=True)
class Loan:
    amount: Decimal("0.00")
    term_months: LoanTermMonths
    interest_rate: Decimal
    id: Optional[int] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None


@dataclass(frozen=True)
class LoanAccount:
    account_id: int
    loan_id: int
    user_id: int
    id: Optional[int] = None


@dataclass(frozen=True)
class LoanTransaction:
    loan_account_id: int
    type: LoanTransactionType
    amount: Decimal("0.00")
    id: Optional[int] = None
    created_at: Optional[datetime] = None
