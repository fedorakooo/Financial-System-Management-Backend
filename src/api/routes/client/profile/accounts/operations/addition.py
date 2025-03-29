from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.api.exceptions.exception_factory import HttpExceptionFactory
from src.api.security import get_current_active_auth_user
from src.application.abstractions.additions.addition_profile import AbstractAdditionProfileService
from src.application.abstractions.logs.log import AbstractLogService
from src.application.dtos.user import UserAccessDTO
from src.domain.exceptions.forbidden import ForbiddenError
from src.infrastructure.dependencies.app import Application
from src.infrastructure.exceptions.repository_exceptions import NotFoundError, UniqueConstraintError, ForeignKeyError
from src.infrastructure.mappers.addition import AdditionSchemaMapper
from src.infrastructure.schemas.addition import AdditionResponse, AdditionCreateRequest


# main router profile/accounts/...
router = APIRouter(prefix="/additions", tags=["Additions"])


@router.get("/", response_model=list[AdditionResponse], responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    500: {"description": "Unexpected server error"}
})
@inject
async def get_additions_by_account_id(
        account_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        addition_profile_service: AbstractAdditionProfileService = Depends(
            Provide[Application.services.addition_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> list[AdditionResponse]:
    try:
        log_service.info(f"User ID {requesting_user.id} ({requesting_user.role}) is fetching additions")
        fetched_additions_dto = await addition_profile_service.get_additions_by_account_id(
            account_id,
            requesting_user
        )
        log_service.info(f"Successfully fetched additions for User ID {requesting_user.id} ({requesting_user.role})")
    except ForbiddenError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered a ForbiddenError while fetching additions: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_403_FORBIDDEN, str(exc))
    except NotFoundError as exc:
        log_service.warning(
            f"User ID {requesting_user.id} ({requesting_user.role}) tried to access non-existent additions: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_404_NOT_FOUND, str(exc))
    except Exception as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered an error while fetching additions: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while fetching the list of additions."
        )
    fetched_additions = [AdditionSchemaMapper.to_response(fetched_addition_dto) for fetched_addition_dto in fetched_additions_dto]
    return fetched_additions


@router.post("/", response_model=AdditionResponse, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive or does not have permission"},
    409: {"description": "Conflict due to a unique constraint violation"},
    422: {"description": "Unprocessable Entity due to foreign key constraint"},
    500: {"description": "Unexpected server error"}
})
@inject
async def create_addition(
        account_id: int,
        addition_create: AdditionCreateRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        addition_profile_service: AbstractAdditionProfileService = Depends(
            Provide[Application.services.addition_profile_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> AdditionResponse:
    log_service.info(f"User ID {requesting_user.id} ({requesting_user.role}) is attempting to create an addition")
    try:
        created_addition = await addition_profile_service.create_addition(
            account_id,
            addition_create,
            requesting_user
        )
        log_service.info(
            f"User ID {requesting_user.id} ({requesting_user.role}) successfully created addition with ID {created_addition.id}"
        )
    except UniqueConstraintError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered unique constraint violation while creating addition: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_409_CONFLICT, str(exc))
    except ForeignKeyError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered foreign key constraint violation while creating addition: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc))
    except ForbiddenError as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered a ForbiddenError while creating addition: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status.HTTP_403_FORBIDDEN, str(exc))
    except Exception as exc:
        log_service.error(
            f"User ID {requesting_user.id} ({requesting_user.role}) encountered an unexpected error while creating addition: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while creating the addition."
        )
    return created_addition
