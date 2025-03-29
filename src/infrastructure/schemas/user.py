from datetime import datetime
from pydantic import BaseModel, EmailStr

from src.domain.enums.user import UserRole


class UserResponse(BaseModel):
    id: int
    name: str
    passport_number: str
    phone_number: str
    email: EmailStr
    role: UserRole
    is_active: bool
    is_foreign: bool
    created_at: datetime
    updated_at: datetime


class UserCreateRequest(BaseModel):
    name: str
    passport_number: str
    phone_number: str
    email: EmailStr
    password: str
    is_foreign: bool = False


class UserUpdateRequest(BaseModel):
    name: str
    passport_number: str
    phone_number: str
    email: EmailStr
