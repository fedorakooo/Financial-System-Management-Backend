from datetime import datetime

from src.domain.entities.user import User
from src.application.dtos.profile import ProfileReadDTO, ProfileUpdateDTO


class ProfileMapper:
    """Utility class for mapping between Profile-related DTOs and domain entities."""

    @staticmethod
    def map_profile_update_dto_to_user(dto: ProfileUpdateDTO, current_user: User) -> User:
        return User(
            name=dto.name if dto.name else current_user.name,
            passport_number=dto.passport_number if dto.passport_number else current_user.passport_number,
            email=dto.email if dto.email else current_user.email,
            phone_number=current_user.phone_number,
            hashed_password=current_user.hashed_password,
            role=current_user.role,
            is_active=current_user.is_active,
            is_foreign=current_user.is_foreign,
            created_at=current_user.created_at,
            updated_at=datetime.now()
        )

    @staticmethod
    def map_user_to_profile_read_dto(user: User) -> ProfileReadDTO:
        return ProfileReadDTO(
            id=user.id,
            name=user.name,
            passport_number=user.passport_number,
            email=user.email,
            phone_number=user.phone_number,
            role=user.role,
            is_active=user.is_active,
            is_foreign=user.is_foreign,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
