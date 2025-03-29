from abc import abstractmethod

from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.loans import AbstractLoanRepository
from src.domain.abstractions.database.uows.uow import AbstractUnitOfWork


class AbstractLoanUnitOfWork(AbstractUnitOfWork):
    @property
    @abstractmethod
    def loan_repository(self) -> AbstractLoanRepository:
        """Return the loan repository."""
        pass

    @property
    @abstractmethod
    def account_repository(self) -> AbstractAccountRepository:
        """Return the account repository."""
        pass


