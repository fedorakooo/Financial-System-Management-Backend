from abc import ABC, abstractmethod
from typing import Any


class AbstractDatabaseConnection(ABC):
    """Abstract class for managing a database connection."""

    @abstractmethod
    async def connect(self) -> None:
        """Establish a connection to the database."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the database connection."""
        pass

    @property
    @abstractmethod
    def connection(self) -> Any:
        """Get the current database connection instance."""
        pass

    @abstractmethod
    async def execute(self, query: str, *args: Any) -> Any:
        """Execute a SQL query that does not return any results."""
        pass

    @abstractmethod
    async def fetch(self, query: str, *args: Any) -> Any:
        """Execute a query and return all rows from the result."""
        pass

    @abstractmethod
    async def fetchrow(self, query: str, *args: Any) -> Any:
        """Execute a query and return a single row from the result."""
        pass

    @abstractmethod
    async def fetchval(self, query: str, *args: Any) -> Any:
        """Execute a query and return a single value."""
        pass
