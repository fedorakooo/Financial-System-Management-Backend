import logging
from src.domain.abstractions.logger.logger import AbstractLogger


class Logger(AbstractLogger):
    def __init__(self, logger_config: dict):
        format_str = logger_config['formatters']['formatter']['format']
        log_level = logger_config['root']['level']

        formatter = logging.Formatter(format_str)

        self.logger = logging.getLogger("application_log")
        self.logger.setLevel(log_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logger_config['handlers']['console']['level'])
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(logger_config['handlers']['file']['filename'])
        file_handler.setLevel(logger_config['handlers']['file']['level'])
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)
