from src.application.mappers.user import UserMapper
from src.domain.abstractions.database.repositories.users import AbstractUserRepository
from src.application.dtos.user import UserReadDTO
from src.domain.abstractions.database.uows.user import AbstractUserUnitOfWork


class AuthUserService:
    def __init__(self, uow: AbstractUserUnitOfWork):
        self.uow = uow

    async def get_user_by_phone_number(self, phone_number: str) -> UserReadDTO:
        async with self.uow as uow:
            user = await uow.user_repository.get_user_by_phone_number(phone_number)
        user_dto = UserMapper.map_user_to_user_read_dto(user)
        return user_dto

    async def get_user_hashed_password_by_phone_number(self, phone_number: str) -> str:
        async with self.uow as uow:
            hashed_password: str = await uow.user_repository.get_user_hashed_password_by_phone_number(phone_number)
        return hashed_password
