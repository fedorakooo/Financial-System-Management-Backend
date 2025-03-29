from src.application.dtos.withdrawal import WithdrawalCreateDTO, WithdrawalReadDTO
from src.domain.entities.withdrawal import Withdrawal


class WithdrawalMapper:
    """Utility class for mapping between Withdrawal-related DTOs and domain entities."""

    @staticmethod
    def map_withdrawal_create_dto_to_withdrawal(dto: WithdrawalCreateDTO, account_id: int) -> Withdrawal:
        return Withdrawal(
            account_id=account_id,
            amount=dto.amount,
            source=dto.source,
        )

    @staticmethod
    def map_withdrawal_to_withdrawal_read_dto(withdrawal: Withdrawal) -> WithdrawalReadDTO:
        return WithdrawalReadDTO(
            id=withdrawal.id,
            account_id=withdrawal.account_id,
            amount=withdrawal.amount,
            source=withdrawal.source,
            created_at=withdrawal.created_at
        )
