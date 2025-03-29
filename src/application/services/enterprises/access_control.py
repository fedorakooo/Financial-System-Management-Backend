from src.application.dtos.user import UserAccessDTO
from src.domain.enums.user import UserRole
from src.domain.exceptions.forbidden import ForbiddenError


class EnterpriseSpecialistAccessControlService:
    """Service for controlling access to loan profile operations."""

    @staticmethod
    def can_get_enterprise_specialist_profile(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [UserRole.SPECIALIST]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_get_enterprise_payroll_requests(
            enterprise_payroll_request_owner: int,
            requesting_user: UserAccessDTO
    ) -> bool:
        if enterprise_payroll_request_owner == requesting_user.id and UserRole(requesting_user.role) in [
            UserRole.SPECIALIST
        ]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_create_enterprise_payroll_request(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [UserRole.SPECIALIST]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_make_enterprise_payroll_request(
            enterprise_payroll_request_owner: int,
            requesting_user: UserAccessDTO
    ) -> bool:
        if enterprise_payroll_request_owner == requesting_user.id and UserRole(requesting_user.role) in [
            UserRole.SPECIALIST
        ]:
            return True
        raise ForbiddenError()


class EnterpriseManagementAccessControlService:
    """Service for controlling access to enterprise management operations."""

    @staticmethod
    def can_get_enterprises(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [
            UserRole.ADMINISTRATOR,
            UserRole.MANAGER,
            UserRole.OPERATOR
        ]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_get_enterprise_payroll_requests(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [
            UserRole.ADMINISTRATOR,
            UserRole.MANAGER,
            UserRole.OPERATOR
        ]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_approve_enterprise_payroll_request(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [
            UserRole.ADMINISTRATOR,
            UserRole.MANAGER
        ]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_create_enterprise(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [
            UserRole.ADMINISTRATOR,
            UserRole.MANAGER
        ]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_create_enterprise_specialist(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [
            UserRole.ADMINISTRATOR,
            UserRole.MANAGER
        ]:
            return True
        raise ForbiddenError()

