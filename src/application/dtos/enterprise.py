from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src.application.dtos.account import AccountReadDTO
from src.application.dtos.user import UserReadDTO
from src.domain.enums.enterprise import EnterpriseType, EnterprisePayrollRequestStatus


@dataclass(frozen=True)
class EnterpriseReadDTO:
    name: str
    type: EnterpriseType
    unp: str
    bank_id: int
    address: str
    account: AccountReadDTO
    id: int
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class EnterpriseCreateDTO:
    name: str
    type: EnterpriseType
    unp: str
    bank_id: int
    address: str


@dataclass(frozen=True)
class EnterpriseSpecialistReadDTO:
    user: UserReadDTO
    enterprise: EnterpriseReadDTO
    id: int


@dataclass(frozen=True)
class EnterpriseSpecialistCreateDTO:
    user_id: int
    enterprise_id: int


@dataclass(frozen=True)
class EnterprisePayrollRequestReadDTO:
    status: EnterprisePayrollRequestStatus
    passport_numbers: list[str]
    accounts_id: list[int]
    enterprise: EnterpriseReadDTO
    specialist: EnterpriseSpecialistReadDTO
    created_at: datetime
    amount: Decimal("0.00")
    updated_at: datetime
    id: int


@dataclass(frozen=True)
class EnterprisePayrollRequestCreateDTO:
    passport_numbers: list[str]
    amount: Decimal("0.00")
    enterprise_id: int
    specialist: int


@dataclass(frozen=True)
class EnterprisePayrollTransactionCreateDTO:
    payroll_request_id: int


@dataclass(frozen=True)
class EnterprisePayrollTransactionReadDTO:
    payroll_request_id: int
    created_at: datetime
