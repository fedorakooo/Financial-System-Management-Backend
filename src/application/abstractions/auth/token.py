from abc import ABC, abstractmethod
from typing import Any

from src.application.dtos.user import UserReadDTO


class AbstractTokenService(ABC):
    """Abstract service for generating and decoding tokens."""

    @abstractmethod
    def create_access_token(self, user: UserReadDTO) -> str:
        """Generate an access token for the given user."""
        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict[str, Any]:
        """Decode the given token and return the payload as a dictionary."""
        pass
