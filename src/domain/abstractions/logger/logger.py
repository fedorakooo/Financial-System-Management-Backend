from abc import ABC, abstractmethod


class AbstractLogger(ABC):
    """Abstract class for logging messages."""

    @abstractmethod
    def info(self, message: str) -> None:
        """Add a regular message to the logs."""
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """Add an error message to the logs."""
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        """Add warning to the logs."""
        pass
