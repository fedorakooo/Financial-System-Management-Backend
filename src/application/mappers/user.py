from datetime import datetime

from src.domain.entities.user import User
from src.application.dtos.user import UserCreateDTO, UserReadDTO, UserUpdateDTO
from src.domain.enums.user import UserRole


class UserMapper:
    """Utility class for mapping between User-related DTOs and domain entities."""

    @staticmethod
    def map_user_create_dto_to_user(
            dto: UserCreateDTO,
            role: UserRole,
            hashed_password: str
    ) -> User:
        return User(
            name=dto.name,
            passport_number=dto.passport_number,
            email=dto.email,
            phone_number=dto.phone_number,
            hashed_password=hashed_password,
            role=role,
            is_active=False,
            is_foreign=dto.is_foreign,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    @staticmethod
    def map_user_update_dto_to_user(dto: UserUpdateDTO, current_user: User) -> User:
        return User(
            name=current_user.name,
            passport_number=current_user.passport_number,
            email=current_user.email,
            phone_number=current_user.phone_number,
            hashed_password=current_user.hashed_password,
            role=current_user.role,
            is_active=dto.is_active if dto.is_active else current_user.is_active,
            is_foreign=current_user.is_foreign,
            created_at=current_user.created_at,
            updated_at=datetime.now()
        )

    @staticmethod
    def map_user_to_user_read_dto(user: User) -> UserReadDTO:
        return UserReadDTO(
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
