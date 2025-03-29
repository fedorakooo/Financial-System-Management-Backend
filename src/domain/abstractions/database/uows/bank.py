from abc import abstractmethod

from src.domain.abstractions.database.repositories.banks import AbstractBankRepository
from src.domain.abstractions.database.uows.uow import AbstractUnitOfWork


class AbstractBankUnitOfWork(AbstractUnitOfWork):
    @property
    @abstractmethod
    def bank_repository(self) -> AbstractBankRepository:
        """Return the account repository."""
        pass
