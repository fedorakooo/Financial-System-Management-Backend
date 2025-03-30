from abc import ABC, abstractmethod

from src.domain.entities.loan import Loan, LoanTransaction, LoanAccount


class AbstractLoanRepository(ABC):
    """Abstract class for a loan repository."""

    @abstractmethod
    async def get_loan_by_id(self, loan_id: int) -> Loan:
        """Fetches a loan by its unique identifier.

        Raises:
            NotFoundError: If the loan with the specified id is not found.
        """

    @abstractmethod
    async def get_loan_account_by_id(self, loan_account_id: int) -> LoanAccount:
        """Fetches a loan account by its unique identifier.

        Raises:
            NotFoundError: If the loan account with the specified id is not found.
        """
        pass

    @abstractmethod
    async def get_loan_account_by_account_id(self, account_id: int) -> LoanAccount:
        """Fetches a loan account by the identifier of its underlying bank account.

        Raises:
            NotFoundError: If the linked loan account does not exist.
        """
        pass

    @abstractmethod
    async def get_loan_accounts_by_user_id(self, user_id: int) -> list[LoanAccount]:
        """Fetches loan accounts associated with a specific user."""
        pass

    @abstractmethod
    async def get_loan_transactions_by_loan_account_id(self, loan_account_id: int) -> list[LoanTransaction]:
        """Fetches loan transactions associated with a specific loan account."""
        pass

    @abstractmethod
    async def create_loan(self, loan: Loan) -> Loan:
        """Creates loan terms and returns the persisted loan with its generated identifier."""
        pass

    @abstractmethod
    async def create_loan_transaction(self, loan_transaction: LoanTransaction) -> LoanTransaction:
        """Records a loan credit or payment within the current transaction."""
        pass

    @abstractmethod
    async def create_loan_account(self, loan_account_create: LoanAccount):
        """Links a bank account, loan, and borrower and returns the persisted loan account."""
        pass
