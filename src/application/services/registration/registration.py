from src.application.mappers.user import UserMapper
from src.domain.abstractions.database.uows.user import AbstractUserUnitOfWork
from src.domain.abstractions.security.password_handler import AbstractPasswordHandler
from src.application.abstractions.registration.registration import AbstractUserRegistrationService
from src.application.dtos.user import UserCreateDTO, UserReadDTO
from src.domain.enums.user import UserRole


class UserRegistrationService(AbstractUserRegistrationService):
    def __init__(
            self,
            uow: AbstractUserUnitOfWork,
            password_handler: AbstractPasswordHandler
    ):
        self.uow = uow
        self.password_handler = password_handler

    async def _create_user(self, user_create_dto: UserCreateDTO, role: UserRole) -> UserReadDTO:
        """General method to create a user for a specific role."""

        hashed_password = self.password_handler.hash_password(user_create_dto.password)

        user_create = UserMapper.map_user_create_dto_to_user(
            user_create_dto,
            role,
            hashed_password
        )

        async with self.uow as uow:
            new_user = await self.uow.user_repository.create_user(user_create)

        new_user_dto = UserMapper.map_user_to_user_read_dto(new_user)
        return new_user_dto

    async def create_user_client(self, user_create_dto: UserCreateDTO) -> UserReadDTO:
        return await self._create_user(user_create_dto, UserRole.CLIENT)

    async def create_user_operator(self, user_create_dto: UserCreateDTO) -> UserReadDTO:
        return await self._create_user(user_create_dto, UserRole.OPERATOR)

    async def create_user_manager(self, user_create_dto: UserCreateDTO) -> UserReadDTO:
        return await self._create_user(user_create_dto, UserRole.MANAGER)

    async def create_user_admin(self, user_create_dto: UserCreateDTO) -> UserReadDTO:
        return await self._create_user(user_create_dto, UserRole.ADMINISTRATOR)

    async def create_user_specialist(self, user_create_dto: UserCreateDTO) -> UserReadDTO:
        return await self._create_user(user_create_dto, UserRole.SPECIALIST)