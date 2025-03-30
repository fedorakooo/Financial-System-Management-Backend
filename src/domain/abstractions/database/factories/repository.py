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
        """Creates a account repository bound to the supplied transaction connection."""
        pass

    @abstractmethod
    def create_addition_repository(self, connection) -> AbstractAdditionRepository:
        """Creates a addition repository bound to the supplied transaction connection."""
        pass

    @abstractmethod
    def create_bank_repository(self, connection) -> AbstractBankRepository:
        """Creates a bank repository bound to the supplied transaction connection."""
        pass

    @abstractmethod
    def create_transfer_repository(self, connection) -> AbstractTransferRepository:
        """Creates a transfer repository bound to the supplied transaction connection."""
        pass

    @abstractmethod
    def create_user_repository(self, connection) -> AbstractUserRepository:
        """Creates a user repository bound to the supplied transaction connection."""
        pass

    @abstractmethod
    def create_withdrawal_repository(self, connection) -> AbstractWithdrawalRepository:
        """Creates a withdrawal repository bound to the supplied transaction connection."""
        pass

    @abstractmethod
    def create_loan_repository(self, connection) -> AbstractLoanRepository:
        """Creates a loan repository bound to the supplied transaction connection."""
        pass

    @abstractmethod
    def create_deposit_repository(self, connection) -> AbstractDepositRepository:
        """Creates a deposit repository bound to the supplied transaction connection."""
        pass

    @abstractmethod
    def create_enterprise_repository(self, connection) -> AbstractEnterpriseRepository:
        """Creates a enterprise repository bound to the supplied transaction connection."""
        pass