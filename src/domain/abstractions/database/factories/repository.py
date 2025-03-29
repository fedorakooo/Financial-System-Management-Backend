from abc import ABC, abstractmethod

from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.additions import AbstractAdditionRepository
from src.domain.abstractions.database.repositories.banks import AbstractBankRepository
from src.domain.abstractions.database.repositories.deposit import AbstractDepositRepository
from src.domain.abstractions.database.repositories.enterprise import AbstractEnterpriseRepository
from src.domain.abstractions.database.repositories.loans import AbstractLoanRepository
from src.domain.abstractions.database.repositories.transfer import AbstractTransferRepository
from src.domain.abstractions.database.repositories.users import AbstractUserRepository
from src.domain.abstractions.database.repositories.withdrawals import AbstractWithdrawalRepository


class AbstractRepositoryFactory(ABC):
    @abstractmethod
    def create_account_repository(self, connection) -> AbstractAccountRepository:
        pass

    @abstractmethod
    def create_addition_repository(self, connection) -> AbstractAdditionRepository:
        pass

    @abstractmethod
    def create_bank_repository(self, connection) -> AbstractBankRepository:
        pass

    @abstractmethod
    def create_transfer_repository(self, connection) -> AbstractTransferRepository:
        pass

    @abstractmethod
    def create_user_repository(self, connection) -> AbstractUserRepository:
        pass

    @abstractmethod
    def create_withdrawal_repository(self, connection) -> AbstractWithdrawalRepository:
        pass

    @abstractmethod
    def create_loan_repository(self, connection) -> AbstractLoanRepository:
        pass

    @abstractmethod
    def create_deposit_repository(self, connection) -> AbstractDepositRepository:
        pass

    @abstractmethod
    def create_enterprise_repository(self, connection) -> AbstractEnterpriseRepository:
        pass