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
        pass