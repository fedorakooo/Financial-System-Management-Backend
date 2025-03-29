from src.application.abstractions.transfers.transfer_profile import AbstractTransferProfileService
from src.application.dtos.transfer import TransferReadDTO, TransferCreateDTO
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.transfer import TransferMapper
from src.application.services.transfer.access_control import TransferProfileAccessControlService as AccessControl
from src.domain.abstractions.database.uows.transfer import AbstractTransferUnitOfWork
from src.domain.enums.account import AccountStatus
from src.domain.exceptions.account import InactiveAccountError
from src.infrastructure.exceptions.repository_exceptions import NotFoundError


class TransferProfileService(AbstractTransferProfileService):
    def __init__(self, uow: AbstractTransferUnitOfWork):
        self.uow = uow

    async def get_transfers_by_account_id(
            self,
            account_id: int,
            requesting_user: UserAccessDTO
    ) -> list[TransferReadDTO]:
        async with self.uow as uow:
            account = await uow.account_repository.get_account_by_id(account_id)
            AccessControl.can_get_transfers(account.user_id, requesting_user)
            transfers = await uow.transfer_repository.get_transfers_by_account_id(account_id)
        transfers_dto = [TransferMapper.map_transfer_to_transfer_read_dto(transfer) for transfer in transfers]
        return transfers_dto

    async def create_transfer(
            self,
            transfer_create_dto: TransferCreateDTO,
            requesting_user: UserAccessDTO
    ) -> TransferReadDTO:
        async with self.uow as uow:
            sender_account = await uow.account_repository.get_account_by_id(transfer_create_dto.from_account_id)
            AccessControl.can_create_transfer(sender_account.user_id, requesting_user)
            if sender_account.status is not AccountStatus.ACTIVE:
                raise InactiveAccountError(sender_account.status)
            receive_account = await uow.account_repository.get_account_by_id(transfer_create_dto.to_account_id)
            if receive_account.status is not AccountStatus.ACTIVE:
                raise NotFoundError(f"Account with id {receive_account.status} not found")

            new_sender_account_balance = sender_account.balance - transfer_create_dto.amount
            new_receiver_account_balance = receive_account.balance + transfer_create_dto.amount
            transfer_create = TransferMapper.map_transfer_create_dto_to_transfer(transfer_create_dto)

            created_transfer = await uow.transfer_repository.create_transfer(transfer_create)
            await uow.account_repository.update_account_balance(sender_account.id, new_sender_account_balance)
            await uow.account_repository.update_account_balance(receive_account.id, new_receiver_account_balance)

        created_transfer_dto = TransferMapper.map_transfer_to_transfer_read_dto(created_transfer)
        return created_transfer_dto
