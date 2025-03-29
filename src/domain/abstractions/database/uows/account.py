from abc import abstractmethod

from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.uows.uow import AbstractUnitOfWork


class AbstractAccountUnitOfWork(AbstractUnitOfWork):
    @property
    @abstractmethod
    def account_repository(self) -> AbstractAccountRepository:
        """Return the account repository."""
        pass
