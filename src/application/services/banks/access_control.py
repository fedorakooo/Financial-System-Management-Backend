from src.application.dtos.user import UserAccessDTO
from src.domain.enums.user import UserRole
from src.domain.exceptions.forbidden import ForbiddenError


class BankManagementAccessControlService:
    """Service for controlling access to bank management operations."""

    @staticmethod
    def can_get_banks(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [
            UserRole.ADMINISTRATOR,
            UserRole.MANAGER,
            UserRole.OPERATOR
        ]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_create_bank(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [
            UserRole.ADMINISTRATOR,
            UserRole.MANAGER
        ]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_update_bank(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [
            UserRole.ADMINISTRATOR,
            UserRole.MANAGER
        ]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_delete_bank(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [
            UserRole.ADMINISTRATOR,
            UserRole.MANAGER
        ]:
            return True
        raise ForbiddenError()
