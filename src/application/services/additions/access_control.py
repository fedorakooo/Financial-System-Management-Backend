from typing import Optional

from src.application.dtos.user import UserAccessDTO
from src.domain.enums.user import UserRole
from src.domain.exceptions.forbidden import ForbiddenError


class AdditionProfileAccessControlService:
    """Service for controlling access to addition profile operations."""

    @staticmethod
    def can_get_additions(account_owner_id: int, requesting_user: UserAccessDTO) -> bool:
        if account_owner_id == requesting_user.id and UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_create_addition(account_owner_id: int, requesting_user: UserAccessDTO) -> bool:
        if account_owner_id == requesting_user.id and UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()
