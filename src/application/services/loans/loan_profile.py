from src.application.abstractions.loans.loan_profile import AbstractLoanProfileService
from src.application.dtos.account import AccountCreateDTO
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.account import AccountMapper
from src.application.mappers.loan import LoanMapper
from src.domain.abstractions.database.uows.loan import AbstractLoanUnitOfWork
from src.application.services.loans.access_control import LoanProfileAccessControlService as AccessControl
from src.domain.entities.loan import LoanAccount
from src.domain.enums.account import AccountType, AccountStatus
from src.domain.enums.loan import LoanTransactionType
from src.application.dtos.loan import (
    LoanAccountReadDTO,
    LoanCreateDTO,
    LoanTransactionCreateDTO,
    LoanTransactionReadDTO
)
from src.domain.exceptions.account import InactiveAccountError, InsufficientFundsError
from src.domain.exceptions.loan import LoanAccountNonZeroBalanceError
from src.domain.exceptions.payment import PaymentExceedsLimitError


class LoanProfileService(AbstractLoanProfileService):
    def __init__(self, uow: AbstractLoanUnitOfWork):
        self.uow = uow

    async def get_loan_account_by_account_id(
            self,
            account_id: int,
            requesting_user: UserAccessDTO
    ) -> list[LoanAccountReadDTO]:
        async with self.uow as uow:
            loan_account = await self.uow.loan_repository.get_loan_account_by_id(account_id)
            account = await self.uow.account_repository.get_account_by_id(loan_account.account_id)
            AccessControl.can_get_loans(account.user_id, requesting_user)
            loan = await self.uow.loan_repository.get_loan_by_id(loan_account.loan_id)
        loan_read_dto = LoanMapper.map_loan_to_loan_read_dto(loan)
        account_read_dto = AccountMapper.map_account_to_account_read_dto(account)
        loan_account_dto = LoanMapper.map_loan_account_to_loan_account_read_dto(
            loan_account,
            account_read_dto,
            loan_read_dto
        )
        return loan_account_dto

    async def create_loan_request(
            self,
            loan_create_dto: LoanCreateDTO,
            account_create_dto: AccountCreateDTO,
            requesting_user: UserAccessDTO
    ) -> LoanAccountReadDTO:
        async with self.uow as uow:
            AccessControl.can_create_loan_request(requesting_user)
            loan = LoanMapper.map_loan_create_dto_to_loan(loan_create_dto)
            account = AccountMapper.map_account_create_dto_to_account(
                account_create_dto,
                requesting_user.id,
                AccountType.LOAN,
                AccountStatus.ON_CONSIDERATION
            )
            created_loan = await self.uow.loan_repository.create_loan(loan)
            created_account = await self.uow.account_repository.create_account(account)
            created_loan_account = await self.uow.loan_repository.create_loan_account(
                LoanAccount(
                    account_id=created_account.id,
                    loan_id=created_loan.id,
                    user_id=created_account.user_id
                )
            )
        created_loan_account_dto = LoanMapper.map_loan_account_to_loan_account_read_dto(
            created_loan_account,
            created_account, created_loan
        )
        return created_loan_account_dto

    async def create_loan_transaction(
            self,
            loan_account_id: int,
            loan_transaction_create_dto: LoanTransactionCreateDTO,
            requesting_user: UserAccessDTO
    ) -> LoanTransactionReadDTO:
        async with self.uow as uow:
            loan_account = await uow.loan_repository.get_loan_account_by_id(loan_account_id)
            AccessControl.can_create_loan_transaction(loan_account.user_id, requesting_user)
            account = await self.uow.account_repository.get_account_by_id(loan_account.account_id)
            if account.status is not AccountStatus.ACTIVE:
                raise InactiveAccountError(account.status)
            if account.balance < loan_transaction_create_dto.amount:
                raise InsufficientFundsError(account.balance)
            loan = await self.uow.loan_repository.get_loan_by_id(loan_account.loan_id)
            max_allowed_payment = loan.amount * loan.interest_rate
            loan_transactions = await self.uow.loan_repository.get_loan_transactions_by_loan_account_id(loan_account_id)
            already_paid = sum(loan_transaction.amount for loan_transaction in loan_transactions)
            if already_paid + loan_transaction_create_dto.amount > max_allowed_payment:
                raise PaymentExceedsLimitError(
                    payment_amount=loan_transaction_create_dto.amount,
                    already_paid=already_paid,
                    max_allowed=max_allowed_payment
                )
            loan_transaction = LoanMapper.map_loan_transaction_create_dto_to_loan_transaction(
                loan_transaction_create_dto,
                LoanTransactionType.PAYMENT
            )
            created_loan_transaction = await self.uow.loan_repository.create_loan_transaction(loan_transaction)
            await self.uow.account_repository.update_account_balance(
                account.id,
                account.balance - created_loan_transaction.amount
            )
            if already_paid + loan_transaction_create_dto.amount == max_allowed_payment:
                if account.balance == 0:
                    await self.uow.account_repository.update_account_status(account.id, AccountStatus.BLOCKED)
                else:
                    raise LoanAccountNonZeroBalanceError(account.balance)
        created_loan_transaction_dto = LoanMapper.map_loan_transaction_to_loan_transaction_read_dto(
            created_loan_transaction
        )
        return created_loan_transaction_dto


    async def get_loan_transactions_by_loan_account_id(
            self,
            loan_account_id: int,
            requesting_user: UserAccessDTO
    ) -> list[LoanTransactionReadDTO]:
        async with self.uow as uow:
            loan_account = await self.uow.loan_repository.get_loan_account_by_id(loan_account_id)
            AccessControl.can_get_loan_transactions(loan_account.user_id, requesting_user)
            loan_transactions = await self.uow.loan_repository.get_loan_transactions_by_loan_account_id(loan_account_id)

        loan_transactions_dto = [
            LoanMapper.map_loan_transaction_to_loan_transaction_read_dto(loan_transaction) for loan_transaction in loan_transactions
        ]
        return loan_transactions_dto
