from abc import ABC, abstractmethod

from src.application.dtos.account import AccountReadDTO, AccountUpdateStaffDTO
from src.application.dtos.user import UserAccessDTO


class AbstractAccountManagementService(ABC):
    """Abstract service for staff-level users to manage accounts."""

    @abstractmethod
    async def get_accounts_by_user_id(self, user_id: int, requesting_user: UserAccessDTO) -> list[AccountReadDTO]:
        """Retrieve accounts information by user id."""
        pass

    @abstractmethod
    async def update_account_by_id(
            self,
            account_id: int,
            account_update_dto: AccountUpdateStaffDTO,
            requesting_user: UserAccessDTO
    ) -> AccountReadDTO:
        """Update an existing account's information by its ID. """
        pass

    @abstractmethod
    async def delete_account_by_id(self, account_id: int, requesting_user: UserAccessDTO) -> None:
        """Delete an account by its ID."""
        pass
