from datetime import datetime

from src.application.dtos.addition import AdditionCreateDTO, AdditionReadDTO
from src.domain.entities.addition import Addition


class AdditionMapper:
    """Utility class for mapping between Addition-related DTOs and domain entities."""

    @staticmethod
    def map_addition_create_dto_to_addition(dto: AdditionCreateDTO, account_id: int) -> Addition:
        return Addition(
            account_id=account_id,
            amount=dto.amount,
            source=dto.source,
            created_at=datetime.now()
        )

    @staticmethod
    def map_addition_to_addition_read_dto(addition: Addition) -> AdditionReadDTO:
        return AdditionReadDTO(
            id=addition.id,
            account_id=addition.account_id,
            amount=addition.amount,
            source=addition.source,
            created_at=addition.created_at
        )
