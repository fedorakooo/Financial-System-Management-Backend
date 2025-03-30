from abc import ABC, abstractmethod

from src.application.dtos.account import AccountCreateDTO
from src.application.dtos.deposit import DepositAccountReadDTO, DepositAccountCreateDTO, DepositTransactionReadDTO, \
    DepositTransactionCreateClientDTO
from src.application.dtos.user import UserAccessDTO


class AbstractDepositProfileService(ABC):
    """Abstract service for managing user deposits."""

    @abstractmethod
    async def get_deposit_account_by_id(
            self,
            deposit_account_id: int,
            requesting_user: UserAccessDTO
    ) -> DepositAccountReadDTO:
        """Fetches a deposit and its underlying account for the owning client.

        Raises:
            ForbiddenError: If the requesting user cannot access this resource.
            NotFoundError: If the requested resource does not exist.
        """
        pass

    @abstractmethod
    async def create_deposit_account(
            self,
            deposit_account_create_dto: DepositAccountCreateDTO,
            account_create_dto: AccountCreateDTO,
            requesting_user: UserAccessDTO
    ) -> DepositAccountReadDTO:
        """Create a new deposit account for the requesting user."""
        pass

    @abstractmethod
    async def transfer_from_deposit_to_account(
            self,
            deposit_transaction_create_client_dto: DepositTransactionCreateClientDTO,
            requesting_user: UserAccessDTO
    ) -> DepositTransactionReadDTO:
        """Transfers the entire active deposit balance to the client's active settlement account.

        Records the withdrawal and blocks the emptied deposit in one transaction.

        Raises:
            ForbiddenError: If the client does not own both accounts.
            NotFoundError: If either account does not exist.
            InactiveAccountError: If either account is not active.
            InvalidAccountTypeError: If the recipient is not a settlement account.
            InvalidOperationError: If the accounts are identical or the deposit is empty.
        """
        pass