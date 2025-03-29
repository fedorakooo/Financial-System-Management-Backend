from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

from src.domain.enums.loan import LoanTermMonths, LoanTransactionType
from src.infrastructure.schemas.account import AccountResponse


class LoanCreateRequest(BaseModel):
    amount: Decimal
    term_months: LoanTermMonths
    interest_rate: Decimal


class LoanResponse(BaseModel):
    amount: Decimal
    term_months: LoanTermMonths
    interest_rate: Decimal
    id: int
    updated_at: datetime
    created_at: datetime


class LoanAccountResponse(BaseModel):
    account_id: int
    account: AccountResponse
    loan_id: int
    loan: LoanResponse
    user_id: int
    id: int


class LoanTransactionResponse(BaseModel):
    loan_account_id: int
    type: LoanTransactionType
    amount: Decimal
    id: int
    created_at: datetime


class LoanTransactionCreateRequest(BaseModel):
    amount: Decimal
