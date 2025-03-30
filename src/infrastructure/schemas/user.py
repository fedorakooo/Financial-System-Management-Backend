from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator

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
    name: str = Field(min_length=1, max_length=150)
    passport_number: str = Field(min_length=1, max_length=20)
    phone_number: str = Field(min_length=1, max_length=20)
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=1)
    is_foreign: bool = False

    @field_validator("password")
    @classmethod
    def password_bytes(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 UTF-8 bytes")
        return value


class UserUpdateRequest(BaseModel):
    is_active: bool
