from src.application.abstractions.transfers.transfer_management import AbstractTransferManagementService
from src.application.dtos.transfer import TransferReadDTO
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.transfer import TransferMapper
from src.domain.abstractions.database.uows.transfer import AbstractTransferUnitOfWork
from src.application.services.transfer.access_control import TransferManagementAccessControlService as AccessControl
from src.domain.enums.account import AccountStatus
from src.domain.enums.transfer import TransferStatus
from src.domain.exceptions.account import SuspendedAccountOperationError
from src.domain.exceptions.transfer import TransferAlreadyCanceledError, InsufficientRecipientBalanceError


class TransferManagementService(AbstractTransferManagementService):
    def __init__(self, uow: AbstractTransferUnitOfWork):
        self.uow = uow

    async def get_transfer_by_id(self, transfer_id: int, requesting_user: UserAccessDTO) -> TransferReadDTO:
        AccessControl.can_get_transaction(requesting_user)
        async with self.uow as uow:
            transfer = await self.uow.transfer_repository.get_transfer_by_id(transfer_id)
        transfer_dto = TransferMapper.map_transfer_to_transfer_read_dto(transfer)
        return transfer_dto

    async def reverse_transfer_by_id(self, transfer_id: int, requesting_user: UserAccessDTO) -> TransferReadDTO:
        AccessControl.can_reverse_transaction(requesting_user)
        async with self.uow as uow:
            transfer = await self.uow.transfer_repository.get_transfer_by_id(transfer_id)
            if transfer.status is TransferStatus.CANCELED:
                raise TransferAlreadyCanceledError(transfer.id, transfer.status)
            sender_account = await self.uow.account_repository.get_account_by_id(transfer.from_account_id)
            if sender_account.status is not AccountStatus.ACTIVE:
                raise SuspendedAccountOperationError(sender_account.id, sender_account.status)
            receive_account = await self.uow.account_repository.get_account_by_id(transfer.to_account_id)
            if receive_account.status is not AccountStatus.ACTIVE:
                raise SuspendedAccountOperationError(receive_account.id, receive_account.status)
            if receive_account.balance < transfer.amount:
                raise InsufficientRecipientBalanceError(
                    account_id=receive_account.id,
                    current_balance=receive_account.balance,
                    required_amount=transfer.amount
                )

            new_sender_account_balance = sender_account.balance + transfer.amount
            new_receive_account_balance = receive_account.balance - transfer.amount
            await self.uow.account_repository.update_account_balance(sender_account.id, new_sender_account_balance)
            await self.uow.account_repository.update_account_balance(receive_account.id, new_receive_account_balance)

            updated_transfer = await self.uow.transfer_repository.update_transfer_status_by_id(
                transfer.id,
                TransferStatus.CANCELED
            )
        updated_transfer_dto = TransferMapper.map_transfer_to_transfer_read_dto(updated_transfer)
        return updated_transfer_dto

