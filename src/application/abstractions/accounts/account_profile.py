from abc import ABC, abstractmethod

from src.application.dtos.account import AccountCreateDTO, AccountReadDTO, AccountUpdateClientDTO
from src.application.dtos.user import UserAccessDTO


class AbstractAccountProfileService(ABC):
    """Abstract service for managing user accounts."""

    @abstractmethod
    async def get_account_by_id(self, account_id: int, requesting_user: UserAccessDTO) -> AccountReadDTO:
        """Retrieve account information by its ID for the requesting user."""
        pass

    @abstractmethod
    async def get_accounts(self, requesting_user: UserAccessDTO) -> list[AccountCreateDTO]:
        """Retrieve accounts associated with the requesting user."""
        pass

    @abstractmethod
    async def create_account(self, account_create: AccountCreateDTO, requesting_user: UserAccessDTO) -> AccountReadDTO:
        """Create a new account for the requesting user."""
        pass

    @abstractmethod
    async def update_account(
            self,
            account_id: int,
            account_update_dto: AccountUpdateClientDTO,
            requesting_user: UserAccessDTO
    ) -> AccountReadDTO:
        """Update an existing account by its ID for the requesting user."""
        pass
