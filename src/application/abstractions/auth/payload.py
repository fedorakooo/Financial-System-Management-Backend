from abc import ABC, abstractmethod

from src.application.dtos.user import UserAuthDTO


class AbstractPayloadExtractorService(ABC):
    """Abstract service for extracting user data from a payload."""

    @abstractmethod
    def extract_user_from_payload(self, payload: dict) -> UserAuthDTO:
        """Extract user information from payload."""
        pass
