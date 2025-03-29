from abc import ABC, abstractmethod
from typing import Optional


class AbstractLoginService(ABC):
    """Abstract service for handling user login operations."""

    @abstractmethod
    async def validate_auth_user(self, phone_number: str, password: str) -> bool:
        """Validate user credentials and return True if valid, else False."""
        pass

    @abstractmethod
    async def authenticate_user(self, phone_number: str, password: str) -> Optional[str]:
        """Validate user credentials and return access token if valid, else return None."""
        pass
