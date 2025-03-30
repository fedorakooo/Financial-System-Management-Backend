from abc import ABC, abstractmethod

from src.domain.entities.deposit import DepositAccount, DepositTransaction


class AbstractDepositRepository(ABC):
    """Abstract class for a deposit repository."""

    @abstractmethod
    async def get_deposit_account_by_id(self, deposit_account_id: int) -> DepositAccount:
        """Fetches a deposit account by its unique identifier.

        Raises:
            NotFoundError: If the deposit account with the specified id is not found.
        """

    async def create_deposit_transaction(self, deposit_transaction: DepositTransaction) -> DepositTransaction:
        """Records a deposit funding or withdrawal operation within the current transaction."""
        pass

    @abstractmethod
    async def create_deposit_account(self, deposit_account_create: DepositAccount):
        """Creates the deposit details linked to the account, owner, and funding account."""
        pass
