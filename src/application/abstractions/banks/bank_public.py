from abc import ABC, abstractmethod

from src.application.dtos.bank import BankReadDTO
from src.application.dtos.user import UserAccessDTO, UserReadDTO


class AbstractBankPublicService(ABC):
    """Abstract service for retrieving and managing access to bank information."""

    @abstractmethod
    async def get_bank_by_id(self, bank_id: int) -> BankReadDTO:
        """Retrieve bank information by its ID."""
        pass

    @abstractmethod
    async def get_banks(self) -> list[BankReadDTO]:
        """Retrieve a list of banks."""
        pass
