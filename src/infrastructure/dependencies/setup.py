from src.infrastructure.dependencies.app import Application
from src.config import settings


def setup_container() -> Application:
    container = Application()

    container.config.gateways.url.from_value(settings.db.url)
    container.config.core.public_key.from_value(settings.auth_jwt.public_key)
    container.config.core.private_key.from_value(settings.auth_jwt.private_key)
    container.config.core.logger_config.from_value(settings.logger.log_config)

    return container
