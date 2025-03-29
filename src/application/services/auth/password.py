from src.application.abstractions.auth.password import AbstractPasswordService
from src.domain.abstractions.security.password_handler import AbstractPasswordHandler


class PasswordService(AbstractPasswordService):
    def __init__(self, password_handler: AbstractPasswordHandler):
        self.password_handler = password_handler

    def validate_password(self, password: str, hashed_password: str) -> bool:
        return self.password_handler.validate_password(password, hashed_password)
