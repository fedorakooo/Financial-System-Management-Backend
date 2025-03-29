from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.api.exceptions.exception_factory import HttpExceptionFactory
from src.api.security import get_current_active_auth_user
from src.application.abstractions.deposits.deposit_profile import AbstractDepositProfileService
from src.application.abstractions.logs.log import AbstractLogService
from src.application.dtos.user import UserAccessDTO
from src.domain.exceptions.forbidden import ForbiddenError
from src.infrastructure.dependencies.app import Application
from src.infrastructure.exceptions.repository_exceptions import NotFoundError
from src.infrastructure.mappers.account import AccountSchemaMapper
from src.infrastructure.mappers.deposit import DepositSchemaMapper
from src.infrastructure.schemas.account import AccountCreateRequest
from src.infrastructure.schemas.deposit import (
    DepositAccountResponse,
    DepositAccountCreateRequest,
    DepositTransactionResponse,
    DepositTransactionCreateClientRequest
)

router = APIRouter(prefix="/deposit_accounts", tags=["Deposits"])


@router.get("/{deposit_account_id}", response_model=DepositAccountResponse)
@inject
async def get_deposit_account_by_id(
        deposit_account_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        deposit_profile_service: AbstractDepositProfileService = Depends(
            Provide[Application.services.deposit_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> DepositAccountResponse:
    try:
        fetched_deposit_account_dto = await deposit_profile_service.get_deposit_account_by_id(
            deposit_account_id,
            requesting_user
        )
    except ForbiddenError as exc:
        raise HttpExceptionFactory.create_http_exception(status.HTTP_403_FORBIDDEN, str(exc))
    except NotFoundError as exc:
        raise HttpExceptionFactory.create_http_exception(status.HTTP_404_NOT_FOUND, str(exc))
    except Exception as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered an error while fetching deposit account with ID {deposit_account_id}: {str(exc)}"
        )
        raise exc
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"An unexpected error occurred while fetching loan account with ID {loan_account_id}."
        )
    fetched_deposit_account = DepositSchemaMapper.map_deposit_account_to_response(fetched_deposit_account_dto)
    return fetched_deposit_account


@router.post("/", response_model=DepositAccountResponse)
@inject
async def create_deposit_account(
        deposit_create_request: DepositAccountCreateRequest,
        account_create_request: AccountCreateRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        deposit_profile_service: AbstractDepositProfileService = Depends(
            Provide[Application.services.deposit_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> DepositAccountResponse:
    log_service.info(
        f"User ID {requesting_user.id} ({requesting_user.role}) is attempting to create deposit account request"
    )
    deposit_create_dto = DepositSchemaMapper.map_deposit_account_from_create_request(
        deposit_create_request,
        requesting_user.id
    )
    account_create_dto = AccountSchemaMapper.from_create_request(account_create_request, requesting_user.id)
    try:
        created_deposit_account_dto = await deposit_profile_service.create_deposit_account(
            deposit_create_dto,
            account_create_dto,
            requesting_user
        )
        log_service.info(
            f"User ID {requesting_user.id} ({requesting_user.role}) successfully created deposit account with ID {created_deposit_account_dto.id}"
        )
    except ForbiddenError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered a ForbiddenError while creating deposit account: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_403_FORBIDDEN, str(exc))
    except Exception as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered an unexpected error while creating deposit account: {str(exc)}"
        )
        raise exc
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while creating deposit account."
        )
    created_deposit_account = DepositSchemaMapper.map_deposit_account_to_response(created_deposit_account_dto)
    return created_deposit_account


@router.post("/{deposit_account_id}", response_model=list[DepositTransactionResponse])
@inject
async def transfer_from_deposit_to_account(
        deposit_account_id: int,
        deposit_transaction_create_request: DepositTransactionCreateClientRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        deposit_profile_service: AbstractDepositProfileService = Depends(
            Provide[Application.services.deposit_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> list[DepositTransactionResponse]:
    deposit_transaction_create_dto = DepositSchemaMapper.map_deposit_transaction_client_from_create_request(
        deposit_transaction_create_request,
        deposit_account_id
    )
    try:
        created_deposit_transaction_dto = await deposit_profile_service.transfer_from_deposit_to_account(
            deposit_transaction_create_dto,
            requesting_user
        )
    except NotFoundError as exc:
        raise HttpExceptionFactory.create_http_exception(status.HTTP_404_NOT_FOUND, str(exc))
    except ForbiddenError as exc:
        raise HttpExceptionFactory.create_http_exception(status.HTTP_403_FORBIDDEN, str(exc))
    except Exception as exc:
        raise exc
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while creating loan transaction."
        )
    created_loan_transaction = DepositSchemaMapper.map_deposit_transfer_to_response(created_deposit_transaction_dto)
    return created_loan_transaction
