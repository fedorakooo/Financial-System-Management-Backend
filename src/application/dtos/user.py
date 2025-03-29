from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.domain.enums.user import UserRole


@dataclass(frozen=True)
class UserReadDTO:
    id: int
    name: str
    passport_number: str
    email: str
    phone_number: str
    is_active: bool
    is_foreign: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class UserCreateDTO:
    name: str
    passport_number: str
    email: str
    phone_number: str
    password: str
    is_foreign: bool


@dataclass(frozen=True)
class UserUpdateDTO:
    is_active: Optional[bool]


@dataclass(frozen=True)
class UserAuthDTO:
    id: int
    role: UserRole
    is_active: bool


@dataclass(frozen=True)
class UserAccessDTO:
    id: int
    role: UserRole
