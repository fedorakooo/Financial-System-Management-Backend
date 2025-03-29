from src.application.dtos.addition import AdditionReadDTO, AdditionCreateDTO
from src.infrastructure.schemas.addition import AdditionResponse, AdditionCreateRequest


class AdditionSchemaMapper:
    """Utility class for mapping between Data Transfer Objects (DTOs) and Pydantic models for the Addition entity."""

    @staticmethod
    def to_response(dto: AdditionReadDTO) -> AdditionResponse:
        return AdditionResponse(
            id=dto.id,
            account_id=dto.account_id,
            amount=dto.amount,
            source=dto.source,
            created_at=dto.created_at
        )

    @staticmethod
    def from_create_request(request: AdditionCreateRequest) -> AdditionCreateDTO:
        return AdditionCreateDTO(
            account_id=request.account_id,
            amount=request.amount,
            source=request.source
        )
