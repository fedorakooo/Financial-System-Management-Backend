from src.application.dtos.account import AccountReadDTO
from src.domain.entities.deposit import DepositAccount, DepositTransaction
from src.application.dtos.deposit import (
    DepositAccountCreateDTO,
    DepositAccountReadDTO,
    DepositTransactionReadDTO
)

class DepositMapper:
    """Utility class for mapping between Deposit-related DTOs and domain entities."""

    @staticmethod
    def map_deposit_account_create_dto_to_deposit_account(
            dto: DepositAccountCreateDTO,
            account_id: int
    ) -> DepositAccount:
        return DepositAccount(
            account_id=account_id,
            interest_rate=dto.interest_rate,
            user_id=dto.user_id,
            from_account_id=dto.from_account_id
        )

    @staticmethod
    def map_deposit_account_to_deposit_account_read_dto(
            deposit_account: DepositAccount,
            account_read_dto: AccountReadDTO
    ) -> DepositAccountReadDTO:
        return DepositAccountReadDTO(
            from_account_id=deposit_account.from_account_id,
            interest_rate=deposit_account.interest_rate,
            id=deposit_account.id,
            account=account_read_dto,
        )

    @staticmethod
    def map_deposit_transaction_to_deposit_transaction_read_dto(
            deposit_transaction: DepositTransaction
    ) -> DepositTransactionReadDTO:
        return DepositTransactionReadDTO(
            deposit_account_id=deposit_transaction,
            type=deposit_transaction.type,
            amount=deposit_transaction.amount,
            created_at=deposit_transaction.created_at
        )
