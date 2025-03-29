from src.application.dtos.account import AccountReadDTO
from src.application.dtos.loan import (
    LoanAccountReadDTO,
    LoanReadDTO,
    LoanCreateDTO,
    LoanTransactionCreateDTO,
    LoanTransactionReadDTO
)
from src.domain.entities.loan import Loan, LoanTransaction, LoanAccount
from src.domain.enums.loan import LoanTransactionType


class LoanMapper:
    """Utility class for mapping between Loan-related DTOs and domain entities."""

    @staticmethod
    def map_loan_create_dto_to_loan(dto: LoanCreateDTO) -> Loan:
        return Loan(
            amount=dto.amount,
            term_months=dto.term_months.value,
            interest_rate=dto.interest_rate
        )

    @staticmethod
    def map_loan_transaction_create_dto_to_loan_transaction(
            dto: LoanTransactionCreateDTO,
            loan_transaction_type: LoanTransactionType
    ) -> LoanTransaction:
        return LoanTransaction(
            loan_account_id=dto.loan_account_id,
            type=loan_transaction_type,
            amount=dto.amount
        )

    @staticmethod
    def map_loan_to_loan_read_dto(
            loan: Loan
    ) -> LoanReadDTO:
        return LoanReadDTO(
            amount=loan.amount,
            term_months=loan.term_months,
            interest_rate=loan.interest_rate,
            id=loan.id,
            updated_at=loan.updated_at,
            created_at=loan.created_at
        )

    @staticmethod
    def map_loan_account_to_loan_account_read_dto(
            loan_account: LoanAccount,
            account: AccountReadDTO,
            loan: LoanReadDTO
    ) -> LoanAccountReadDTO:
        return LoanAccountReadDTO(
            id=loan_account.id,
            account_id=loan_account.account_id,
            account=account,
            loan_id=loan_account.loan_id,
            loan=loan,
            user_id=loan_account.user_id
        )

    @staticmethod
    def map_loan_transaction_to_loan_transaction_read_dto(
            loan_transaction: LoanTransaction
    ) -> LoanTransactionReadDTO:
        return LoanTransactionReadDTO(
            loan_account_id=loan_transaction.loan_account_id,
            type=loan_transaction.type,
            amount=loan_transaction.amount,
            id=loan_transaction.id,
            created_at=loan_transaction.created_at
        )
