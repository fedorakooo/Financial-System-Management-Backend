from abc import ABC, abstractmethod
from decimal import Decimal

from src.domain.entities.account import Account
from src.domain.enums.account import AccountStatus


class AbstractAccountRepository(ABC):
    """Abstract class for an account repository."""

    @abstractmethod
    async def get_account_by_id(self, account_id) -> Account:
        """Fetches an account by its unique identifier.

        Raises:
            NotFoundError: If the account with the specified id is not found.
        """
        pass

    @abstractmethod
    async def get_accounts_by_user_id(self, user_id) -> list[Account]:
        """Fetches all accounts associated with a specific user."""
        pass

    @abstractmethod
    async def create_account(self, account_create: Account) -> Account:
        """Creates a new account.

        Raises:
            UniqueConstraintError: If there is a violation of unique constraints.
            ForeignKeyError: If a foreign key constraint violation occurs.
        """
        pass

    @abstractmethod
    async def update_account(self, account_id: int, account_update: Account) -> Account:
        """Updates an account by its unique identifier.

        Raises:
            NotFoundError: If the account with the specified id is not found.
            NoFieldsToUpdateError: If no fields are provided for updating.
        """
        pass

    @abstractmethod
    async def update_account_status(self, account_id: int, new_status: AccountStatus) -> None:
        pass

    @abstractmethod
    async def update_account_balance(self, account_id: int, new_balance: Decimal) -> None:
        pass

    @abstractmethod
    async def delete_account_by_id(self, account_id: int) -> None:
        """Deletes an account by its unique identifier.

        Raises:
            NotFoundError: If the account with the specified id is not found.
        """
        pass
