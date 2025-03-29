from typing import Optional

from src.application.dtos.user import UserAccessDTO
from src.domain.enums.user import UserRole
from src.domain.exceptions.forbidden import ForbiddenError


class TransferProfileAccessControlService:
    """Service for controlling access to transfer profile operations."""

    @staticmethod
    def can_get_transfers(account_owner_id: int, requesting_user: UserAccessDTO) -> bool:
        if account_owner_id == requesting_user.id and UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_create_transfer(account_owner_id: int, requesting_user: UserAccessDTO) -> bool:
        if account_owner_id == requesting_user.id and UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()

class TransferManagementAccessControlService:
    """Service for controlling access to transfer management operations."""

    @staticmethod
    def can_get_transaction(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [
            UserRole.ADMINISTRATOR,
            UserRole.MANAGER,
            UserRole.OPERATOR
        ]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_reverse_transaction(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [
            UserRole.ADMINISTRATOR,
            UserRole.MANAGER,
        ]:
            return True
        raise ForbiddenError()
