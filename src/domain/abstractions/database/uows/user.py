from abc import abstractmethod

from src.domain.abstractions.database.repositories.users import AbstractUserRepository
from src.domain.abstractions.database.uows.uow import AbstractUnitOfWork


class AbstractUserUnitOfWork(AbstractUnitOfWork):
    @property
    @abstractmethod
    def user_repository(self) -> AbstractUserRepository:
        """Return the user repository."""
        pass
