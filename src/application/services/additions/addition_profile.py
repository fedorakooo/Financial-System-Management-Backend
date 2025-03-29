from src.application.abstractions.additions.addition_profile import AbstractAdditionProfileService
from src.application.dtos.addition import AdditionReadDTO, AdditionCreateDTO
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.addition import AdditionMapper
from src.application.services.additions.access_control import AdditionProfileAccessControlService as AccessControl
from src.domain.abstractions.database.uows.addition import AbstractAdditionUnitOfWork
from src.domain.enums.account import AccountStatus, AccountType
from src.domain.exceptions.account import InactiveAccountError, InvalidAccountTypeError


class AdditionProfileService(AbstractAdditionProfileService):
    def __init__(self, uow: AbstractAdditionUnitOfWork):
        self.uow = uow

    async def get_additions_by_account_id(
            self,
            account_id: int,
            requesting_user: UserAccessDTO
    ) -> list[AdditionReadDTO]:
        async with self.uow as uow:
            account = await uow.account_repository.get_account_by_id(account_id)
            AccessControl.can_get_additions(account.user_id, requesting_user)

            additions = await uow.addition_repository.get_additions_by_account_id(account_id)

        additions_dto = [AdditionMapper.map_addition_to_addition_read_dto(addition) for addition in additions]
        return additions_dto

    async def create_addition(
            self,
            account_id: int,
            addition_create_dto: AdditionCreateDTO,
            requesting_user: UserAccessDTO
    ) -> AdditionReadDTO:
        async with self.uow as uow:
            account = await uow.account_repository.get_account_by_id(account_id)
            AccessControl.can_create_addition(account.user_id, requesting_user)
            if account.status is not AccountStatus.ACTIVE:
                raise InactiveAccountError(account.status)
            if account.type is not AccountType.SETTLEMENT:
                raise InvalidAccountTypeError(account.type, AccountType.SETTLEMENT)
            new_account_balance = account.balance + addition_create_dto.amount
            addition_create = AdditionMapper.map_addition_create_dto_to_addition(addition_create_dto, account_id)
            created_addition = await uow.addition_repository.create_addition(addition_create)
            await uow.account_repository.update_account_balance(account_id, new_account_balance)

        created_addition_dto = AdditionMapper.map_addition_to_addition_read_dto(created_addition)
        return created_addition_dto
