from abc import abstractmethod

from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.deposit import AbstractDepositRepository
from src.domain.abstractions.database.uows.uow import AbstractUnitOfWork


class AbstractDepositUnitOfWork(AbstractUnitOfWork):
    @property
    @abstractmethod
    def deposit_repository(self) -> AbstractDepositRepository:
        """Return the deposit repository."""
        pass

    @property
    @abstractmethod
    def account_repository(self) -> AbstractAccountRepository:
        """Return the account repository."""
        pass
