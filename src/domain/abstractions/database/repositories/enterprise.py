from abc import ABC, abstractmethod

from src.domain.enums.enterprise import EnterprisePayrollRequestStatus
from src.domain.entities.enterprise import (
    Enterprise,
    EnterpriseSpecialist,
    EnterprisePayrollRequest,
    EnterprisePayrollTransaction
)

class AbstractEnterpriseRepository(ABC):
    """Abstract class for an enterprise repository."""

    @abstractmethod
    async def get_enterprise_by_id(self, enterprise_id: int) -> Enterprise:
        """Fetches an enterprise by its unique identifier.

        Raises:
            NotFoundError: If the enterprise with the specified id is not found.
        """

    @abstractmethod
    async def get_enterprise_specialist_by_user_id(self, user_id: int) -> EnterpriseSpecialist:
        """Fetches the enterprise specialist associated with a user.

        Raises:
            NotFoundError: If the specialist profile does not exist.
        """
        pass

    @abstractmethod
    async def get_enterprise_specialist_by_id(self, specialist_id: int) -> EnterpriseSpecialist:
        """Fetches an enterprise specialist by its unique identifier.

        Raises:
            NotFoundError: If the specialist does not exist.
        """
        pass

    @abstractmethod
    async def get_enterprise_payroll_request_by_id(self, enterprise_payroll_request_id: int) -> EnterprisePayrollRequest:
        """Fetches and locks a payroll request until the transaction ends.

        Raises:
            NotFoundError: If the payroll request does not exist.
            InvalidOperationError: If a legacy request has no reconciled payment amount.
        """
        pass

    @abstractmethod
    async def create_enterprise_specialist(self, enterprise_specialist: EnterpriseSpecialist) -> EnterpriseSpecialist:
        """Creates the association between a specialist user and an enterprise."""
        pass

    @abstractmethod
    async def get_enterprise_payroll_transactions_by_payroll_request_id(
            self,
            enterprise_payroll_request_id: int
    ) -> list[EnterprisePayrollRequest]:
        """Fetches the payment history of a payroll request, or an empty list if unpaid."""
        pass


    @abstractmethod
    async def create_payroll_request(self, payroll_request: EnterprisePayrollRequest) -> EnterprisePayrollRequest:
        """Creates a payroll request with its recipients, amount, status, and selected accounts."""
        pass

    @abstractmethod
    async def create_enterprise_payroll_transaction(
            self,
            enterprise_payroll_transaction: EnterprisePayrollTransaction
    ) -> EnterprisePayrollTransaction:
        """Records a completed payroll payment within the same transaction as the balance changes."""
        pass

    @abstractmethod
    async def create_enterprise(self, enterprise: Enterprise) -> Enterprise:
        """Creates an enterprise linked to its bank and enterprise account."""
        pass

    @abstractmethod
    async def update_payroll_request_status_by_id(
            self,
            payroll_request_id: int,
            payroll_request_status: EnterprisePayrollRequestStatus
    ) -> EnterprisePayrollRequest:
        """Updates a payroll request status and returns the updated request.

        Raises:
            NotFoundError: If the payroll request does not exist.
        """
        pass

    @abstractmethod
    async def update_payroll_request_accounts(self, payroll_request_id: int, accounts_id: list[int]) -> None:
        """Persist the salary accounts selected during approval."""
