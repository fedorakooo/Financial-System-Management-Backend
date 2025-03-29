from src.application.abstractions.banks.bank_public import AbstractBankPublicService
from src.application.dtos.bank import BankReadDTO
from src.application.mappers.bank import BankMapper
from src.domain.abstractions.database.uows.bank import AbstractBankUnitOfWork


class BankPublicService(AbstractBankPublicService):
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
