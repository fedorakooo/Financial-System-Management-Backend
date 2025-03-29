from typing import Optional

from src.application.abstractions.auth.login import AbstractLoginService
from src.application.abstractions.auth.password import AbstractPasswordService
from src.application.abstractions.auth.token import AbstractTokenService
from src.application.abstractions.auth.users import AbstractAuthUserService
from src.infrastructure.exceptions.jwt_exceptions import InvalidLoginError


class LoginService(AbstractLoginService):
    def __init__(
            self,
            auth_user_service: AbstractAuthUserService,
            password_service: AbstractPasswordService,
            token_service: AbstractTokenService
    ):
        self.auth_user_service = auth_user_service
        self.password_service = password_service
        self.token_service = token_service

    async def validate_auth_user(self, phone_number: str, password: str) -> bool:
        hashed_password = await self.auth_user_service.get_user_hashed_password_by_phone_number(phone_number)
        if not hashed_password or not self.password_service.validate_password(password, hashed_password):
            return False
        return True

    async def authenticate_user(self, phone_number: str, password: str) -> Optional[str]:
        user = await self.auth_user_service.get_user_by_phone_number(phone_number)
        is_valid = await self.validate_auth_user(phone_number, password)
        if not is_valid:
            raise InvalidLoginError()

        return self.token_service.create_access_token(user)

