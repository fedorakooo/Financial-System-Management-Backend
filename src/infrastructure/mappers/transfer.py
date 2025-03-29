from src.application.dtos.transfer import TransferReadDTO, TransferCreateDTO
from src.infrastructure.schemas.transfer import TransferResponse, TransferCreateRequest


class TransferSchemaMapper:
    """Utility class for mapping between Data Transfer Objects (DTOs) and Pydantic models for the Transfer entity."""

    @staticmethod
    def to_response(dto: TransferReadDTO) -> TransferResponse:
        return TransferResponse(
            id=dto.id,
            from_account_id=dto.from_account_id,
            to_account_id=dto.to_account_id,
            amount=dto.amount,
            status=dto.status,
            updated_at=dto.updated_at,
            created_at=dto.created_at
        )

    @staticmethod
    def from_create_request(request: TransferCreateRequest, account_id: int) -> TransferCreateDTO:
        return TransferCreateDTO(
            from_account_id=account_id,
            to_account_id=request.to_account_id,
            amount=request.amount
        )
