from abc import ABC, abstractmethod


class AbstractPasswordService(ABC):
    """Abstract service for handling password operations."""

    @abstractmethod
    def validate_password(self, password: str, hashed_password: str) -> bool:
        """Validate user credentials by comparing password with hashed password."""
        pass
