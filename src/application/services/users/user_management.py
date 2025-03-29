from src.application.abstractions.users.user_management import AbstractUserManagementService
from src.application.dtos.user import UserAccessDTO, UserReadDTO, UserUpdateDTO
from src.application.mappers.user import UserMapper
from src.application.services.users.access_control import UserManagementAccessControlService as AccessControl
from src.domain.abstractions.database.uows.user import AbstractUserUnitOfWork


class UserManagementService(AbstractUserManagementService):
    def __init__(self, uow: AbstractUserUnitOfWork):
        self.uow = uow

    async def get_user_by_id(self, user_id: int, requesting_user: UserAccessDTO) -> UserReadDTO:
        AccessControl.can_get_users(requesting_user)
        async with self.uow as uow:
            user = await self.uow.user_repository.get_user_by_id(user_id)
        user_dto = UserMapper.map_user_to_user_read_dto(user)
        return user_dto

    async def get_all_users(self, requesting_user: UserAccessDTO) -> list[UserReadDTO]:
        AccessControl.can_get_users(requesting_user)
        async with self.uow as uow:
            users = await uow.user_repository.get_users()
        users_dto = [UserMapper.map_user_to_user_read_dto(user) for user in users]
        return users_dto

    async def update_user_by_id(
            self,
            user_id: int,
            user_update_dto: UserUpdateDTO,
            requesting_user: UserAccessDTO
    ) -> UserReadDTO:
        AccessControl.can_update_user(requesting_user)

        async with self.uow as uow:
            current_user = await uow.user_repository.get_user_by_id(user_id)
            user_update = UserMapper.map_user_update_dto_to_user(user_update_dto, current_user)

            updated_user = await uow.user_repository.update_user_by_id(user_id, user_update)

        updated_user_dto = UserMapper.map_user_to_user_read_dto(updated_user)
        return updated_user_dto

    async def delete_user_by_id(self, user_id: int, requesting_user: UserAccessDTO) -> None:
        AccessControl.can_delete_user(requesting_user)

        async with self.uow as uow:
            await uow.user_repository.delete_user_by_id(user_id)
