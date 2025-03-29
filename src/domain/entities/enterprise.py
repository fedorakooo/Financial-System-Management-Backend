from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from src.domain.enums.enterprise import EnterpriseType, EnterprisePayrollRequestStatus


@dataclass(frozen=True)
class Enterprise:
    name: str
    type: EnterpriseType
    unp: str
    bank_id: int
    address: str
    account_id: int
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass(frozen=True)
class EnterpriseSpecialist:
    user_id: int
    enterprise_id: int
    id: Optional[int] = None


@dataclass(frozen=True)
class EnterprisePayrollRequest:
    status: EnterprisePayrollRequestStatus
    passport_numbers: list[str]
    enterprise_id: int
    specialist_id: int
    amount: Decimal("0.00")
    accounts_id: Optional[list[int]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    id: Optional[int] = None

@dataclass(frozen=True)
class EnterprisePayrollTransaction:
    payroll_request_id: int
    created_at: Optional[datetime] = None
