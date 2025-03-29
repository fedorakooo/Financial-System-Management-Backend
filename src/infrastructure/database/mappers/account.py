from decimal import Decimal

from src.domain.entities.account import Account
from src.domain.enums.account import AccountStatus, AccountType


class AccountDatabaseMapper:
    """Utility class for mapping between database rows and Account entities."""

    @staticmethod
    def from_db_row(row: dict) -> Account:
        return Account(
            user_id=row["user_id"],
            bank_id=row["bank_id"],
            id=row.get("id"),
            balance=Decimal(row["balance"]),
            status=AccountStatus(row["status"]),
            type=AccountType(row["type"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    @staticmethod
    def to_db_row(account: Account) -> dict:
        return {
            "bank_id": account.bank_id,
            "status": account.status.value,
            "type": account.type.value,
            "user_id": account.user_id
        }
