from src.application.mappers.bank import BankMapper
from src.application.services.banks.access_control import BankManagementAccessControlService
from src.application.abstractions.banks.bank_management import AbstractBankManagementService
from src.application.dtos.bank import BankReadDTO, BankCreateDTO, BankUpdateDTO
from src.application.dtos.user import UserAccessDTO
from src.domain.abstractions.database.uows.bank import AbstractBankUnitOfWork


class BankManagementService(AbstractBankManagementService):
    def __init__(self, uow: AbstractBankUnitOfWork):
        self.uow = uow

    async def get_bank_by_id(self, bank_id: int) -> BankReadDTO:
        async with self.uow as uow:
            bank = await uow.bank_repository.get_bank_by_id(bank_id)
        bank_dto = BankMapper.map_bank_to_bank_read_dto(bank)
        return bank_dto

    async def get_banks(self) -> list[BankReadDTO]:
        async with self.uow as uow:
            banks = await uow.bank_repository.get_banks()
        banks_dto = [BankMapper.map_bank_to_bank_read_dto(bank) for bank in banks]
        return banks_dto

    async def create_bank(self, bank_create_dto: BankCreateDTO, requesting_user: UserAccessDTO) -> BankReadDTO:
        BankManagementAccessControlService.can_create_bank(requesting_user)

        bank_create = BankMapper.map_bank_create_dto_to_addition(bank_create_dto)
        async with self.uow as uow:
            new_bank = await uow.bank_repository.create_bank(bank_create)

        new_bank_dto = BankMapper.map_bank_to_bank_read_dto(new_bank)
        return new_bank_dto

    async def update_bank_by_id(
            self,
            bank_id: int,
            bank_update_dto: BankUpdateDTO,
            requesting_user: UserAccessDTO
    ) -> BankReadDTO:
        BankManagementAccessControlService.can_update_bank(requesting_user)

        async with self.uow as uow:
            current_bank = await uow.bank_repository.get_bank_by_id(bank_id)
            bank_update = BankMapper.map_bank_update_dto_to_bank(bank_update_dto, current_bank)
            updated_bank = await uow.bank_repository.update_bank_by_id(bank_id, bank_update)

        updated_bank_dto = BankMapper.map_bank_to_bank_read_dto(updated_bank)
        return updated_bank_dto

    async def delete_bank_by_id(self, bank_id: int, requesting_user: UserAccessDTO) -> None:
        BankManagementAccessControlService.can_delete_bank(requesting_user)
        async with self.uow as uow:
            await uow.bank_repository.delete_bank_by_id(bank_id)
