from src.domain.entities.transfer import Transfer
from src.domain.enums.transfer import TransferStatus


class TransferDatabaseMapper:
    """Utility class for mapping between database rows and Transfer entities."""

    @staticmethod
    def from_db_row(row: dict) -> Transfer:
        return Transfer(
            from_account_id=row["from_account_id"],
            to_account_id=row["to_account_id"],
            amount=row["amount"],
            id=row["id"],
            status=TransferStatus(row["status"]),
            updated_at=row["updated_at"],
            created_at=row["created_at"]
        )

    @staticmethod
    def to_db_row(transfer: Transfer) -> dict:
        return {
            "from_account_id": transfer.from_account_id,
            "to_account_id": transfer.to_account_id,
            "amount": transfer.amount
        }
