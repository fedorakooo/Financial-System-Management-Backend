from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.domain.enums.user import UserRole


@dataclass(frozen=True)
class ProfileReadDTO:
    id: int
    name: str
    passport_number: str
    email: str
    role: UserRole
    phone_number: str
    is_active: bool
    is_foreign: bool
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class ProfileUpdateDTO:
    name: Optional[str]
    passport_number: Optional[str]
    email: Optional[str]
