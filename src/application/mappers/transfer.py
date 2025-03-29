from src.application.dtos.transfer import TransferCreateDTO, TransferReadDTO
from src.domain.entities.transfer import Transfer


class TransferMapper:
    """Utility class for mapping between Transfer-related DTOs and domain entities."""

    @staticmethod
    def map_transfer_create_dto_to_transfer(dto: TransferCreateDTO) -> Transfer:
        return Transfer(
            from_account_id=dto.from_account_id,
            to_account_id=dto.to_account_id,
            amount=dto.amount,
        )

    @staticmethod
    def map_transfer_to_transfer_read_dto(transfer: Transfer) -> TransferReadDTO:
        return TransferReadDTO(
            from_account_id=transfer.from_account_id,
            to_account_id=transfer.to_account_id,
            amount=transfer.amount,
            id=transfer.id,
            status=transfer.status,
            updated_at=transfer.updated_at,
            created_at=transfer.created_at
        )
