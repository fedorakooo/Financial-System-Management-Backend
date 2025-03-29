from src.application.dtos.user import UserReadDTO, UserCreateDTO, UserUpdateDTO
from src.infrastructure.schemas.user import UserResponse, UserCreateRequest, UserUpdateRequest


class UserSchemaMapper:
    """Utility class for mapping between Data Transfer Objects (DTOs) and Pydantic models for the User entity."""

    @staticmethod
    def to_response(dto: UserReadDTO) -> UserResponse:
        return UserResponse(
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

    # Pydantic -> DTO
    @staticmethod
    def from_create_request(request: UserCreateRequest) -> UserCreateDTO:
        return UserCreateDTO(
            name=request.name,
            passport_number=request.passport_number,
            email=request.email,
            phone_number=request.phone_number,
            password=request.password,
            is_foreign=request.is_foreign,
        )

    @staticmethod
    def from_update_request(request: UserUpdateRequest) -> UserUpdateDTO:
        return UserUpdateDTO(
            is_active=request.is_active if hasattr(request, 'is_active') else None,
        )