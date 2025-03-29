from abc import abstractmethod

from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.withdrawals import AbstractWithdrawalRepository
from src.domain.abstractions.database.uows.uow import AbstractUnitOfWork


class AbstractWithdrawalUnitOfWork(AbstractUnitOfWork):
    @property
    @abstractmethod
    def account_repository(self) -> AbstractAccountRepository:
        """Return the account repository."""
        pass

    @property
    @abstractmethod
    def withdrawal_repository(self) -> AbstractWithdrawalRepository:
        """Return the withdrawal repository."""
        pass