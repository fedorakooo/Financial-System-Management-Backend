from dependency_injector import containers, providers

from src.infrastructure.database.uows.account import AccountUnitOfWork
from src.infrastructure.database.uows.addition import AdditionUnitOfWork
from src.infrastructure.database.uows.bank import BankUnitOfWork
from src.infrastructure.database.uows.deposit import DepositUnitOfWork
from src.infrastructure.database.uows.enterprise import EnterpriseUnitOfWork
from src.infrastructure.database.uows.loan import LoanUnitOfWork
from src.infrastructure.database.uows.transfer import TransferUnitOfWork
from src.infrastructure.database.uows.user import UserUnitOfWork
from src.infrastructure.database.uows.withdrawal import WithdrawalUnitOfWork


class UnitOfWork(containers.DeclarativeContainer):
    gateways = providers.DependenciesContainer()

    bank_unit_of_work = providers.Factory(
        BankUnitOfWork,
        db_connection=gateways.database_connection,
        repository_factory=gateways.repository_factory,
    )

    user_unit_of_work = providers.Factory(
        UserUnitOfWork,
        db_connection=gateways.database_connection,
        repository_factory=gateways.repository_factory,
    )

    account_unit_of_work = providers.Factory(
        AccountUnitOfWork,
        db_connection=gateways.database_connection,
        repository_factory=gateways.repository_factory,
    )

    addition_unit_of_work = providers.Factory(
        AdditionUnitOfWork,
        db_connection=gateways.database_connection,
        repository_factory=gateways.repository_factory,
    )

    withdrawal_unit_of_work = providers.Factory(
        WithdrawalUnitOfWork,
        db_connection=gateways.database_connection,
        repository_factory=gateways.repository_factory,
    )

    transfer_unit_of_work = providers.Factory(
        TransferUnitOfWork,
        db_connection=gateways.database_connection,
        repository_factory=gateways.repository_factory,
    )

    loan_unit_of_work = providers.Factory(
        LoanUnitOfWork,
        db_connection=gateways.database_connection,
        repository_factory=gateways.repository_factory,
    )

    deposit_unit_of_work = providers.Factory(
        DepositUnitOfWork,
        db_connection=gateways.database_connection,
        repository_factory=gateways.repository_factory,
    )

    enterprise_unit_of_work = providers.Factory(
        EnterpriseUnitOfWork,
        db_connection=gateways.database_connection,
        repository_factory=gateways.repository_factory,
    )