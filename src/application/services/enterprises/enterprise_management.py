from src.application.abstractions.enterprises.enterprise_management import AbstractEnterpriseManagementService
from src.application.dtos.enterprise import (
    EnterpriseReadDTO, EnterprisePayrollRequestReadDTO,
    EnterpriseCreateDTO, EnterpriseSpecialistCreateDTO, EnterpriseSpecialistReadDTO
)
from src.application.dtos.user import UserAccessDTO, UserCreateDTO
from src.application.mappers.account import AccountMapper
from src.application.mappers.enterprise import EnterpriseMapper
from src.application.mappers.user import UserMapper
from src.domain.abstractions.database.uows.enterprise import AbstractEnterpriseUnitOfWork
from src.domain.abstractions.security.password_handler import AbstractPasswordHandler
from src.application.services.enterprises.access_control import EnterpriseManagementAccessControlService as AccessControl
from src.domain.entities.enterprise import EnterpriseSpecialist
from src.domain.entities.account import Account
from src.domain.exceptions.payment import InvalidOperationError
from src.domain.enums.account import AccountType, AccountStatus
from src.domain.enums.enterprise import EnterprisePayrollRequestStatus
from src.domain.enums.user import UserRole


class EnterpriseManagementService(AbstractEnterpriseManagementService):
    def __init__(
            self,
            uow: AbstractEnterpriseUnitOfWork,
            password_handler: AbstractPasswordHandler
    ):
        self.uow = uow
        self.password_handler = password_handler

    async def get_enterprise_by_id(self, enterprise_id: int, requesting_user: UserAccessDTO) -> EnterpriseReadDTO:
        AccessControl.can_get_enterprises(requesting_user)
        async with self.uow as uow:
            enterprise = await self.uow.enterprise_repository.get_enterprise_by_id(enterprise_id)
            account = await self.uow.account_repository.get_account_by_id(enterprise.account_id)
        account_dto = AccountMapper.map_account_to_account_read_dto(account)
        enterprise_dto = EnterpriseMapper.map_enterprise_to_enterprise_read_dto(enterprise, account_dto)
        return enterprise_dto

    async def get_enterprise_payroll_request_by_id(
            self,
            enterprise_payroll_request_id: int,
            requesting_user: UserAccessDTO
    ) -> EnterprisePayrollRequestReadDTO:
        AccessControl.can_get_enterprise_payroll_requests(requesting_user)
        async with self.uow as uow:
            enterprise_payroll_request = await self.uow.enterprise_repository.get_enterprise_payroll_request_by_id(enterprise_payroll_request_id)
            enterprise = await self.uow.enterprise_repository.get_enterprise_by_id(enterprise_payroll_request.enterprise_id)
            account = await self.uow.account_repository.get_account_by_id(enterprise.account_id)
            specialist = await self.uow.enterprise_repository.get_enterprise_specialist_by_id(enterprise_payroll_request.specialist_id)
            user = await self.uow.user_repository.get_user_by_id(specialist.user_id)
        account_dto = AccountMapper.map_account_to_account_read_dto(account)
        enterprise_dto = EnterpriseMapper.map_enterprise_to_enterprise_read_dto(enterprise, account_dto)
        user_dto = UserMapper.map_user_to_user_read_dto(user)
        specialist_dto = EnterpriseMapper.map_enterprise_specialist_to_enterprise_specialist_read_dto(
            specialist,
            user_dto,
            enterprise_dto
        )
        enterprise_payroll_request_dto = EnterpriseMapper.map_enterprise_payroll_request_to_enterprise_payroll_request_read_dto(
            enterprise_payroll_request,
            enterprise_dto,
            specialist_dto
        )
        return enterprise_payroll_request_dto

    async def approve_enterprise_payroll_request(
            self,
            enterprise_payroll_request_id: int,
            requesting_user: UserAccessDTO
    ) -> EnterprisePayrollRequestReadDTO:
        AccessControl.can_approve_enterprise_payroll_request(requesting_user)
        async with self.uow as uow:
            enterprise_payroll_request = await self.uow.enterprise_repository.get_enterprise_payroll_request_by_id(enterprise_payroll_request_id)
            if enterprise_payroll_request.status is not EnterprisePayrollRequestStatus.ON_CONSIDERATION:
                raise InvalidOperationError("Payroll request must be awaiting approval")
            enterprise = await self.uow.enterprise_repository.get_enterprise_by_id(enterprise_payroll_request.enterprise_id)
            account = await self.uow.account_repository.get_account_by_id(enterprise.account_id)
            accounts_id = []
            for user_passport_number in enterprise_payroll_request.passport_numbers:
                # raise not found error if no user
                user = await self.uow.user_repository.get_user_by_passport_number(user_passport_number)

                salary_account = await self.uow.account_repository.create_account(
                    Account(
                        user_id=user.id,
                        bank_id=enterprise.bank_id,
                        type=AccountType.SALARY,
                        status=AccountStatus.ACTIVE
                    )
                )
                accounts_id.append(salary_account.id)
            await uow.enterprise_repository.update_payroll_request_accounts(enterprise_payroll_request.id, accounts_id)
            specialist = await self.uow.enterprise_repository.get_enterprise_specialist_by_id(enterprise_payroll_request.specialist_id)
            user = await self.uow.user_repository.get_user_by_id(specialist.user_id)
            enterprise_payroll_request = await self.uow.enterprise_repository.update_payroll_request_status_by_id(
                enterprise_payroll_request.id,
                EnterprisePayrollRequestStatus.APPROVED
            )
        user_dto = UserMapper.map_user_to_user_read_dto(user)
        account_dto = AccountMapper.map_account_to_account_read_dto(account)
        enterprise_dto = EnterpriseMapper.map_enterprise_to_enterprise_read_dto(enterprise, account_dto)
        specialist_dto = EnterpriseMapper.map_enterprise_specialist_to_enterprise_specialist_read_dto(specialist, user_dto, enterprise_dto)
        enterprise_payroll_request_dto = EnterpriseMapper.map_enterprise_payroll_request_to_enterprise_payroll_request_read_dto(
            enterprise_payroll_request,
            enterprise_dto,
            specialist_dto
        )
        return enterprise_payroll_request_dto

    async def create_enterprise(
            self,
            enterprise_create_dto: EnterpriseCreateDTO,
            requesting_user: UserAccessDTO
    ) -> EnterpriseReadDTO:
        AccessControl.can_create_enterprise(requesting_user)
        async with self.uow as uow:
            created_account = await self.uow.account_repository.create_account(
                Account(
                    user_id=requesting_user.id,
                    bank_id=enterprise_create_dto.bank_id,
                    type=AccountType.ENTERPRISE,
                    status=AccountStatus.ACTIVE
                )
            )
            enterprise_create = EnterpriseMapper.map_enterprise_create_dto_to_enterprise(
                enterprise_create_dto,
                created_account.id
            )
            created_enterprise = await self.uow.enterprise_repository.create_enterprise(enterprise_create)
        created_account_dto = AccountMapper.map_account_to_account_read_dto(created_account)
        created_enterprise_dto = EnterpriseMapper.map_enterprise_to_enterprise_read_dto(
            created_enterprise,
            created_account_dto
        )
        return created_enterprise_dto

    async def create_enterprise_specialist(
            self,
            enterprise_specialist_create_dto: EnterpriseSpecialistCreateDTO,
            requesting_user: UserAccessDTO,
            user_create_dto: UserCreateDTO = None
    ) -> EnterpriseSpecialistReadDTO:
        AccessControl.can_create_enterprise_specialist(requesting_user)
        async with self.uow as uow:
            await uow.enterprise_repository.get_enterprise_by_id(enterprise_specialist_create_dto.enterprise_id)
            if user_create_dto is None:
                user = await uow.user_repository.get_user_by_id(enterprise_specialist_create_dto.user_id)
                if user.role is not UserRole.SPECIALIST:
                    raise InvalidOperationError("User must have the specialist role")
            else:
                hashed_password = self.password_handler.hash_password(user_create_dto.password)
                user_create = UserMapper.map_user_create_dto_to_user(
                    user_create_dto,
                    UserRole.SPECIALIST,
                    hashed_password
                )
                user = await uow.user_repository.create_user(user_create)
            enterprise_specialist_create = EnterpriseSpecialist(
                user_id=user.id,
                enterprise_id=enterprise_specialist_create_dto.enterprise_id
            )
            created_enterprise_specialist = await self.uow.enterprise_repository.create_enterprise_specialist(enterprise_specialist_create)
            user = await self.uow.user_repository.get_user_by_id(created_enterprise_specialist.user_id)
            enterprise = await self.uow.enterprise_repository.get_enterprise_by_id(created_enterprise_specialist.enterprise_id)
            account = await self.uow.account_repository.get_account_by_id(enterprise.account_id)
        account_dto = AccountMapper.map_account_to_account_read_dto(account)
        user_dto = UserMapper.map_user_to_user_read_dto(user)
        enterprise_dto = EnterpriseMapper.map_enterprise_to_enterprise_read_dto(enterprise, account_dto)
        return EnterpriseMapper.map_enterprise_specialist_to_enterprise_specialist_read_dto(
            created_enterprise_specialist,
            user_dto,
            enterprise_dto
        )