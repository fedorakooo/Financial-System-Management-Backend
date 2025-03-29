from abc import abstractmethod, ABC

from src.application.dtos.bank import BankReadDTO, BankCreateDTO, BankUpdateDTO
from src.application.dtos.user import UserAccessDTO


class AbstractBankManagementService(ABC):
    """Abstract service for staff-level users to manage banks."""

    @abstractmethod
    async def get_bank_by_id(self, bank_id: int) -> BankReadDTO:
        """Retrieve bank information by its ID."""
        pass

    @abstractmethod
    async def get_banks(self) -> list[BankReadDTO]:
        """Retrieve a list of banks."""
        pass

    @abstractmethod
    async def create_bank(self, bank_create_dto: BankCreateDTO, requesting_user: UserAccessDTO) -> BankReadDTO:
        """Create a new bank based on the provided information."""
        pass

    @abstractmethod
    async def update_bank_by_id(
            self,
            bank_id: int,
            bank_update_dto: BankUpdateDTO,
            requesting_user: UserAccessDTO
    ) -> BankReadDTO:
        """Update an existing bank's information by its ID. """
        pass

    @abstractmethod
    async def delete_bank_by_id(self, bank_id: int, requesting_user: UserAccessDTO) -> None:
        """Delete a bank by its ID."""
        pass
