from src.application.dtos.profile import ProfileReadDTO, ProfileUpdateDTO
from src.infrastructure.schemas.profile import ProfileResponse, ProfileUpdateRequest


class ProfileSchemaMapper:
    """Utility class for mapping between Data Transfer Objects (DTOs) and Pydantic models for the Profile entity."""

    @staticmethod
    def to_response(dto: ProfileReadDTO) -> ProfileResponse:
        return ProfileResponse(
            id=dto.id,
            name=dto.name,
            passport_number=dto.passport_number,
            phone_number=dto.phone_number,
            email=dto.email,
            role=dto.role,
            is_active=dto.is_active,
            is_foreign=dto.is_foreign,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @staticmethod
    def from_update_request(request: ProfileUpdateRequest) -> ProfileUpdateDTO:
        return ProfileUpdateDTO(
            name=request.name if hasattr(request, 'name') else None,
            passport_number=request.passport_number if hasattr(request, 'passport_number') else None,
            email=request.email if hasattr(request, 'email') else None
        )
