from src.domain.entities.user import User
from src.domain.enums.user import UserRole


class UserDatabaseMapper:
    """Utility class for mapping between database rows and User entities."""

    @staticmethod
    def from_db_row(row: dict) -> User:
        return User(
            id=row["id"],
            name=row["name"],
            passport_number=row["passport_number"],
            phone_number=row["phone_number"],
            email=row["email"],
            role=UserRole(row["role"]),
            hashed_password=row["hashed_password"],
            is_active=row["is_active"],
            is_foreign=row["is_foreign"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    @staticmethod
    def to_db_row(user: User) -> dict:
        return {
            "name": user.name,
            "passport_number": user.passport_number,
            "phone_number": user.phone_number,
            "email": user.email,
            "role": user.role.value,
            "hashed_password": user.hashed_password,
            "is_active": user.is_active,
            "is_foreign": user.is_foreign,
        }
