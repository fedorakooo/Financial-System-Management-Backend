from abc import ABC, abstractmethod

from src.application.dtos.user import UserReadDTO


class AbstractAuthUserService(ABC):
    """Abstract service for user authentication and password management."""

    @abstractmethod
    async def get_user_by_phone_number(self, phone_number: str) -> UserReadDTO:
        """Retrieve a user by their phone number."""
        pass

    @abstractmethod
    async def get_user_hashed_password_by_phone_number(self, phone_number: str) -> str:
        """Retrieve the hashed password for a user based on their phone number."""
        pass
