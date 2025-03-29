from src.application.dtos.enterprise import EnterpriseReadDTO, EnterpriseCreateDTO, EnterpriseSpecialistReadDTO, \
    EnterpriseSpecialistCreateDTO, EnterprisePayrollRequestReadDTO, EnterprisePayrollRequestCreateDTO, \
    EnterprisePayrollTransactionCreateDTO, EnterprisePayrollTransactionReadDTO
from src.infrastructure.schemas.enterprise import EnterpriseResponse, EnterpriseCreateRequest, \
    EnterpriseSpecialistResponse, EnterpriseSpecialistCreateRequest, EnterprisePayrollRequestResponse, \
    EnterprisePayrollRequestCreateRequest, EnterprisePayrollTransactionCreateRequest, \
    EnterprisePayrollTransactionResponse
from src.infrastructure.mappers.account import AccountSchemaMapper
from src.infrastructure.mappers.user import UserSchemaMapper


class EnterpriseSchemaMapper:
    """Utility class for mapping between Data Transfer Objects (DTOs) and Pydantic models for the Enterprise entities."""

    @staticmethod
    def map_enterprise_to_response(dto: EnterpriseReadDTO) -> EnterpriseResponse:
        account_response = AccountSchemaMapper.to_response(dto.account)
        return EnterpriseResponse(
            id=dto.id,
            name=dto.name,
            type=dto.type,
            unp=dto.unp,
            bank_id=dto.bank_id,
            address=dto.address,
            account=account_response,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @staticmethod
    def map_enterprise_from_create_request(request: EnterpriseCreateRequest) -> EnterpriseCreateDTO:
        return EnterpriseCreateDTO(
            name=request.name,
            type=request.type,
            unp=request.unp,
            bank_id=request.bank_id,
            address=request.address,
        )

    @staticmethod
    def map_enterprise_specialist_to_response(dto: EnterpriseSpecialistReadDTO) -> EnterpriseSpecialistResponse:
        user_response = UserSchemaMapper.to_response(dto.user)
        enterprise_response = EnterpriseSchemaMapper.map_enterprise_to_response(dto.enterprise)
        return EnterpriseSpecialistResponse(
            user=user_response,
            enterprise=enterprise_response,
            id=dto.id
        )

    @staticmethod
    def map_enterprise_specialist_from_create_request(
            request: EnterpriseSpecialistCreateRequest,
            created_user_id: int
    ) -> EnterpriseSpecialistCreateDTO:
        return EnterpriseSpecialistCreateDTO(
            enterprise_id=request.enterprise_id,
            user_id=created_user_id
        )

    @staticmethod
    def map_enterprise_payroll_request_to_response(dto: EnterprisePayrollRequestReadDTO) -> EnterprisePayrollRequestResponse:
        enterprise_response = EnterpriseSchemaMapper.map_enterprise_to_response(dto.enterprise)
        specialist_response = EnterpriseSchemaMapper.map_enterprise_specialist_to_response(dto.specialist)
        return EnterprisePayrollRequestResponse(
            id=dto.id,
            status=dto.status,
            passport_numbers=dto.passport_numbers,
            accounts_id=dto.accounts_id,
            enterprise=enterprise_response,
            specialist=specialist_response,
            created_at=dto.created_at,
            amount=dto.amount,
            updated_at=dto.updated_at
        )

    @staticmethod
    def map_enterprise_payroll_request_from_create_request(request: EnterprisePayrollRequestCreateRequest) -> EnterprisePayrollRequestCreateDTO:
        return EnterprisePayrollRequestCreateDTO(
            passport_numbers=request.passport_numbers,
            amount=request.amount,
            enterprise_id=request.enterprise_id,
            specialist=request.specialist
        )

    @staticmethod
    def map_enterprise_payroll_transaction_to_response(dto: EnterprisePayrollTransactionReadDTO) -> EnterprisePayrollTransactionResponse:
        return EnterprisePayrollTransactionResponse(
            payroll_request_id=dto.payroll_request_id,
            created_at=dto.created_at
        )

    @staticmethod
    def map_enterprise_payroll_transaction_from_create_request(request: EnterprisePayrollTransactionCreateRequest) -> EnterprisePayrollTransactionCreateDTO:
        return EnterprisePayrollTransactionCreateDTO(
            payroll_request_id=request.payroll_request_id
        )
