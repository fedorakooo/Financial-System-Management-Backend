from abc import ABC, abstractmethod

from src.application.dtos.user import UserAccessDTO
from src.application.dtos.enterprise import (
    EnterprisePayrollRequestReadDTO, EnterprisePayrollTransactionReadDTO,
    EnterpriseSpecialistReadDTO, EnterprisePayrollRequestCreateDTO
)


class AbstractEnterpriseSpecialistService(ABC):
    """Abstract service for enterprise specialists to manage their payroll requests."""

    @abstractmethod
    async def get_enterprise_payroll_request_by_id(
            self,
            enterprise_payroll_request_id: int,
            requesting_user: UserAccessDTO
    ) -> EnterprisePayrollRequestReadDTO:
        """Fetches a payroll request owned by the requesting specialist.

        Raises:
            ForbiddenError: If the requesting user cannot access this resource.
            NotFoundError: If the requested resource does not exist.
        """
        pass

    @abstractmethod
    async def get_payroll_transactions_by_enterprise_payroll_request_id(
            self,
            enterprise_payroll_request_id: int,
            requesting_user: UserAccessDTO
    ) -> list[EnterprisePayrollTransactionReadDTO]:
        """Fetches payment history for a payroll request owned by the requesting specialist.

        Raises:
            ForbiddenError: If the requesting user cannot access this resource.
            NotFoundError: If the requested resource does not exist.
        """
        pass

    @abstractmethod
    async def get_enterprise_specialist_profile(self, requesting_user: UserAccessDTO) -> EnterpriseSpecialistReadDTO:
        """Fetches the requesting specialist's profile, enterprise, and enterprise account.

        Raises:
            ForbiddenError: If the requesting user cannot access this resource.
            NotFoundError: If the requested resource does not exist.
        """
        pass

    @abstractmethod
    async def create_enterprise_payroll_request(
            self,
            enterprise_payroll_request: EnterprisePayrollRequestCreateDTO,
            requesting_user: UserAccessDTO
    ) -> EnterprisePayrollRequestReadDTO:
        """Creates a payroll request for the requesting specialist and their enterprise.

        Raises:
            ForbiddenError: If the user is not the specified specialist.
            NotFoundError: If the specialist or enterprise does not exist.
            InvalidOperationError: If the specialist belongs to another enterprise.
        """
        pass

    @abstractmethod
    async def make_enterprise_payroll_request(
            self,
            enterprise_payroll_request_id: int,
            requesting_user: UserAccessDTO
    ) -> None:
        """Pays an approved payroll request once, updating all accounts and the journal atomically.

        Raises:
            ForbiddenError: If the request belongs to another specialist.
            NotFoundError: If a required resource does not exist.
            InvalidOperationError: If the request is unapproved, already paid, or has invalid recipients.
            InactiveAccountError: If a participating account is not active.
            InsufficientFundsError: If the enterprise cannot fund the entire payroll.
        """
        pass
