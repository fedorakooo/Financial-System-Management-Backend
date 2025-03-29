from abc import abstractmethod

from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.additions import AbstractAdditionRepository
from src.domain.abstractions.database.uows.uow import AbstractUnitOfWork


class AbstractAdditionUnitOfWork(AbstractUnitOfWork):
    @property
    @abstractmethod
    def account_repository(self) -> AbstractAccountRepository:
        """Return the account repository."""
        pass

    @property
    @abstractmethod
    def addition_repository(self) -> AbstractAdditionRepository:
        """Return the addition repository."""
        pass
