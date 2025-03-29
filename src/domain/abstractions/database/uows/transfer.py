from abc import abstractmethod

from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.transfer import AbstractTransferRepository
from src.domain.abstractions.database.uows.uow import AbstractUnitOfWork


class AbstractTransferUnitOfWork(AbstractUnitOfWork):
    @property
    @abstractmethod
    def account_repository(self) -> AbstractAccountRepository:
        """Return the account repository."""
        pass

    @property
    @abstractmethod
    def transfer_repository(self) -> AbstractTransferRepository:
        """Return the transfer repository."""
        pass