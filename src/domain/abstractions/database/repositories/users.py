from abc import ABC, abstractmethod

from src.domain.entities.user import User


class AbstractUserRepository(ABC):
    """Abstract class for a user repository."""

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User:
        """Fetches a user by its unique identifier.

        Raises:
            NotFoundError: If the user with the specified id is not found.
        """
        pass

    async def get_user_by_passport_number(self, passport_number: str) -> User:
        pass

    @abstractmethod
    async def get_user_by_phone_number(self, phone_number: str) -> User:
        """Fetches a user by their phone number.

        Raises:
            NotFoundError: If the user with the specified phone number is not found.
        """
        pass

    @abstractmethod
    async def get_user_hashed_password_by_phone_number(self, phone_number: str) -> str:
        """Fetches the hashed password of a user by their phone number.

        Raises:
            NotFoundError: If the user with the specified phone number is not found.
        """
        pass

    @abstractmethod
    async def get_users(self) -> list[User]:
        """Fetches users from the repository."""
        pass

    @abstractmethod
    async def create_user(self, user_create: User) -> User:
        """Creates a new user.

        Raises:
            UniqueConstraintError: If there is a violation of unique constraints.
        """
        pass

    @abstractmethod
    async def update_user_by_id(self, user_id: int, user_update: User) -> User:
        """Updates a user by its unique identifier.

        Raises:
            NotFoundError: If the user with the specified id is not found.
            NoFieldsToUpdateError: If no fields are provided for updating.
            UniqueConstraintError: If there is a violation of unique constraints.
        """
        pass

    @abstractmethod
    async def delete_user_by_id(self, user_id: int) -> None:
        """Deletes a user by its unique identifier.

        Raises:
            NotFoundError: If the user with the specified id is not found.
        """
        pass
