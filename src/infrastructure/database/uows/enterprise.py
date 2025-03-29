from typing import Optional

from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.factories.repository import AbstractRepositoryFactory
from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.enterprise import AbstractEnterpriseRepository
from src.domain.abstractions.database.repositories.users import AbstractUserRepository
from src.domain.abstractions.database.uows.enterprise import AbstractEnterpriseUnitOfWork


class EnterpriseUnitOfWork(AbstractEnterpriseUnitOfWork):
    def __init__(self, db_connection: AbstractDatabaseConnection, repository_factory: AbstractRepositoryFactory):
        self.db_connection = db_connection
        self.repository_factory = repository_factory
        self._enterprise_repository: Optional[AbstractEnterpriseRepository] = None
        self._account_repository: Optional[AbstractAccountRepository] = None
        self._user_repository: Optional[AbstractUserRepository] = None
        self._transaction = None

    async def __aenter__(self):
        """Set up the context manager by establishing a connection and starting a transaction."""
        await self.db_connection.connect()
        self._transaction = self.db_connection.connection.transaction()
        await self._transaction.start()

        self._enterprise_repository = self.repository_factory.create_enterprise_repository(self.db_connection.connection)
        self._account_repository = self.repository_factory.create_account_repository(self.db_connection.connection)
        self._user_repository = self.repository_factory.create_user_repository(self.db_connection.connection)

        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Clean up by committing or rolling back the transaction and closing the connection."""
        if self._transaction:
            if exc_type is None:
                await self._transaction.commit()
            else:
                await self._transaction.rollback()
            self._transaction = None
        await self.db_connection.close()

    @property
    def account_repository(self) -> AbstractAccountRepository:
        """Return the account repository."""
        if self._account_repository is None:
            raise RuntimeError("Account repository is not initialized. Use the context manager.")
        return self._account_repository

    @property
    def enterprise_repository(self) -> AbstractEnterpriseRepository:
        """Return the deposit repository."""
        if self._enterprise_repository is None:
            raise RuntimeError("Deposit repository is not initialized. Use the context manager.")
        return self._enterprise_repository

    @property
    def user_repository(self) -> AbstractUserRepository:
        """Return the deposit repository."""
        if self._user_repository is None:
            raise RuntimeError("User repository is not initialized. Use the context manager.")
        return self._user_repository