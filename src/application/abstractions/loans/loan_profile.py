from abc import ABC, abstractmethod

from src.application.dtos.account import AccountCreateDTO
from src.application.dtos.loan import (
    LoanAccountReadDTO,
    LoanCreateDTO,
    LoanReadDTO,
    LoanTransactionCreateDTO,
    LoanTransactionReadDTO
)
from src.application.dtos.user import UserAccessDTO


class AbstractLoanProfileService(ABC):
    """Abstract service for managing user loans."""

    @abstractmethod
    async def get_loan_account_by_account_id(
            self,
            account_id: int,
            requesting_user: UserAccessDTO
    ) -> LoanAccountReadDTO:
        """Fetches the client's loan account by the underlying bank account identifier.

        Raises:
            ForbiddenError: If the requesting user cannot access this resource.
            NotFoundError: If the requested resource does not exist.
        """
        pass

    @abstractmethod
    async def create_loan_request(
            self,
            loan_create_dto: LoanCreateDTO,
            account_create_dto: AccountCreateDTO,
            requesting_user: UserAccessDTO
    ) -> LoanReadDTO:
        """Creates loan terms, a pending bank account, and their borrower association atomically.

        Raises:
            ForbiddenError: If the requesting user cannot create loan requests.
        """
        pass

    @abstractmethod
    async def create_loan_transaction(
            self,
            account_id: int,
            loan_transaction: LoanTransactionCreateDTO,
            requesting_user: UserAccessDTO
    ) -> LoanTransactionReadDTO:
        """Records a payment and debits the client's active loan account atomically.

        Counts PAYMENT records toward the repayment limit and blocks the account
        when the final payment leaves a zero balance.

        Raises:
            ForbiddenError: If the loan belongs to another client.
            NotFoundError: If the loan account does not exist.
            InvalidOperationError: If the argument and DTO identify different loan accounts.
            InactiveAccountError: If the bank account is not active.
            InsufficientFundsError: If its balance cannot cover the payment.
            PaymentExceedsLimitError: If the payment exceeds the remaining repayment limit.
            LoanAccountNonZeroBalanceError: If the final payment leaves unused funds.
        """
        pass

    @abstractmethod
    async def get_loan_transactions_by_loan_account_id(
            self,
            loan_account_id: int,
            requesting_user: UserAccessDTO
    ) -> list[LoanTransactionReadDTO]:
        """Fetches the credit and payment history of the client's loan account.

        Raises:
            ForbiddenError: If the requesting user cannot access this resource.
            NotFoundError: If the requested resource does not exist.
        """
        pass