import bcrypt

from src.domain.abstractions.security.password_handler import AbstractPasswordHandler


class PasswordHandler(AbstractPasswordHandler):
    def hash_password(self, password: str) -> str:
        """Hashes password using bcrypt."""

        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode('utf-8')

    def validate_password(self, password: str, hashed_password: str) -> bool:
        """Checks if the password you entered matches the hash."""

        return bcrypt.checkpw(password.encode(), hashed_password.encode())
