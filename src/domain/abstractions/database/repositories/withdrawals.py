from abc import ABC, abstractmethod

from src.domain.entities.withdrawal import Withdrawal


class AbstractWithdrawalRepository(ABC):
    """Abstract class for a withdrawal repository."""

    @abstractmethod
    async def get_withdrawal_by_id(self, withdrawal_id: int) -> Withdrawal:
        """Fetches a withdrawal by its unique identifier.

        Raises:
            NotFoundError: If the withdrawal with the specified id is not found."""
        pass

    @abstractmethod
    async def get_withdrawals(self) -> list[Withdrawal]:
        """Fetches all withdrawals from the repository."""
        pass

    @abstractmethod
    async def get_withdrawals_by_account_id(self, account_id: int) -> list[Withdrawal]:
        """Fetches all withdrawals associated with a specific user."""
        pass

    async def create_withdrawal(self, withdrawal_create: Withdrawal) -> Withdrawal:
        """Creates a new withdrawal.

        Raises:
            UniqueConstraintError: If there is a violation of unique constraints.
            ForeignKeyError: If a foreign key constraint violation occurs.
        """
        pass
