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
        pass

    @abstractmethod
    async def get_enterprise_specialist_by_id(self, specialist_id: int) -> EnterpriseSpecialist:
        pass

    @abstractmethod
    async def get_enterprise_payroll_request_by_id(self, enterprise_payroll_request_id: int) -> EnterprisePayrollRequest:
        pass

    @abstractmethod
    async def create_enterprise_specialist(self, enterprise_specialist: EnterpriseSpecialist) -> EnterpriseSpecialist:
        pass

    @abstractmethod
    async def get_enterprise_payroll_transactions_by_payroll_request_id(
            self,
            enterprise_payroll_request_id: int
    ) -> list[EnterprisePayrollRequest]:
        pass


    @abstractmethod
    async def create_payroll_request(self, payroll_request: EnterprisePayrollRequest) -> EnterprisePayrollRequest:
        pass

    async def create_enterprise_payroll_transaction(
            self,
            enterprise_payroll_transaction: EnterprisePayrollTransaction
    ) -> EnterprisePayrollTransaction:
        pass

    async def create_enterprise(self, enterprise: Enterprise) -> Enterprise:
        pass

    @abstractmethod
    async def update_payroll_request_status_by_id(
            self,
            payroll_request_id: int,
            payroll_request_status: EnterprisePayrollRequestStatus
    ) -> EnterprisePayrollRequest:
        pass



