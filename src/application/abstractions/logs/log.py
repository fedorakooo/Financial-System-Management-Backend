from abc import ABC, abstractmethod


class AbstractLogService(ABC):
    """Abstract service for logging different types of messages."""

    @abstractmethod
    def info(self, message: str) -> None:
        """Log an informational message."""
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """Log an error message."""
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        """Log a warning message."""
        pass
