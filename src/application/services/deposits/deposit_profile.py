from src.application.abstractions.deposits.deposit_profile import AbstractDepositProfileService
from src.application.dtos.account import AccountCreateDTO
from src.application.dtos.deposit import DepositAccountReadDTO, DepositAccountCreateDTO, DepositTransactionReadDTO, \
    DepositTransactionCreateClientDTO
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.account import AccountMapper
from src.application.mappers.deposit import DepositMapper
from src.domain.abstractions.database.uows.deposit import AbstractDepositUnitOfWork
from src.application.services.deposits.access_control import DepositProfileAccessControlService as AccessControl
from src.domain.entities.deposit import DepositTransaction
from src.domain.enums.account import AccountType, AccountStatus
from src.domain.enums.deposit import DepositTransactionType


class DepositProfileService(AbstractDepositProfileService):
    def __init__(self, uow: AbstractDepositUnitOfWork):
        self.uow = uow

    async def get_deposit_account_by_id(
            self,
            deposit_account_id: int,
            requesting_user: UserAccessDTO
    ) -> DepositAccountReadDTO:
        async with self.uow as uow:
            deposit_account = await self.uow.deposit_repository.get_deposit_account_by_id(deposit_account_id)
            account = await self.uow.account_repository.get_account_by_id(deposit_account.account_id)
            AccessControl.can_get_deposit_accounts(account.user_id, requesting_user)
        account_read_dto = AccountMapper.map_account_to_account_read_dto(account)
        deposit_account_dto = DepositMapper.map_deposit_account_to_deposit_account_read_dto(
            deposit_account,
            account_read_dto
        )
        return deposit_account_dto

    async def create_deposit_account(
            self,
            deposit_account_create_dto: DepositAccountCreateDTO,
            account_create_dto: AccountCreateDTO,
            requesting_user: UserAccessDTO
    ) -> DepositAccountReadDTO:
        AccessControl.can_create_deposit_account(requesting_user)
        account_create = AccountMapper.map_account_create_dto_to_account(
            account_create_dto,
            requesting_user.id,
            AccountType.DEPOSIT,
            AccountStatus.ON_CONSIDERATION
        )
        async with self.uow as uow:
            created_account = await self.uow.account_repository.create_account(account_create)
            deposit_account_create = DepositMapper.map_deposit_account_create_dto_to_deposit_account(
                deposit_account_create_dto,
                created_account.id
            )
            created_deposit_account = await self.uow.deposit_repository.create_deposit_account(deposit_account_create)
        created_account_dto = AccountMapper.map_account_to_account_read_dto(created_account)
        return DepositMapper.map_deposit_account_to_deposit_account_read_dto(
            created_deposit_account,
            created_account_dto
        )

    async def transfer_from_deposit_to_account(
            self,
            deposit_transaction_create_client_dto: DepositTransactionCreateClientDTO,
            requesting_user: UserAccessDTO
    ) -> DepositTransactionReadDTO:
        async with self.uow as uow:
            deposit_account = await self.uow.deposit_repository.get_deposit_account_by_id(
                deposit_transaction_create_client_dto.deposit_account_id
            )
            AccessControl.can_create_deposit_transaction(deposit_account.user_id, requesting_user)
            account = await self.uow.account_repository.get_account_by_id(deposit_account.account_id)
            receiver_account = await self.uow.account_repository.get_account_by_id(
                deposit_transaction_create_client_dto.account_id
            )
            created_deposit_transaction = await self.uow.deposit_repository.create_deposit_transaction(
                DepositTransaction(
                    from_account_id=deposit_transaction_create_client_dto.deposit_account_id,
                    to_account_id=deposit_transaction_create_client_dto.account_id,
                    type=DepositTransactionType.WITHDRAWAL,
                    amount=account.balance
                )
            )
            await self.uow.account_repository.update_account_balance(
                receiver_account.id,
                receiver_account.balance + account.balance
            )
            await self.uow.account_repository.update_account_balance(account.id, 0)
            await self.uow.account_repository.update_account_status(account.id, AccountStatus.BLOCKED)
        return DepositMapper.map_deposit_transaction_to_deposit_transaction_read_dto(created_deposit_transaction)

