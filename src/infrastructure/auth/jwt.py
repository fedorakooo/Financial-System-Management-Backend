import jwt
from datetime import timedelta, datetime
from typing import Optional, Union

from src.domain.abstractions.auth.jwt_handler import AbstractJWTHandler
from src.infrastructure.exceptions.jwt_exceptions import (
    InvalidTokenError,
    ExpiredTokenError,
    TokenDecodeError,
    TokenCreationError
)


class JWTHandler(AbstractJWTHandler):
    def __init__(
            self,
            private_key: str,
            public_key: str,
            algorithm: str,
            expire_minutes: int
    ):
        self.private_key = private_key
        self.public_key = public_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def encode(
            self,
            payload: dict,
            expire_timedelta: Optional[timedelta] = None
    ) -> str:
        to_encode = payload.copy()
        now = datetime.utcnow()

        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=self.expire_minutes)

        to_encode.update(
            exp=expire,
            iat=now
        )
        try:
            encoded = jwt.encode(
                to_encode,
                self.private_key,
                algorithm=self.algorithm
            )
        except Exception:
            raise TokenCreationError("Failed to create token")

        return encoded

    def decode(
            self,
            token: Union[str, bytes]
    ) -> dict:
        try:
            decoded = jwt.decode(
                token,
                self.public_key,
                algorithms=[self.algorithm]
            )
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenError("Token has expired")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("The token is invalid.")
        except Exception:
            raise TokenDecodeError("Failed to decode token")

        return decoded
