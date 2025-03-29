from src.application.dtos.withdrawal import WithdrawalReadDTO, WithdrawalCreateDTO
from src.infrastructure.schemas.withdrawal import WithdrawalResponse, WithdrawalCreateRequest


class WithdrawalSchemaMapper:
    """Utility class for mapping between Data Transfer Objects (DTOs) and Pydantic models for the Withdrawal entity."""

    @staticmethod
    def to_response(dto: WithdrawalReadDTO) -> WithdrawalResponse:
        return WithdrawalResponse(
            id=dto.id,
            account_id=dto.account_id,
            amount=dto.amount,
            source=dto.source,
            created_at=dto.created_at
        )

    @staticmethod
    def from_create_request(request: WithdrawalCreateRequest, account_id: int) -> WithdrawalCreateDTO:
        return WithdrawalCreateDTO(
            account_id=account_id,
            amount=request.amount,
            source=request.source
        )
