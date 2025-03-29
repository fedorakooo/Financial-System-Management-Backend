from abc import ABC, abstractmethod

from src.application.dtos.transfer import TransferReadDTO, TransferCreateDTO
from src.application.dtos.user import UserAccessDTO


class AbstractTransferProfileService(ABC):
    """Abstract service for managing user transfers."""

    @abstractmethod
    async def get_transfers_by_account_id(
            self,
            account_id: int,
            requesting_user: UserAccessDTO
    ) -> list[TransferReadDTO]:
        """Retrieve transfers associated with the requesting account."""
        pass

    @abstractmethod
    async def create_transfer(
            self,
            transfer_create_dto: TransferCreateDTO,
            requesting_user: UserAccessDTO
    ) -> TransferReadDTO:
        """Create a new transfer for the requesting user."""
        pass
