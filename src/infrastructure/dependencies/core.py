from dependency_injector import containers, providers

from src.infrastructure.auth.jwt import JWTHandler
from src.infrastructure.logger.logger import Logger
from src.infrastructure.security.password_handler import PasswordHandler


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()

    logger = providers.Singleton(
        Logger,
        logger_config=config.logger_config
    )

    password_handler = providers.Singleton(
        PasswordHandler,
    )

    token_handler = providers.Singleton(
        JWTHandler,
        private_key=config.private_key,
        public_key=config.public_key,
        algorithm=config.jwt_handler.algorithm,
        expire_minutes=config.jwt_handler.expire_minutes,
    )
