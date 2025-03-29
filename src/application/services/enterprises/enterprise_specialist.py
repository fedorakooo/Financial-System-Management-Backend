from src.application.abstractions.enterprises.enterprise_specialist import AbstractEnterpriseSpecialistService
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.account import AccountMapper
from src.application.mappers.enterprise import EnterpriseMapper
from src.application.mappers.user import UserMapper
from src.domain.abstractions.database.uows.enterprise import AbstractEnterpriseUnitOfWork
from src.application.services.enterprises.access_control import EnterpriseSpecialistAccessControlService as AccessControl
from src.domain.exceptions.account import InsufficientFundsError
from src.application.dtos.enterprise import (
    EnterpriseSpecialistReadDTO,
    EnterprisePayrollRequestReadDTO,
    EnterprisePayrollTransactionReadDTO,
    EnterprisePayrollRequestCreateDTO
)


class EnterpriseSpecialistService(AbstractEnterpriseSpecialistService):
    def __init__(self, uow: AbstractEnterpriseUnitOfWork):
        self.uow = uow

    async def get_enterprise_specialist_profile(self, requesting_user: UserAccessDTO) -> EnterpriseSpecialistReadDTO:
        AccessControl.can_get_enterprise_specialist_profile(requesting_user)
        async with self.uow as uow:
            enterprise_specialist = await self.uow.enterprise_repository.get_enterprise_specialist_by_user_id(
                requesting_user.id
            )
            user = await self.uow.user_repository.get_user_by_id(enterprise_specialist.user_id)
            enterprise = await self.uow.enterprise_repository.get_enterprise_by_id(enterprise_specialist.enterprise_id)
            enterprise_account = await self.uow.account_repository.get_account_by_id(enterprise.account_id)
        account_dto = AccountMapper.map_account_to_account_read_dto(enterprise_account)
        enterprise_dto = EnterpriseMapper.map_enterprise_to_enterprise_read_dto(enterprise, account_dto)
        user_dto = UserMapper.map_user_to_user_read_dto(user)
        enterprise_specialist_dto = EnterpriseMapper.map_enterprise_specialist_to_enterprise_specialist_read_dto(
            specialist=enterprise_specialist,
            user_read_dto=user_dto,
            enterprise_read_dto=enterprise_dto
        )
        return enterprise_specialist_dto

    async def get_enterprise_payroll_request_by_id(
            self,
            payroll_request_id: int,
            specialist_id: int,
            requesting_user: UserAccessDTO
    ) -> list[EnterprisePayrollRequestReadDTO]:
        async with self.uow as uow:
            enterprise_payroll_request = await self.uow.enterprise_repository.get_enterprise_payroll_request_by_id(payroll_request_id)
            enterprise_specialist = await self.uow.enterprise_repository.get_enterprise_specialist_by_id(enterprise_payroll_request.specialist_id)
            AccessControl.can_get_enterprise_payroll_requests(enterprise_specialist.user_id, requesting_user)
            enterprise = await self.uow.enterprise_repository.get_enterprise_by_id(enterprise_payroll_request.enterprise_id)
            account = await self.uow.account_repository.get_account_by_id(enterprise.account_id)
            user = await self.uow.user_repository.get_user_by_id(enterprise_specialist.user_id)
        user_dto = UserMapper.map_user_to_user_read_dto(user)
        account_dto = AccountMapper.map_account_to_account_read_dto(account)
        enterprise_read_dto = EnterpriseMapper.map_enterprise_to_enterprise_read_dto(enterprise, account_dto)
        enterprise_specialist_dto = EnterpriseMapper.map_enterprise_specialist_to_enterprise_specialist_read_dto(enterprise_specialist, user_dto)
        enterprise_payroll_request_dto = EnterpriseMapper.map_enterprise_payroll_request_to_enterprise_payroll_request_read_dto(
            request=enterprise_payroll_request,
            enterprise_read_dto=enterprise_read_dto,
            specialist_read_dto=enterprise_specialist_dto
        )
        return enterprise_payroll_request_dto

    async def get_payroll_transactions_by_enterprise_payroll_request_id(
            self,
            enterprise_payroll_request_id: int,
            requesting_user: UserAccessDTO
    ) -> list[EnterprisePayrollTransactionReadDTO]:
        async with self.uow as uow:
            enterprise_payroll_request = await self.uow.enterprise_repository.get_enterprise_payroll_request_by_id(enterprise_payroll_request_id)
            enterprise_specialist = await self.uow.enterprise_repository.get_enterprise_specialist_by_id(enterprise_payroll_request.specialist_id)
            AccessControl.can_get_enterprise_payroll_requests(enterprise_specialist.user_id, requesting_user)
            payroll_transactions = await self.uow.enterprise_repository.get_enterprise_payroll_request_by_id(enterprise_payroll_request_id)
        payroll_transactions_dto = [EnterpriseMapper.map_enterprise_payroll_transaction_to_enterprise_payroll_transaction_read_dto(payroll_transaction) for payroll_transaction in payroll_transactions]
        return payroll_transactions_dto


    async def create_enterprise_payroll_request(
            self,
            enterprise_payroll_request_dto: EnterprisePayrollRequestCreateDTO,
            requesting_user: UserAccessDTO
    ) -> EnterprisePayrollRequestReadDTO:
        AccessControl.can_create_enterprise_payroll_request(requesting_user)
        enterprise_payroll_request = EnterpriseMapper.map_enterprise_payroll_request_create_dto_to_enterprise_payroll_request(enterprise_payroll_request_dto)
        async with self.uow as uow:
            created_enterprise_payroll_request = await self.uow.enterprise_repository.create_payroll_request(enterprise_payroll_request)
            specialist = await self.uow.enterprise_repository.get_enterprise_specialist_by_id(created_enterprise_payroll_request.specialist_id)
            enterprise = await self.uow.enterprise_repository.get_enterprise_by_id(created_enterprise_payroll_request.enterprise_id)
            account = await self.uow.account_repository.get_account_by_id(enterprise.account_id)
            user = await self.uow.user_repository.get_user_by_id(specialist.user_id)
        account_dto = AccountMapper.map_account_to_account_read_dto(account)
        user_dto = UserMapper.map_user_to_user_read_dto(user)
        enterprise_dto = EnterpriseMapper.map_enterprise_to_enterprise_read_dto(enterprise, account_dto)
        specialist_dto = EnterpriseMapper.map_enterprise_specialist_to_enterprise_specialist_read_dto(
            specialist=specialist,
            user_read_dto=user_dto,
            enterprise_read_dto=enterprise_dto
        )
        created_enterprise_payroll_request_dto = EnterpriseMapper.map_enterprise_payroll_request_to_enterprise_payroll_request_read_dto(
            created_enterprise_payroll_request,
            enterprise_read_dto=enterprise_dto,
            specialist_read_dto=specialist_dto
        )
        return created_enterprise_payroll_request_dto

    async def make_enterprise_payroll_request(
            self,
            enterprise_payroll_request_id: int,
            requesting_user: UserAccessDTO
    ) -> None:
        async with self.uow as uow:
            enterprise_payroll_request = await self.uow.enterprise_repository.get_enterprise_payroll_request_by_id(enterprise_payroll_request_id)
            specialist = await self.uow.enterprise_repository.get_enterprise_specialist_by_id(enterprise_payroll_request.specialist_id)
            AccessControl.can_make_enterprise_payroll_request(specialist.user_id, requesting_user)
            enterprise = await self.uow.enterprise_repository.get_enterprise_by_id(enterprise_payroll_request.enterprise_id)
            enterprise_account = await self.uow.account_repository.get_account_by_id(enterprise.account_id)
            payment_amount = len(enterprise_payroll_request.passport_numbers) * enterprise_payroll_request.amount
            if payment_amount > enterprise_account.balance:
                raise InsufficientFundsError(enterprise_account.balance)
            for account_id in enterprise_payroll_request.accounts_id:
                user_account = await self.uow.account_repository.get_account_by_id(account_id)
                new_account_balance = user_account.balance + enterprise_payroll_request.amount
                await self.uow.account_repository.update_account_balance(user_account.id, new_account_balance)
            new_enterprise_account_balance = enterprise_account.balance - payment_amount
            await self.uow.account_repository.update_account_balance(enterprise_account.id, new_enterprise_account_balance)