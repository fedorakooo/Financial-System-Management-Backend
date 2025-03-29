from src.domain.entities.loan import Loan, LoanTransaction, LoanAccount
from src.domain.enums.loan import LoanTermMonths, LoanTransactionType


class LoanDatabaseMapper:
    """Utility class for mapping between database rows and Loans entities."""

    @staticmethod
    def from_db_row_to_loan(row: dict) -> Loan:
        return Loan(
            amount=row["amount"],
            term_months=LoanTermMonths(row["term_months"]),
            interest_rate=row["interest_rate"],
            id=row["id"],
            updated_at=row["updated_at"],
            created_at=row["created_at"]
        )

    @staticmethod
    def from_loan_to_db_row(loan: Loan) -> dict:
        return {
            "interest_rate": loan.interest_rate,
            "amount": loan.amount,
            "term_months": loan.term_months,
        }

    @staticmethod
    def from_db_row_to_loan_transaction(row: dict) -> LoanTransaction:
        return LoanTransaction(
            loan_account_id=row["loan_account_id"],
            id=row["id"],
            type=LoanTransactionType(row["type"]),
            amount=row["amount"],
            created_at=row["created_at"]
        )

    @staticmethod
    def from_loan_transaction_to_db_row(loan: LoanTransaction) -> dict:
        return {
            "type": loan.type.value,
            "loan_account_id": loan.loan_account_id,
            "amount": loan.amount,
        }

    @staticmethod
    def from_db_row_to_loan_account(row: dict) -> LoanAccount:
        return LoanAccount(
            account_id=row["account_id"],
            loan_id=row["loan_id"],
            id=row["id"],
            user_id=row["user_id"]
        )

    @staticmethod
    def from_loan_account_to_db_row(loan: LoanAccount) -> dict:
        return {
            "account_id": loan.account_id,
            "loan_id": loan.loan_id,
            "user_id": loan.user_id,
        }
