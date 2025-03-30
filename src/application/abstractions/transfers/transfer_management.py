from abc import ABC, abstractmethod

from src.application.dtos.transfer import TransferReadDTO
from src.application.dtos.user import UserAccessDTO


class AbstractTransferManagementService(ABC):
    """Abstract service for staff-level users to manage transfers."""

    @abstractmethod
    async def get_transfer_by_id(self, transfer_id: int, requesting_user: UserAccessDTO) -> TransferReadDTO:
        """Fetches a transfer by its identifier for an authorized staff member.

        Raises:
            ForbiddenError: If the requesting user cannot access this resource.
            NotFoundError: If the requested resource does not exist.
        """
        pass

    @abstractmethod
    async def reverse_transfer_by_id(self, transfer_id: int, requesting_user: UserAccessDTO) -> TransferReadDTO:
        """Reverses a completed transfer and marks it canceled in the same transaction.

        Locks the transfer and both participating accounts before changing balances.

        Raises:
            ForbiddenError: If the staff member cannot reverse transfers.
            NotFoundError: If the transfer or either account does not exist.
            TransferAlreadyCanceledError: If the transfer has already been reversed.
            SuspendedAccountOperationError: If either account is not active.
            InsufficientRecipientBalanceError: If the recipient cannot return the transferred amount.
        """
        pass