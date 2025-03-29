from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import Provide, inject

from src.api.security import get_current_active_auth_user
from src.application.abstractions.accounts.account_profile import AbstractAccountProfileService
from src.application.abstractions.logs.log import AbstractLogService
from src.application.dtos.user import UserAccessDTO
from src.domain.exceptions.account import AccountAlreadyInRequestedStatusError, StatusChangeNotAllowedError
from src.api.exceptions.exception_factory import HttpExceptionFactory
from src.domain.exceptions.forbidden import ForbiddenError
from src.infrastructure.dependencies.app import Application
from src.infrastructure.mappers.account import AccountSchemaMapper
from src.infrastructure.schemas.account import AccountResponse, AccountUpdateRequest, AccountCreateRequest
from src.infrastructure.exceptions.repository_exceptions import (
    UniqueConstraintError,
    ForeignKeyError,
    NotFoundError,
    NoFieldsToUpdateError
)

from src.api.routes.client.profile.accounts.operations.addition import router as addition_router
from src.api.routes.client.profile.accounts.operations.withdrawals import router as withdrawal_router
from src.api.routes.client.profile.accounts.operations.transfer import router as transfer_router
from src.api.routes.client.profile.accounts.operations.loan import router as loan_router
from src.api.routes.client.profile.accounts.operations.deposit import router as deposit_router

router = APIRouter(prefix="/accounts", tags=["Accounts"])
router.include_router(addition_router)
router.include_router(withdrawal_router)
router.include_router(transfer_router)
router.include_router(loan_router)
router.include_router(deposit_router)


@router.get("/{account_id}", response_model=AccountResponse, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    404: {"description": "Account not found"},
    500: {"description": "Unexpected server error"}
})
@inject
async def get_account_by_id(
        account_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        account_profile_service: AbstractAccountProfileService = Depends(
            Provide[Application.services.account_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> AccountResponse:
    log_service.info(f"User ID {requesting_user.id} ({requesting_user.role}) is fetching account with ID {account_id}")
    try:
        fetched_account_dto = await account_profile_service.get_account_by_id(account_id, requesting_user)
        log_service.info(
            f"Successfully fetched account with ID {account_id} for User ID {requesting_user.id} ({requesting_user.role})")
    except ForbiddenError as exc:
        log_service.warning(f"Forbidden access attempt by user ID {requesting_user.id}: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc)
        )
    except NotFoundError as exc:
        log_service.warning(
            f"User ID {requesting_user.id} ({requesting_user.role}) attempted to fetch non-existent account ID {account_id}: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_404_NOT_FOUND,
            f"Account with ID {account_id} not found."
        )
    except Exception as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered an error while fetching account with ID {account_id}: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"An unexpected error occurred while fetching the account with ID {account_id}."
        )
    return AccountSchemaMapper.to_response(fetched_account_dto)


@router.get("/", response_model=list[AccountResponse], responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    500: {"description": "Unexpected server error"}
})
@inject
async def get_user_accounts(
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        account_profile_service: AbstractAccountProfileService = Depends(
            Provide[Application.services.account_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> list[AccountResponse]:
    log_service.info(f"User ID {requesting_user.id} ({requesting_user.role}) is fetching accounts")
    try:
        fetched_accounts_dto = await account_profile_service.get_accounts(requesting_user)
        log_service.info(f"Successfully fetched accounts for User ID {requesting_user.id} ({requesting_user.role})")
    except ForbiddenError as exc:
        log_service.warning(f"Forbidden access attempt by user ID {requesting_user.id}: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc)
        )
    except Exception as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered an error while fetching accounts: {str(exc)}"
        )
        raise exc
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while fetching the list of accounts."
        )
    return [AccountSchemaMapper.to_response(fetched_account_dto) for fetched_account_dto in fetched_accounts_dto]


@router.post("/", response_model=AccountResponse, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive or does not have permission"},
    409: {"description": "Conflict due to a unique constraint violation"},
    500: {"description": "Unexpected server error"}
})
@inject
async def create_account(
        account_create: AccountCreateRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        account_profile_service: AbstractAccountProfileService = Depends(
            Provide[Application.services.account_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> AccountResponse:
    account_create_dto = AccountSchemaMapper.from_create_request(account_create, requesting_user.id)
    log_service.info(f"User ID {requesting_user.id} ({requesting_user.role}) is attempting to create an account")
    try:
        created_account_dto = await account_profile_service.create_account(
            account_create_dto,
            requesting_user
        )
        log_service.info(
            f"User ID {requesting_user.id} ({requesting_user.role}) successfully created account with ID {created_account_dto.id}"
        )
    except UniqueConstraintError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered unique constraint violation while creating account: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_409_CONFLICT, str(exc))
    except ForeignKeyError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered foreign key constraint violation while creating account: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc))
    except Exception as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered an unexpected error while creating account: {str(exc)}"
        )
        raise exc
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while creating the account."
        )
    return AccountSchemaMapper.to_response(created_account_dto)


@router.patch("/{account_id}", response_model=AccountResponse, responses={
    400: {"description": "Bad request"},
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive or does not have permission"},
    404: {"description": "Account not found"},
    500: {"description": "Unexpected server error"}
})
@inject
async def update_account(
        account_id: int,
        account_update: AccountUpdateRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        account_profile_service: AbstractAccountProfileService = Depends(
            Provide[Application.services.account_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> AccountResponse:
    account_update_dto = AccountSchemaMapper.from_update_request_to_client(account_update)
    log_service.info(
        f"User ID {requesting_user.id} ({requesting_user.role}) is attempting to update account with ID {account_id}"
    )
    try:
        updated_account_dto = await account_profile_service.update_account(
            account_id,
            account_update_dto,
            requesting_user
        )
        log_service.info(
            f"User ID {requesting_user.id} ({requesting_user.role}) successfully updated account with ID {updated_account_dto.id}"
        )
    except NotFoundError as exc:
        log_service.warning(
            f"User ID {requesting_user.id} ({requesting_user.role}) attempted to update non-existent account ID {account_id}: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_404_NOT_FOUND,
            f"Account with ID {account_id} not found."
        )
    except ForbiddenError as exc:
        log_service.warning(f"Forbidden access attempt by user ID {requesting_user.id}: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc)
        )
    except NoFieldsToUpdateError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) attempted to update account with ID {account_id} but no fields were provided: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_400_BAD_REQUEST, str(exc))
    except AccountAlreadyInRequestedStatusError as exc:
        log_service.warning(
            f"User ID {requesting_user.id} ({requesting_user.role}) attempted to update account ID {account_id} to the same status: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_400_BAD_REQUEST, str(exc))
    except StatusChangeNotAllowedError as exc:
        log_service.warning(
            f"User ID {requesting_user.id} ({requesting_user.role}) attempted to change account ID {account_id} status: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_403_FORBIDDEN, str(exc))
    except Exception as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered an unexpected error while updating account ID {account_id}: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while processing your request."
        )
    return AccountSchemaMapper.to_response(updated_account_dto)
