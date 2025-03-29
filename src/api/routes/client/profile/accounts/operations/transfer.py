from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.api.exceptions.exception_factory import HttpExceptionFactory
from src.api.security import get_current_active_auth_user
from src.application.abstractions.transfers.transfer_profile import AbstractTransferProfileService
from src.application.abstractions.logs.log import AbstractLogService
from src.application.dtos.user import UserAccessDTO
from src.domain.exceptions.forbidden import ForbiddenError
from src.infrastructure.dependencies.app import Application
from src.infrastructure.exceptions.repository_exceptions import NotFoundError, UniqueConstraintError, ForeignKeyError
from src.infrastructure.mappers.transfer import TransferSchemaMapper
from src.infrastructure.schemas.transfer import TransferResponse, TransferCreateRequest

router = APIRouter(prefix="/transfers", tags=["Transfers"])


@router.get("/", response_model=list[TransferResponse], responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    500: {"description": "Unexpected server error"}
})
@inject
async def get_transfers_by_account_id(
        account_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        transfer_profile_service: AbstractTransferProfileService = Depends(
            Provide[Application.services.transfer_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> list[TransferResponse]:
    try:
        log_service.info(f"User ID {requesting_user.id} ({requesting_user.role}) is fetching transfers")
        fetched_transfers_dto = await transfer_profile_service.get_transfers_by_account_id(
            account_id,
            requesting_user
        )
        log_service.info(f"Successfully fetched transfers for User ID {requesting_user.id} ({requesting_user.role})")
    except ForbiddenError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered a ForbiddenError while fetching transfers: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_403_FORBIDDEN, str(exc))
    except NotFoundError as exc:
        log_service.warning(
            f"User ID {requesting_user.id} ({requesting_user.role}) tried to access non-existent transfers: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_404_NOT_FOUND, str(exc))
    except Exception as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered an error while fetching transfers: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while fetching the list of transfers."
        )
    fetched_transfers = [TransferSchemaMapper.to_response(fetched_transfer_dto) for fetched_transfer_dto in fetched_transfers_dto]
    return fetched_transfers


@router.post("/", response_model=TransferResponse, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive or does not have permission"},
    409: {"description": "Conflict due to a unique constraint violation"},
    422: {"description": "Unprocessable Entity due to foreign key constraint"},
    500: {"description": "Unexpected server error"}
})
@inject
async def create_transfer(
        account_id: int,
        transfer_create: TransferCreateRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        transfer_profile_service: AbstractTransferProfileService = Depends(
            Provide[Application.services.transfer_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> TransferResponse:
    log_service.info(f"User ID {requesting_user.id} ({requesting_user.role}) is attempting to create an transfer")
    transfer_create_dto = TransferSchemaMapper.from_create_request(transfer_create, account_id)
    try:
        created_transfer = await transfer_profile_service.create_transfer(
            transfer_create_dto,
            requesting_user
        )
        log_service.info(
            f"User ID {requesting_user.id} ({requesting_user.role}) successfully created transfer with ID {created_transfer.id}"
        )
    except UniqueConstraintError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered unique constraint violation while creating transfer: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_409_CONFLICT, str(exc))
    except ForeignKeyError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered foreign key constraint violation while creating transfer: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc))
    except ForbiddenError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered a ForbiddenError while creating transfer: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_403_FORBIDDEN, str(exc))
    except Exception as exc:
        raise exc
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered an unexpected error while creating transfer: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while creating the transfer."
        )
    return created_transfer
