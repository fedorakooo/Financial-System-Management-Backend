from src.domain.entities.account import Account
from src.domain.entities.addition import Addition
from src.domain.enums.addition import AdditionSource


class AdditionDatabaseMapper:
    """Utility class for mapping between database rows and Addition entities."""

    @staticmethod
    def from_db_row(row: dict) -> Account:
        return Addition(
            account_id=row["account_id"],
            amount=row["amount"],
            source=AdditionSource(row["source"]),
            id=row["id"],
            created_at=row["created_at"]
        )

    @staticmethod
    def to_db_row(addition: Addition) -> dict:
        return {
            "account_id": addition.account_id,
            "amount": addition.amount,
            "source": addition.source.value
        }
