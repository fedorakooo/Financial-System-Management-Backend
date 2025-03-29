from src.application.dtos.account import AccountReadDTO, AccountUpdateClientDTO, AccountUpdateStaffDTO, AccountCreateDTO
from src.infrastructure.schemas.account import AccountResponse, AccountUpdateRequest, AccountCreateRequest


class AccountSchemaMapper:
    """Utility class for mapping between Data Transfer Objects (DTOs) and Pydantic models for the Account entity."""

    @staticmethod
    def to_response(dto: AccountReadDTO) -> AccountResponse:
        return AccountResponse(
            id=dto.id,
            user_id=dto.user_id,
            bank_id=dto.bank_id,
            balance=dto.balance,
            status=dto.status,
            type=dto.type,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @staticmethod
    def from_create_request(request: AccountCreateRequest, user_id: int) -> AccountCreateDTO:
        return AccountCreateDTO(
            user_id=user_id,
            bank_id=request.bank_id,
        )

    @staticmethod
    def from_update_request_to_client(request: AccountUpdateRequest) -> AccountUpdateClientDTO:
        return AccountUpdateClientDTO(
            status=request.status if hasattr(request, 'status') else None
        )

    @staticmethod
    def from_update_request_to_staff(request: AccountUpdateRequest) -> AccountUpdateStaffDTO:
        return AccountUpdateClientDTO(
            status=request.status if hasattr(request, 'status') else None
        )
