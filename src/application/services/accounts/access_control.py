from src.application.dtos.user import UserAccessDTO
from src.domain.enums.user import UserRole
from src.domain.exceptions.forbidden import ForbiddenError


class AccountProfileAccessControlService:
    """Service for controlling access to account profile operations."""

    @staticmethod
    def can_get_account(owner_id: int, requesting_user: UserAccessDTO) -> bool:
        if owner_id == requesting_user.id and UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_get_accounts(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_create_account(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_update_account(owner_id: int, requesting_user: UserAccessDTO) -> bool:
        if owner_id == requesting_user.id and UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()


class AccountManagementAccessControlService:
    """Service for controlling access to account management operations."""

    @staticmethod
    def can_get_accounts(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [
            UserRole.ADMINISTRATOR,
            UserRole.MANAGER,
            UserRole.OPERATOR
        ]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_update_account(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [
            UserRole.ADMINISTRATOR,
            UserRole.MANAGER
        ]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_delete_account(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [
            UserRole.ADMINISTRATOR,
            UserRole.MANAGER
        ]:
            return True
        raise ForbiddenError()
