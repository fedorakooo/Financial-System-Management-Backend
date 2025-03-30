from src.application.abstractions.accounts.account_management import AbstractAccountManagementService
from src.application.dtos.account import AccountReadDTO, AccountUpdateStaffDTO
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.account import AccountMapper
from src.application.services.accounts.access_control import AccountManagementAccessControlService as AccessControl
from src.domain.abstractions.database.uows.account import AbstractAccountUnitOfWork
from src.domain.enums.account import AccountType, AccountStatus
from src.domain.exceptions.account import StatusChangeNotAllowedError
from src.domain.exceptions.payment import InvalidOperationError


class AccountManagementService(AbstractAccountManagementService):
    def __init__(self, uow: AbstractAccountUnitOfWork):
        self.uow = uow

    async def get_accounts_by_user_id(self, user_id: int, requesting_user: UserAccessDTO) -> list[AccountReadDTO]:
        AccessControl.can_get_accounts(requesting_user)

        async with self.uow as uow:
            accounts = await uow.account_repository.get_accounts_by_user_id(user_id)

        accounts_dto = [AccountMapper.map_account_to_account_read_dto(account) for account in accounts]
        return accounts_dto

    async def update_account_by_id(
            self,
            account_id: int,
            account_update_dto: AccountUpdateStaffDTO,
            requesting_user: UserAccessDTO
    ) -> AccountReadDTO:
        AccessControl.can_update_account(requesting_user)
        async with self.uow as uow:
            current_account = await self.uow.account_repository.get_account_by_id(account_id)
            if current_account.type is AccountType.LOAN and account_update_dto.status is AccountStatus.ACTIVE:
                raise StatusChangeNotAllowedError(current_account.status, account_update_dto.status)
            if current_account.status is AccountStatus.CANCELLED:
                raise StatusChangeNotAllowedError(current_account.status, account_update_dto.status)
            if account_update_dto.status is AccountStatus.CANCELLED and current_account.balance != 0:
                raise InvalidOperationError("Cannot cancel an account with a nonzero balance")
            account_update = AccountMapper.map_account_update_staff_dto_to_account(account_update_dto, current_account)
            updated_account = await self.uow.account_repository.update_account(account_id, account_update)
        updated_account_dto = AccountMapper.map_account_to_account_read_dto(updated_account)
        return updated_account_dto

    async def delete_account_by_id(self, account_id: int, requesting_user: UserAccessDTO) -> None:
        AccessControl.can_delete_account(requesting_user)

        async with self.uow as uow:
            await uow.account_repository.delete_account_by_id(account_id)
