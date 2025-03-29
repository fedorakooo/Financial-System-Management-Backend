from src.domain.entities.deposit import DepositAccount, DepositTransaction


class DepositDatabaseMapper:
    """Utility class for mapping between database rows and Deposit entities."""

    @staticmethod
    def from_db_row_to_deposit_account(row: dict) -> DepositAccount:
        return DepositAccount(
            from_account_id=row["from_account_id"],
            account_id=row["account_id"],
            interest_rate=row["interest_rate"],
            user_id=row["user_id"],
            id=row["id"]
        )

    @staticmethod
    def from_db_row_to_deposit_transaction(row: dict) -> DepositTransaction:
        return DepositTransaction(
            deposit_account_id=row["deposit_account_id"],
            type=row["type"],
            amount=row["amount"],
            id=row["id"],
            created_at=row["created_at"],
            account_id=row["account_id"]
        )

    @staticmethod
    def from_deposit_transaction_to_db_row(deposit_transaction: DepositTransaction) -> dict:
        return {
            "deposit_account_id": deposit_transaction.deposit_account_id,
            "account_id": deposit_transaction.account_id,
            "type": deposit_transaction.type,
            "amount": deposit_transaction.amount
        }


    @staticmethod
    def from_deposit_account_to_db_row(deposit_account: DepositAccount) -> dict:
        return {
            "account_id": deposit_account.account_id,
            "from_account_id": deposit_account.from_account_id,
            "interest_rate": deposit_account.interest_rate,
            "user_id": deposit_account.user_id,
        }