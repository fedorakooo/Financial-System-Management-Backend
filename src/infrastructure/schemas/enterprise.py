from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from src.domain.enums.enterprise import EnterpriseType, EnterprisePayrollRequestStatus
from src.infrastructure.schemas.account import AccountResponse
from src.infrastructure.schemas.user import UserResponse


class EnterpriseResponse(BaseModel):
    name: str
    type: EnterpriseType
    unp: str
    bank_id: int
    address: str
    account: AccountResponse
    id: int
    created_at: datetime
    updated_at: datetime


class EnterpriseCreateRequest(BaseModel):
    name: str
    type: EnterpriseType
    unp: str
    bank_id: int
    address: str


class EnterpriseSpecialistResponse(BaseModel):
    user: UserResponse
    enterprise: EnterpriseResponse
    id: int


class EnterpriseSpecialistCreateRequest(BaseModel):
    enterprise_id: int


class EnterprisePayrollRequestResponse(BaseModel):
    status: EnterprisePayrollRequestStatus
    passport_numbers: list[str]
    accounts_id: list[int]
    enterprise: EnterpriseResponse
    specialist: EnterpriseSpecialistResponse
    created_at: datetime
    amount: Decimal
    updated_at: datetime
    id: int


class EnterprisePayrollRequestCreateRequest(BaseModel):
    passport_numbers: list[str]
    amount: Decimal
    enterprise_id: int
    specialist: int


class EnterprisePayrollTransactionCreateRequest(BaseModel):
    payroll_request_id: int


class EnterprisePayrollTransactionResponse(BaseModel):
    payroll_request_id: int
    created_at: datetime
