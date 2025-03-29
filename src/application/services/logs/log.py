from src.domain.abstractions.logger.logger import AbstractLogger
from src.application.abstractions.logs.log import AbstractLogService


class LogService(AbstractLogService):
    def __init__(self, logger: AbstractLogger):
        self.logger = logger

    def info(self, message: str) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)
