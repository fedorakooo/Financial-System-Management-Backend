from abc import ABC, abstractmethod

from src.domain.entities.bank import Bank


class AbstractBankRepository(ABC):
    """Abstract class for a bank repository."""

    @abstractmethod
    async def get_bank_by_id(self, bank_id: int) -> Bank:
        """Fetches a bank by its unique identifier.

        Raises:
            NotFoundError: If the bank with the specified id is not found.
        """
        pass

    @abstractmethod
    async def get_banks(self) -> list[Bank]:
        """Fetches banks from the repository."""
        pass

    @abstractmethod
    async def create_bank(self, bank_create: Bank) -> Bank:
        """Creates a new bank.

        Raises:
            UniqueConstraintError: If there is a violation of unique constraints.
            ForeignKeyError: If a foreign key constraint violation occurs.
        """
        pass

    @abstractmethod
    async def update_bank_by_id(self, bank_id: int, bank_update: Bank) -> Bank:
        """Updates a bank by its unique identifier.

        Raises:
            NotFoundError: If the bank with the specified id is not found.
            NoFieldsToUpdateError: If no fields are provided for updating.
            UniqueConstraintError: If there is a violation of unique constraints.
        """
        pass

    @abstractmethod
    async def delete_bank_by_id(self, bank_id: int) -> None:
        """Deletes a bank by its unique identifier.

        Raises:
            NotFoundError: If the bank with the specified id is not found.
        """
        pass
