from typing import Optional

from src.application.dtos.user import UserAccessDTO
from src.domain.enums.user import UserRole
from src.domain.exceptions.forbidden import ForbiddenError


class WithdrawalProfileAccessControlService:
    """Service for controlling access to withdrawal profile operations."""

    @staticmethod
    def can_get_withdrawals(account_owner_id: int, requesting_user: UserAccessDTO) -> Optional[bool]:
        if account_owner_id == requesting_user.id and UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_create_withdrawal(account_owner_id: int, requesting_user: UserAccessDTO) -> Optional[bool]:
        if account_owner_id == requesting_user.id and UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()
