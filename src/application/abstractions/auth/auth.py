from abc import ABC, abstractmethod

from src.application.dtos.user import UserAccessDTO


class AbstractAuthService(ABC):
    """Abstract service for handling authentication operations."""

    @abstractmethod
    def get_current_active_auth_user(self, token: str) -> UserAccessDTO:
        """Retrieve the current active authenticated user based on the provided token."""
        pass
