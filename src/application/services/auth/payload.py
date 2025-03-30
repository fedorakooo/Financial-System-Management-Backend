from src.application.abstractions.auth.payload import AbstractPayloadExtractorService
from src.application.dtos.user import UserAccessDTO
from src.domain.abstractions.auth.jwt_handler import AbstractJWTHandler
from src.domain.enums.user import UserRole
from src.infrastructure.exceptions.jwt_exceptions import InvalidTokenError


class PayloadExtractorService(AbstractPayloadExtractorService):
    def __init__(self, token_handler: AbstractJWTHandler):
        self.token_handler = token_handler

    def extract_user_from_payload(self, payload: dict) -> UserAccessDTO:
        if type(payload.get("id")) is not int or payload["id"] <= 0:
            raise InvalidTokenError("Invalid token identity")
        try:
            UserRole(payload.get("role"))
        except (ValueError, TypeError):
            raise InvalidTokenError("Invalid token role")

        return UserAccessDTO(
            id=payload.get("id"),
            role=payload.get("role")
        )
