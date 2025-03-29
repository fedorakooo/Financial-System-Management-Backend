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
    ) -> list[LoanAccountReadDTO]:
        pass

    @abstractmethod
    async def create_loan_request(
            self,
            loan_create_dto: LoanCreateDTO,
            account_create_dto: AccountCreateDTO,
            requesting_user: UserAccessDTO
    ) -> LoanReadDTO:
        pass

    @abstractmethod
    async def create_loan_transaction(
            self,
            account_id: int,
            loan_transaction: LoanTransactionCreateDTO,
            requesting_user: UserAccessDTO
    ) -> LoanTransactionReadDTO:
        pass

    @abstractmethod
    async def get_loan_transactions_by_loan_account_id(
            self,
            loan_account_id: int,
            requesting_user: UserAccessDTO
    ) -> list[LoanTransactionReadDTO]:
        pass