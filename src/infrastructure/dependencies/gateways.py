from dependency_injector import containers, providers

from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.database.database_initializer import DatabaseInitializer
from src.infrastructure.database.factories.repository_factory import RepositoryFactory


class Gateways(containers.DeclarativeContainer):
    config = providers.Configuration()

    core = providers.DependenciesContainer()

    database_connection = providers.Singleton(
        DatabaseConnection,
        logger=core.logger,
        dsn=config.url
    )

    database_initializer = providers.Factory(
        DatabaseInitializer,
        db_connection=database_connection,
    )

    repository_factory = providers.Factory(
        RepositoryFactory,
    )
