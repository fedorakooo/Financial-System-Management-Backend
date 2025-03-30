from abc import ABC, abstractmethod

from src.application.dtos.enterprise import (
    EnterpriseReadDTO,
    EnterprisePayrollRequestReadDTO,
    EnterpriseCreateDTO,
    EnterpriseSpecialistReadDTO,
    EnterpriseSpecialistCreateDTO
)
from src.application.dtos.user import UserAccessDTO, UserCreateDTO


class AbstractEnterpriseManagementService(ABC):
    """Abstract service for staff-level users to manage enterprises."""

    @abstractmethod
    async def get_enterprise_by_id(self, enterprise_id: int, requesting_user: UserAccessDTO) -> EnterpriseReadDTO:
        """Fetches an enterprise and its account for an authorized staff member.

        Raises:
            ForbiddenError: If the requesting user cannot access this resource.
            NotFoundError: If the requested resource does not exist.
        """
        pass

    @abstractmethod
    async def get_enterprise_payroll_request_by_id(
            self,
            enterprise_payroll_request: int,
            requesting_user: UserAccessDTO
    ) -> EnterprisePayrollRequestReadDTO:
        """Fetches a payroll request with its enterprise and specialist details for staff.

        Raises:
            ForbiddenError: If the requesting user cannot access this resource.
            NotFoundError: If the requested resource does not exist.
        """
        pass

    @abstractmethod
    async def approve_enterprise_payroll_request(
            self,
            enterprise_payroll_request: int,
            requesting_user: UserAccessDTO
    ) -> EnterprisePayrollRequestReadDTO:
        """Approves a pending payroll request and creates its salary accounts atomically.

        Raises:
            ForbiddenError: If the staff member cannot approve payroll requests.
            NotFoundError: If the request, enterprise, specialist, or a recipient is missing.
            InvalidOperationError: If the request is no longer awaiting approval.
        """
        pass

    async def create_enterprise(
            self,
            enterprise_create_dto: EnterpriseCreateDTO,
            requesting_user: UserAccessDTO
    ) -> EnterpriseReadDTO:
        """Creates an enterprise and its active enterprise account in one transaction.

        Raises:
            ForbiddenError: If the staff member cannot create enterprises.
        """
        pass

    async def create_enterprise_specialist(
            self,
            enterprise_specialist_create_dto: EnterpriseSpecialistCreateDTO,
            requesting_user: UserAccessDTO,
            user_create_dto: UserCreateDTO = None
    ) -> EnterpriseSpecialistReadDTO:
        """Creates a specialist association for an authorized staff member.

        When user_create_dto is provided, creates the user and association atomically;
        otherwise links an existing user with the SPECIALIST role.

        Raises:
            ForbiddenError: If the staff member cannot create specialists.
            NotFoundError: If the enterprise or existing user does not exist.
            InvalidOperationError: If the existing user is not a specialist.
        """
        pass