from abc import ABC, abstractmethod

from src.domain.entities.transfer import Transfer
from src.domain.enums.transfer import TransferStatus


class AbstractTransferRepository(ABC):
    """Abstract class for a transfer repository."""

    @abstractmethod
    async def get_transfer_by_id(self, transfer_id: int) -> Transfer:
        """Fetches a transfer by its unique identifier.

        Raises:
            NotFoundError: If the transfer with the specified id is not found."""
        pass

    @abstractmethod
    async def get_transfers_by_account_id(self, account_id: int) -> list[Transfer]:
        """Fetches incoming and outgoing transfers associated with a specific account."""
        pass

    @abstractmethod
    async def create_transfer(self, transfer_create: Transfer) -> Transfer:
        """Records a transfer within the same transaction as the sender and recipient balance changes."""
        pass

    @abstractmethod
    async def update_transfer_status_by_id(self, transfer_id: int, transfer_status: TransferStatus) -> Transfer:
        """Updates a transfer status and returns the updated transfer.

        Raises:
            NotFoundError: If the transfer does not exist.
        """
        pass