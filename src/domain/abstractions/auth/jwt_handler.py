from abc import ABC, abstractmethod

from datetime import timedelta
from typing import Optional, Union


class AbstractJWTHandler(ABC):
    """Abstract class for extracting user data from a JWT payload."""

    @abstractmethod
    def encode(
            self,
            payload: dict,
            expire_timedelta: Optional[timedelta] = None
    ) -> str:
        """Encodes (creates) a JWT token."""
        pass

    @abstractmethod
    def decode(
            self,
            token: Union[str, bytes]
    ) -> dict:
        """Decodes a JWT token and extracts its payload."""
        pass
