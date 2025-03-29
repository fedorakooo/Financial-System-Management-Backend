from dependency_injector import providers, containers

from src.application.services.accounts.account_management import AccountManagementService
from src.application.services.accounts.account_profile import AccountProfileService
from src.application.services.additions.addition_profile import AdditionProfileService
from src.application.services.auth.auth import AuthService
from src.application.services.auth.login import LoginService
from src.application.services.auth.password import PasswordService
from src.application.services.auth.payload import PayloadExtractorService
from src.application.services.auth.token import TokenService
from src.application.services.auth.user import AuthUserService
from src.application.services.banks.bank_management import BankManagementService
from src.application.services.banks.bank_public import BankPublicService
from src.application.services.deposits.deposit_profile import DepositProfileService
from src.application.services.enterprises.enterprise_management import EnterpriseManagementService
from src.application.services.enterprises.enterprise_specialist import EnterpriseSpecialistService
from src.application.services.loans.loan_management import LoanManagementService
from src.application.services.loans.loan_profile import LoanProfileService
from src.application.services.logs.log import LogService
from src.application.services.profile.profile import ProfileService
from src.application.services.registration.registration import UserRegistrationService
from src.application.services.transfer.transfer_management import TransferManagementService
from src.application.services.transfer.transfer_profile import TransferProfileService
from src.application.services.users.user_management import UserManagementService
from src.application.services.withdrawals.withdrawal_profile import WithdrawalProfileService
from src.domain.entities.enterprise import EnterpriseSpecialist


class Services(containers.DeclarativeContainer):
    config = providers.Configuration()

    core = providers.DependenciesContainer()
    uow = providers.DependenciesContainer()

    log_service = providers.Factory(
        LogService,
        logger=core.logger
    )

    token_service = providers.Factory(
        TokenService,
        token_handler=core.token_handler,
    )

    payload_extractor_service = providers.Factory(
        PayloadExtractorService,
        token_handler=core.token_handler,
    )

    password_service = providers.Factory(
        PasswordService,
        password_handler=core.password_handler,
    )

    auth_service = providers.Factory(
        AuthService,
        token_service=token_service,
        payload_extractor_service=payload_extractor_service,
    )

    user_registration_service = providers.Factory(
        UserRegistrationService,
        uow=uow.user_unit_of_work,
        password_handler=core.password_handler
    )

    auth_user_service = providers.Factory(
        AuthUserService,
        uow=uow.user_unit_of_work,
    )

    login_service = providers.Factory(
        LoginService,
        auth_user_service=auth_user_service,
        password_service=password_service,
        token_service=token_service,
    )

    bank_info_service = providers.Factory(
        BankPublicService,
        uow=uow.bank_unit_of_work,
    )

    profile_service = providers.Factory(
        ProfileService,
        uow=uow.user_unit_of_work,
    )

    account_profile_service = providers.Factory(
        AccountProfileService,
        uow=uow.account_unit_of_work,
    )

    addition_profile_service = providers.Factory(
        AdditionProfileService,
        uow=uow.addition_unit_of_work,
    )

    bank_management_service = providers.Factory(
        BankManagementService,
        uow=uow.bank_unit_of_work,
    )

    user_management_service = providers.Factory(
        UserManagementService,
        uow=uow.user_unit_of_work,
    )

    account_management_service = providers.Factory(
        AccountManagementService,
        uow=uow.account_unit_of_work,
    )

    withdrawal_profile_service = providers.Factory(
        WithdrawalProfileService,
        uow=uow.withdrawal_unit_of_work,
    )

    transfer_profile_service = providers.Factory(
        TransferProfileService,
        uow=uow.transfer_unit_of_work,
    )

    loan_profile_service = providers.Factory(
        LoanProfileService,
        uow=uow.loan_unit_of_work,
    )

    loan_management_service = providers.Factory(
        LoanManagementService,
        uow=uow.loan_unit_of_work,
    )

    deposit_profile_service = providers.Factory(
        DepositProfileService,
        uow=uow.deposit_unit_of_work,
    )

    transfer_management_service = providers.Factory(
        TransferManagementService,
        uow=uow.transfer_unit_of_work,
    )

    enterprise_management_service = providers.Factory(
        EnterpriseManagementService,
        uow=uow.enterprise_unit_of_work
    )

    enterprise_specialist_service = providers.Factory(
        EnterpriseSpecialistService,
        uow=uow.enterprise_unit_of_work
    )
