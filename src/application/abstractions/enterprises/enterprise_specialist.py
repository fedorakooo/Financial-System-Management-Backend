from abc import ABC, abstractmethod

from src.application.dtos.user import UserAccessDTO
from src.application.dtos.enterprise import (
    EnterprisePayrollRequestReadDTO, EnterprisePayrollTransactionReadDTO,
    EnterpriseSpecialistReadDTO, EnterprisePayrollRequestCreateDTO
)


class AbstractEnterpriseSpecialistService(ABC):
    """Abstract service for managing user deposits."""

    @abstractmethod
    async def get_enterprise_payroll_request_by_id(
            self,
            enterprise_payroll_request_id: int,
            requesting_user: UserAccessDTO
    ) -> EnterprisePayrollRequestReadDTO:
        pass

    @abstractmethod
    async def get_payroll_transactions_by_enterprise_payroll_request_id(
            self,
            enterprise_payroll_request_id: int,
            requesting_user: UserAccessDTO
    ) -> list[EnterprisePayrollTransactionReadDTO]:
        pass

    @abstractmethod
    async def get_enterprise_specialist_profile(self, requesting_user: UserAccessDTO) -> EnterpriseSpecialistReadDTO:
        pass

    @abstractmethod
    async def create_enterprise_payroll_request(
            self,
            enterprise_payroll_request: EnterprisePayrollRequestCreateDTO,
            requesting_user: UserAccessDTO
    ) -> EnterprisePayrollRequestReadDTO:
        pass

    @abstractmethod
    async def make_enterprise_payroll_request(
            self,
            enterprise_payroll_request_id: int,
            requesting_user: UserAccessDTO
    ) -> None:
        pass
