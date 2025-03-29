from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.api.exceptions.exception_factory import HttpExceptionFactory
from src.api.security import get_current_active_auth_user
from src.application.abstractions.loans.loan_profile import AbstractLoanProfileService
from src.application.abstractions.logs.log import AbstractLogService
from src.application.dtos.user import UserAccessDTO
from src.domain.exceptions.forbidden import ForbiddenError
from src.infrastructure.dependencies.app import Application
from src.infrastructure.exceptions.repository_exceptions import NotFoundError
from src.infrastructure.mappers.account import AccountSchemaMapper
from src.infrastructure.mappers.loan import LoanSchemaMapper
from src.infrastructure.schemas.account import AccountCreateRequest
from src.infrastructure.schemas.loan import LoanAccountResponse, LoanResponse, LoanCreateRequest, \
    LoanTransactionResponse, LoanTransactionCreateRequest

router = APIRouter(prefix="/loan_accounts", tags=["Loans"])


@router.get("/{account_id}", response_model=LoanAccountResponse)
@inject
async def get_loan_account_by_account_id(
        account_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        loan_profile_service: AbstractLoanProfileService = Depends(
            Provide[Application.services.loan_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> LoanAccountResponse:
    try:
        log_service.info(
            f"User ID {requesting_user.id} ({requesting_user.role}) is fetching loan account with account ID {account_id}"
        )
        fetched_loan_account_dto = await loan_profile_service.get_loan_account_by_account_id(
            account_id,
            requesting_user
        )
        log_service.info(f"Successfully fetched transfers for User ID {requesting_user.id} ({requesting_user.role})")
    except ForbiddenError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered a ForbiddenError while fetching loan account: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_403_FORBIDDEN, str(exc))
    except NotFoundError as exc:
        log_service.warning(
            f"User ID {requesting_user.id} ({requesting_user.role}) tried to access non-existent loan account with ID {loan_account_id}: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_404_NOT_FOUND, str(exc))
    except Exception as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered an error while fetching loan account: {str(exc)}"
        )
        raise exc
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"An unexpected error occurred while fetching loan account with ID {loan_account_id}."
        )
    fetched_loan_account = LoanSchemaMapper.map_loan_account_to_response(fetched_loan_account_dto)
    return fetched_loan_account


@router.post("/", response_model=LoanAccountResponse)
@inject
async def create_loan_request(
        loan_create_request: LoanCreateRequest,
        account_create_request: AccountCreateRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        loan_profile_service: AbstractLoanProfileService = Depends(
            Provide[Application.services.loan_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> LoanAccountResponse:
    log_service.info(f"User ID {requesting_user.id} ({requesting_user.role}) is attempting to create loan request")
    loan_create_dto = LoanSchemaMapper.map_loan_from_create_request(loan_create_request)
    account_create_dto = AccountSchemaMapper.from_create_request(account_create_request, requesting_user.id)
    try:
        created_loan_account_dto = await loan_profile_service.create_loan_request(
            loan_create_dto,
            account_create_dto,
            requesting_user
        )
        log_service.info(
            f"User ID {requesting_user.id} ({requesting_user.role}) successfully created loan request with ID {created_loan_account_dto.id}"
        )
    except ForbiddenError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered a ForbiddenError while creating loan request: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_403_FORBIDDEN, str(exc))
    except Exception as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered an unexpected error while creating loan request: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while creating loan request."
        )
    created_loan_account = LoanSchemaMapper.map_loan_account_to_response(created_loan_account_dto)
    return created_loan_account

@router.post("/{loan_account_id}/transactions", response_model=LoanTransactionResponse)
@inject
async def create_loan_transaction(
        loan_account_id: int,
        loan_transaction_create_request: LoanTransactionCreateRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        loan_profile_service: AbstractLoanProfileService = Depends(
            Provide[Application.services.loan_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> LoanTransactionResponse:
    log_service.info(f"User ID {requesting_user.id} ({requesting_user.role}) is attempting to create loan transaction")
    loan_transaction_create_dto = LoanSchemaMapper.map_loan_transaction_from_create_request(
        loan_transaction_create_request,
        loan_account_id
    )
    try:
        created_loan_transaction_dto = await loan_profile_service.create_loan_transaction(
            loan_account_id,
            loan_transaction_create_dto,
            requesting_user
        )
        log_service.info(
            f"User ID {requesting_user.id} ({requesting_user.role}) successfully created loan transaction with ID {created_loan_transaction_dto.id}"
        )
    except NotFoundError as exc:
        log_service.warning(
            f"User ID {requesting_user.id} ({requesting_user.role}) tried to create loan transaction for non-existent loan account with ID {loan_account_id}: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_404_NOT_FOUND, str(exc))
    except ForbiddenError as exc:
        raise exc
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered a ForbiddenError while creating loan transaction request: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_403_FORBIDDEN, str(exc))
    except Exception as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered an unexpected error while creating loan transaction: {str(exc)}"
        )
        raise exc
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while creating loan transaction."
        )
    created_loan_transaction = LoanSchemaMapper.map_loan_transaction_to_response(created_loan_transaction_dto)
    return created_loan_transaction


@router.get("/{loan_account_id}/transactions", response_model=list[LoanTransactionResponse])
@inject
async def get_loan_transactions_by_loan_account_id(
        loan_account_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        loan_profile_service: AbstractLoanProfileService = Depends(
            Provide[Application.services.loan_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> list[LoanTransactionResponse]:
    try:
        loan_transactions_dto = await loan_profile_service.get_loan_transactions_by_loan_account_id(
            loan_account_id,
            requesting_user
        )
    except Exception as exc:
        raise exc
    loan_transactions = [
        LoanSchemaMapper.map_loan_transaction_to_response(loan_transaction_dto) for loan_transaction_dto in loan_transactions_dto
    ]
    return loan_transactions