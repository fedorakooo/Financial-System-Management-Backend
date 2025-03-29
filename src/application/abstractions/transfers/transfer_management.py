from abc import ABC, abstractmethod

from src.application.dtos.transfer import TransferReadDTO
from src.application.dtos.user import UserAccessDTO


class AbstractTransferManagementService(ABC):
    """Abstract service for staff-level users to manage transfers."""

    @abstractmethod
    async def get_transfer_by_id(self, transfer_id: int, requesting_user: UserAccessDTO) -> TransferReadDTO:
        pass

    @abstractmethod
    async def reverse_transfer_by_id(self, transfer_id: int, requesting_user: UserAccessDTO) -> TransferReadDTO:
        pass