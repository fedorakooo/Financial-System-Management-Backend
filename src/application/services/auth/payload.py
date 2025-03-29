from src.application.abstractions.auth.payload import AbstractPayloadExtractorService
from src.application.dtos.user import UserAccessDTO, UserAuthDTO
from src.domain.abstractions.auth.jwt_handler import AbstractJWTHandler
from src.domain.exceptions.forbidden import UserInactiveError


class PayloadExtractorService(AbstractPayloadExtractorService):
    def __init__(self, token_handler: AbstractJWTHandler):
        self.token_handler = token_handler

    def extract_user_from_payload(self, payload: dict) -> UserAuthDTO:
        if not payload.get("is_active"):
            raise UserInactiveError()

        return UserAccessDTO(
            id=payload.get("id"),
            role=payload.get("role")
        )
