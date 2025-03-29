from src.application.abstractions.withdrawals.withdrawal_profile import AbstractWithdrawalProfileService
from src.application.dtos.withdrawal import WithdrawalReadDTO, WithdrawalCreateDTO
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.withdrawal import WithdrawalMapper
from src.application.services.withdrawals.access_control import WithdrawalProfileAccessControlService as AccessControl
from src.domain.abstractions.database.uows.withdrawal import AbstractWithdrawalUnitOfWork
from src.domain.enums.account import AccountStatus, AccountType
from src.domain.exceptions.account import InsufficientFundsError, InactiveAccountError, InvalidAccountTypeError


class WithdrawalProfileService(AbstractWithdrawalProfileService):
    def __init__(self, uow: AbstractWithdrawalUnitOfWork):
        self.uow = uow

    async def get_withdrawals_by_account_id(
            self,
            account_id: int,
            requesting_user: UserAccessDTO
    ) -> list[WithdrawalReadDTO]:
        async with self.uow as uow:
            account = await self.uow.account_repository.get_account_by_id(account_id)
            AccessControl.can_get_withdrawals(account.user_id, requesting_user)

            withdrawals = await self.uow.withdrawal_repository.get_withdrawals_by_account_id(account_id)

        withdrawals_dto = [WithdrawalMapper.map_withdrawal_to_withdrawal_read_dto(withdrawal) for withdrawal in
                           withdrawals]
        return withdrawals_dto

    async def create_withdrawal(
            self,
            withdrawal_create_dto: WithdrawalCreateDTO,
            requesting_user: UserAccessDTO
    ) -> WithdrawalReadDTO:
        async with self.uow as uow:
            account = await uow.account_repository.get_account_by_id(withdrawal_create_dto.account_id)
            AccessControl.can_create_withdrawal(account.user_id, requesting_user)
            if account.status is not AccountStatus.ACTIVE:
                raise InactiveAccountError(account.status)
            if account.type is not AccountType.SETTLEMENT:
                raise InvalidAccountTypeError(account.type, AccountType.SETTLEMENT)
            new_account_balance = account.balance - withdrawal_create_dto.amount
            if new_account_balance < 0:
                raise InsufficientFundsError(account.balance)
            created_withdrawal = await uow.withdrawal_repository.create_withdrawal(withdrawal_create_dto)
            await uow.account_repository.update_account_balance(withdrawal_create_dto.account_id, new_account_balance)

        created_withdrawal_dto = WithdrawalMapper.map_withdrawal_to_withdrawal_read_dto(created_withdrawal)
        return created_withdrawal_dto
