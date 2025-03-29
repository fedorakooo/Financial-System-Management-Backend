from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

from src.domain.enums.user import UserRole


@dataclass(frozen=True)
class User:
    name: str
    passport_number: str
    phone_number: str
    email: str
    role: UserRole
    hashed_password: str
    is_active: bool
    is_foreign: bool
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = datetime.now()
