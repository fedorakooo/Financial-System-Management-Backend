class JWTError(Exception):
    """Base exception for JWT errors."""
    pass


class InvalidTokenError(JWTError):
    """Exception raised for invalid JWT tokens."""
    pass


class ExpiredTokenError(JWTError):
    """Exception raised when a JWT token has expired."""

    DEFAULT_MESSAGE = "Token has expired."

    def __init__(self, message: str = DEFAULT_MESSAGE):
        super().__init__(message)


class TokenDecodeError(JWTError):
    """Exception raised when decoding a JWT token fails."""
    pass


class TokenCreationError(JWTError):
    """Exception raised when creating a JWT token fails."""
    pass


class InvalidLoginError(Exception):
    """Exception raised for invalid login attempts (wrong phone number or password)."""

    def __init__(self, message: str = "Invalid phone number or password"):
        super().__init__(message)

