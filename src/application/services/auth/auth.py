from src.application.abstractions.auth.auth import AbstractAuthService
from src.application.abstractions.auth.payload import AbstractPayloadExtractorService
from src.application.abstractions.auth.token import AbstractTokenService
from src.application.dtos.user import UserAccessDTO


class AuthService(AbstractAuthService):
    def __init__(
            self,
            token_service: AbstractTokenService,
            payload_extractor_service: AbstractPayloadExtractorService
    ):
        self.token_service = token_service
        self.payload_extractor_service = payload_extractor_service

    def get_current_active_auth_user(self, token: str) -> UserAccessDTO:
        payload = self.token_service.decode_token(token)
        user_access_dto = self.payload_extractor_service.extract_user_from_payload(payload)
        return user_access_dto
