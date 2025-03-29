from src.application.dtos.user import UserAccessDTO
from src.domain.enums.user import UserRole
from src.domain.exceptions.forbidden import ForbiddenError


class UserManagementAccessControlService:
    """Service for controlling access to user management operations."""

    @staticmethod
    def can_get_users(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [UserRole.OPERATOR, UserRole.MANAGER, UserRole.ADMINISTRATOR]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_update_user(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [UserRole.MANAGER, UserRole.ADMINISTRATOR]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_delete_user(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [UserRole.MANAGER, UserRole.ADMINISTRATOR]:
            return True
        raise ForbiddenError()