from pydantic import BaseModel, EmailStr
from datetime import datetime

from src.domain.enums.user import UserRole


class ProfileResponse(BaseModel):
    id: int
    name: str
    passport_number: str
    email: EmailStr
    role: UserRole
    phone_number: str
    is_active: bool
    is_foreign: bool
    created_at: datetime
    updated_at: datetime


class ProfileUpdateRequest(BaseModel):
    name: str
    passport_number: str
    email: EmailStr
