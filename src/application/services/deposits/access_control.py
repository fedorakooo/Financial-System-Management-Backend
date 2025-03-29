from src.application.dtos.user import UserAccessDTO
from src.domain.enums.user import UserRole
from src.domain.exceptions.forbidden import ForbiddenError


class DepositProfileAccessControlService:
    """Service for controlling access to deposit profile operations."""

    @staticmethod
    def can_get_deposit_accounts(deposit_account_owner_id: int, requesting_user: UserAccessDTO) -> bool:
        if deposit_account_owner_id == requesting_user.id and UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_create_deposit_account(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_create_deposit_transaction(deposit_account_owner_id: int, requesting_user: UserAccessDTO) -> bool:
        if deposit_account_owner_id == requesting_user.id and UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()