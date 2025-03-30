from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.api.exceptions.exception_factory import HttpExceptionFactory
from src.api.security import get_current_active_auth_user
from src.application.abstractions.withdrawals.withdrawal_profile import AbstractWithdrawalProfileService
from src.application.abstractions.logs.log import AbstractLogService
from src.application.dtos.user import UserAccessDTO
from src.domain.exceptions.forbidden import ForbiddenError
from src.infrastructure.dependencies.app import Application
from src.infrastructure.exceptions.repository_exceptions import NotFoundError, UniqueConstraintError, ForeignKeyError
from src.infrastructure.mappers.withdrawal import WithdrawalSchemaMapper
from src.infrastructure.schemas.withdrawal import WithdrawalResponse, WithdrawalCreateRequest

router = APIRouter(prefix="/withdrawals", tags=["Withdrawals"])


@router.get("/", response_model=list[WithdrawalResponse], responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    500: {"description": "Unexpected server error"}
})
@inject
async def get_withdrawals_by_account_id(
        account_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        withdrawal_profile_service: AbstractWithdrawalProfileService = Depends(
            Provide[Application.services.withdrawal_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> list[WithdrawalResponse]:
    try:
        log_service.info(f"User ID {requesting_user.id} ({requesting_user.role}) is fetching withdrawals")
        fetched_withdrawals = await withdrawal_profile_service.get_withdrawals_by_account_id(
            account_id,
            requesting_user
        )
        log_service.info(f"Successfully fetched withdrawals for User ID {requesting_user.id} ({requesting_user.role})")
    except ForbiddenError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered a ForbiddenError while fetching withdrawals: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_403_FORBIDDEN, str(exc))
    except NotFoundError as exc:
        log_service.warning(
            f"User ID {requesting_user.id} ({requesting_user.role}) tried to access non-existent withdrawals: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_404_NOT_FOUND, str(exc))
    except Exception as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered an error while fetching withdrawals: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while fetching the list of withdrawals."
        )
    return fetched_withdrawals


@router.post("/", response_model=WithdrawalResponse, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive or does not have permission"},
    409: {"description": "Conflict due to a unique constraint violation"},
    422: {"description": "Unprocessable Entity due to foreign key constraint"},
    500: {"description": "Unexpected server error"}
})
@inject
async def create_withdrawal(
        account_id: int,
        withdrawal_create: WithdrawalCreateRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        withdrawal_profile_service: AbstractWithdrawalProfileService = Depends(
            Provide[Application.services.withdrawal_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> WithdrawalResponse:
    log_service.info(f"User ID {requesting_user.id} ({requesting_user.role}) is attempting to create an withdrawal")
    withdrawal_create_dto = WithdrawalSchemaMapper.from_create_request(withdrawal_create, account_id)
    try:
        created_withdrawal = await withdrawal_profile_service.create_withdrawal(
            withdrawal_create_dto,
            requesting_user
        )
        log_service.info(
            f"User ID {requesting_user.id} ({requesting_user.role}) successfully created withdrawal with ID {created_withdrawal.id}"
        )
    except UniqueConstraintError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered unique constraint violation while creating withdrawal: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_409_CONFLICT, str(exc))
    except ForeignKeyError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered foreign key constraint violation while creating withdrawal: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc))
    except ForbiddenError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered a ForbiddenError while creating withdrawal: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_403_FORBIDDEN, str(exc))
    except Exception as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered an unexpected error while creating withdrawal: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while creating the withdrawal."
        )
    return created_withdrawal
