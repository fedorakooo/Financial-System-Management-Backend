from src.application.dtos.bank import BankReadDTO, BankCreateDTO, BankUpdateDTO
from src.infrastructure.schemas.bank import BankResponse, BankCreateRequest, BankUpdateRequest


class BankSchemaMapper:
    """Utility class for mapping between Data Transfer Objects (DTOs) and Pydantic models for the Bank entity."""

    @staticmethod
    def to_response(dto: BankReadDTO) -> BankResponse:
        return BankResponse(
            id=dto.id,
            name=dto.name,
            bic=dto.bic,
            address=dto.address,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @staticmethod
    def from_create_request(request: BankCreateRequest) -> BankCreateDTO:
        return BankCreateDTO(
            name=request.name,
            bic=request.bic,
            address=request.address
        )

    @staticmethod
    def from_update_request(request: BankUpdateRequest) -> BankUpdateDTO:
        return BankUpdateDTO(
            name=request.name if hasattr(request, 'name') else None,
            address=request.address if hasattr(request, 'address') else None,
        )
