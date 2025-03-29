from abc import ABC, abstractmethod

from src.application.dtos.enterprise import EnterpriseReadDTO, EnterprisePayrollRequestReadDTO, EnterpriseCreateDTO, \
    EnterpriseSpecialistReadDTO, EnterpriseSpecialistCreateDTO
from src.application.dtos.user import UserAccessDTO


class AbstractEnterpriseManagementService(ABC):
    """Abstract service for staff-level users to manage enterprises."""

    @abstractmethod
    async def get_enterprise_by_id(self, enterprise_id: int, requesting_user: UserAccessDTO) -> EnterpriseReadDTO:
        pass

    @abstractmethod
    async def get_enterprise_payroll_request_by_id(
            self,
            enterprise_payroll_request: int,
            requesting_user: UserAccessDTO
    ) -> EnterprisePayrollRequestReadDTO:
        pass

    @abstractmethod
    async def approve_enterprise_payroll_request(
            self,
            enterprise_payroll_request: int,
            requesting_user: UserAccessDTO
    ) -> EnterprisePayrollRequestReadDTO:
        pass

    async def create_enterprise(
            self,
            enterprise_create_dto: EnterpriseCreateDTO,
            requesting_user: UserAccessDTO
    ) -> EnterpriseReadDTO:
        pass

    async def create_enterprise_specialist(
            self,
            enterprise_specialist_create_dto: EnterpriseSpecialistCreateDTO,
            requesting_user: UserAccessDTO
    ) -> EnterpriseSpecialistReadDTO:
        pass