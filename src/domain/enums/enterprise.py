from enum import Enum


class EnterpriseType(Enum):
    LLC = "LLC"
    SP = "SP"
    LLP = "LLP"


class EnterprisePayrollRequestStatus(Enum):
    APPROVED = 'APPROVED'
    ON_CONSIDERATION = 'ON_CONSIDERATION'
    CANCELLED = 'CANCELLED'
