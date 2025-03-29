from abc import ABC, abstractmethod

from src.domain.entities.addition import Addition


class AbstractAdditionRepository(ABC):
    """Abstract class for an addition repository."""

    @abstractmethod
    async def get_addition_by_id(self, addition_id: int) -> Addition:
        """Fetches an addition by its unique identifier.

        Raises:
            NotFoundError: If the addition with the specified id is not found."""
        pass

    @abstractmethod
    async def get_additions(self) -> list[Addition]:
        """Fetches all additions from the repository."""
        pass

    @abstractmethod
    async def create_addition(self, addition_create: Addition) -> dict:
        pass

    @abstractmethod
    async def get_additions_by_account_id(self, account_id: int) -> list[Addition]:
        """Fetches all additions associated with a specific user."""
        pass
