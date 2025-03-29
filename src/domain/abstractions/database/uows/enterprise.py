from abc import abstractmethod

from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.enterprise import AbstractEnterpriseRepository
from src.domain.abstractions.database.repositories.users import AbstractUserRepository
from src.domain.abstractions.database.uows.uow import AbstractUnitOfWork


class AbstractEnterpriseUnitOfWork(AbstractUnitOfWork):
    @property
    @abstractmethod
    def enterprise_repository(self) -> AbstractEnterpriseRepository:
        """Return the enterprise repository."""
        pass

    @property
    @abstractmethod
    def account_repository(self) -> AbstractAccountRepository:
        """Return the account repository."""
        pass

    @property
    @abstractmethod
    def user_repository(self) -> AbstractUserRepository:
        """Return the user repository."""
        pass
