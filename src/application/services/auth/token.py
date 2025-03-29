from datetime import datetime, timedelta
from typing import Any

from src.config import settings
from src.domain.abstractions.auth.jwt_handler import AbstractJWTHandler
from src.application.abstractions.auth.token import AbstractTokenService
from src.application.dtos.user import UserReadDTO


class TokenService(AbstractTokenService):
    def __init__(self, token_handler: AbstractJWTHandler):
        self.token_handler = token_handler

    def create_access_token(self, user: UserReadDTO) -> str:
        payload = {
            "id": user.id,
            "role": user.role.value,
            "is_active": user.is_active,
            "exp": datetime.utcnow() + timedelta(minutes=settings.auth_jwt.expire_minutes)
        }
        access_token = self.token_handler.encode(payload=payload)
        return access_token

    def decode_token(self, token: str) -> dict[str, Any]:
        return self.token_handler.decode(token)
