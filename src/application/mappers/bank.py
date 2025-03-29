from datetime import datetime

from src.domain.entities.bank import Bank
from src.application.dtos.bank import BankCreateDTO, BankUpdateDTO, BankReadDTO


class BankMapper:
    """Utility class for mapping between Bank-related DTOs and domain entities."""

    @staticmethod
    def map_bank_create_dto_to_addition(dto: BankCreateDTO) -> Bank:
        return Bank(
            name=dto.name,
            bic=dto.name,
            address=dto.name,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    @staticmethod
    def map_bank_update_dto_to_bank(dto: BankUpdateDTO, current_bank: Bank) -> Bank:
        return Bank(
            id=current_bank.id,
            name=dto.name if dto.name else current_bank.name,
            bic=current_bank.bic,
            address=dto.address if dto.address else current_bank.address,
            created_at=current_bank.created_at,
            updated_at=datetime.now()
        )

    @staticmethod
    def map_bank_to_bank_read_dto(bank: Bank) -> BankReadDTO:
        return BankReadDTO(
            id=bank.id,
            name=bank.name,
            bic=bank.bic,
            address=bank.address,
            created_at=bank.created_at,
            updated_at=bank.updated_at
        )
