from src.domain.entities.withdrawal import Withdrawal
from src.domain.enums.withdrawal import WithdrawalSource


class WithdrawalDatabaseMapper:
    """Utility class for mapping between database rows and withdrawal entities."""

    @staticmethod
    def from_db_row(row: dict) -> Withdrawal:
        return Withdrawal(
            account_id=row["account_id"],
            amount=row["amount"],
            source=WithdrawalSource(row["source"]),
            id=row["id"],
            created_at=row["created_at"]
        )

    @staticmethod
    def to_db_row(withdrawal: Withdrawal) -> dict:
        return {
            "account_id": withdrawal.account_id,
            "amount": withdrawal.amount,
            "source": withdrawal.source.value
        }
