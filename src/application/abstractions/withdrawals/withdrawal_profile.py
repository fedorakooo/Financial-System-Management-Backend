from abc import ABC, abstractmethod

from src.application.dtos.withdrawal import WithdrawalReadDTO, WithdrawalCreateDTO
from src.application.dtos.user import UserAccessDTO


class AbstractWithdrawalProfileService(ABC):
    """Abstract service for managing user withdrawals."""

    @abstractmethod
    async def get_withdrawals_by_account_id(
            self,
            account_id: int,
            requesting_user: UserAccessDTO
    ) -> list[WithdrawalReadDTO]:
        """Retrieve withdrawals associated with the requesting account."""
        pass

    @abstractmethod
    async def create_withdrawal(
            self,
            withdrawal_create_dto: WithdrawalCreateDTO,
            requesting_user: UserAccessDTO
    ) -> WithdrawalReadDTO:
        """Create a new withdrawal for the requesting user."""
        pass
