from abc import ABC, abstractmethod


class AbstractPasswordHandler(ABC):
    """Abstract class for handling password operations."""

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash the given password."""
        pass

    @abstractmethod
    def validate_password(self, password: str, hashed_password: str) -> bool:
        """Validate if the given password matches the hashed password."""
        pass
