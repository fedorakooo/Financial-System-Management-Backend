from src.application.dtos.account import AccountReadDTO
from src.domain.entities.enterprise import (
    Enterprise, EnterpriseSpecialist, EnterprisePayrollRequest, EnterprisePayrollTransaction
)
from src.application.dtos.enterprise import (
    EnterpriseCreateDTO, EnterpriseReadDTO,
    EnterpriseSpecialistCreateDTO, EnterpriseSpecialistReadDTO,
    EnterprisePayrollRequestCreateDTO, EnterprisePayrollRequestReadDTO,
    EnterprisePayrollTransactionCreateDTO, EnterprisePayrollTransactionReadDTO
)

class EnterpriseMapper:
    """Utility class for mapping between Enterprise-related DTOs and domain entities."""

    @staticmethod
    def map_enterprise_create_dto_to_enterprise(dto: EnterpriseCreateDTO, account_id: int) -> Enterprise:
        return Enterprise(
            name=dto.name,
            type=dto.type,
            unp=dto.unp,
            bank_id=dto.bank_id,
            address=dto.address,
            account_id=account_id
        )

    @staticmethod
    def map_enterprise_to_enterprise_read_dto(
            enterprise: Enterprise,
            account_read_dto: AccountReadDTO
    ) -> EnterpriseReadDTO:
        return EnterpriseReadDTO(
            name=enterprise.name,
            type=enterprise.type,
            unp=enterprise.unp,
            bank_id=enterprise.bank_id,
            address=enterprise.address,
            account=account_read_dto,
            id=enterprise.id,
            created_at=enterprise.created_at,
            updated_at=enterprise.updated_at
        )

    @staticmethod
    def map_enterprise_specialist_create_dto_to_enterprise_specialist(
            dto: EnterpriseSpecialistCreateDTO
    ) -> EnterpriseSpecialist:
        return EnterpriseSpecialist(
            user_id=dto.user_id,
            enterprise_id=dto.enterprise_id
        )

    @staticmethod
    def map_enterprise_specialist_to_enterprise_specialist_read_dto(
            specialist: EnterpriseSpecialist,
            user_read_dto,
            enterprise_read_dto: EnterpriseReadDTO
    ) -> EnterpriseSpecialistReadDTO:
        return EnterpriseSpecialistReadDTO(
            user=user_read_dto,
            enterprise=enterprise_read_dto,
            id=specialist.id
        )

    @staticmethod
    def map_enterprise_payroll_request_create_dto_to_enterprise_payroll_request(
            dto: EnterprisePayrollRequestCreateDTO
    ) -> EnterprisePayrollRequest:
        return EnterprisePayrollRequest(
            status=EnterprisePayrollRequestStatus.ON_CONSIDERATION,
            passport_numbers=dto.passport_numbers,
            enterprise_id=dto.enterprise_id,
            specialist_id=dto.specialist
        )

    @staticmethod
    def map_enterprise_payroll_request_to_enterprise_payroll_request_read_dto(
            request: EnterprisePayrollRequest,
            enterprise_read_dto: EnterpriseReadDTO,
            specialist_read_dto: EnterpriseSpecialistReadDTO
    ) -> EnterprisePayrollRequestReadDTO:
        return EnterprisePayrollRequestReadDTO(
            status=request.status,
            passport_numbers=request.passport_numbers,
            enterprise=enterprise_read_dto,
            specialist=specialist_read_dto,
            created_at=request.created_at,
            updated_at=request.updated_at,
            id=request.id
        )

    @staticmethod
    def map_enterprise_payroll_transaction_create_dto_to_enterprise_payroll_transaction(
            dto: EnterprisePayrollTransactionCreateDTO
    ) -> EnterprisePayrollTransaction:
        return EnterprisePayrollTransaction(
            payroll_request_id=dto.payroll_request_id
        )

    @staticmethod
    def map_enterprise_payroll_transaction_to_enterprise_payroll_transaction_read_dto(
            transaction: EnterprisePayrollTransaction
    ) -> EnterprisePayrollTransactionReadDTO:
        return EnterprisePayrollTransactionReadDTO(
            payroll_request_id=transaction.payroll_request_id,
            created_at=transaction.created_at
        )
