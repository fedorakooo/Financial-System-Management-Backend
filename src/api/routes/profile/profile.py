from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import Provide, inject

from src.api.exceptions.exception_factory import HttpExceptionFactory
from src.api.security import get_current_active_auth_user
from src.application.abstractions.logs.log import AbstractLogService
from src.application.abstractions.profile.profile import AbstractProfileService
from src.application.dtos.user import UserAccessDTO
from src.domain.entities.user import User
from src.infrastructure.dependencies.app import Application
from src.infrastructure.mappers.profile import ProfileSchemaMapper
from src.infrastructure.schemas.profile import ProfileResponse, ProfileUpdateRequest
from src.infrastructure.exceptions.repository_exceptions import (
    NotFoundError,
    NoFieldsToUpdateError,
    UniqueConstraintError
)

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/", response_model=ProfileResponse, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    500: {"description": "Unexpected server error"}
})
@inject
async def get_profile(
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        profile_service: AbstractProfileService = Depends(Provide[Application.services.profile_service]),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> ProfileResponse:
    try:
        fetched_profile_dto: User = await profile_service.get_profile(requesting_user)
        log_service.info(f"Successfully fetched profile for user_id = {fetched_profile_dto.id}")
    except NotFoundError as exc:
        log_service.warning(f"User with ID {requesting_user.id} failed to fetch profile: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(status.HTTP_404_NOT_FOUND, str(exc))
    except Exception as exc:
        log_service.error(f"Unexpected error occurred while fetching profile for user {requesting_user.id}: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while fetching the user."
        )
    return ProfileSchemaMapper.to_response(fetched_profile_dto)


@router.patch("/", response_model=ProfileResponse, responses={
    400: {"description": "No fields to update"},
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    409: {"description": "Conflict due to a unique constraint violation"},
    500: {"description": "Unexpected server error"}
})
@inject
async def update_profile(
        profile_update: ProfileUpdateRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        profile_service: AbstractProfileService = Depends(Provide[Application.services.profile_service]),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> ProfileResponse:
    log_service.info(f"User {requesting_user.id} is updating profile")
    try:
        updated_user_dto = await profile_service.update_profile_by_user_id(
            requesting_user,
            profile_update
        )
        log_service.info(f"Profile updated successfully for user_id = {updated_user_dto.id}")
    except NotFoundError as exc:
        log_service.error(f"User with ID {requesting_user.id} not found for update: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(status.HTTP_404_NOT_FOUND, str(exc))
    except NoFieldsToUpdateError as exc:
        log_service.error(f"No fields to update for user with ID {requesting_user.id}: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(status.HTTP_400_BAD_REQUEST, str(exc))
    except UniqueConstraintError as exc:
        log_service.error(f"Unique constraint violation for user with ID {requesting_user.id}: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(status.HTTP_409_CONFLICT, str(exc))
    except Exception as exc:
        log_service.error(f"Unexpected error occurred while updating profile for user {requesting_user.id}: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while updating profile."
        )
    return ProfileSchemaMapper.to_response(updated_user_dto)


@router.delete("/", response_model=dict, status_code=status.HTTP_200_OK, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    404: {"description": "User not found for deletion"},
    500: {"description": "Unexpected server error"}
})
@inject
async def delete_profile(
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        user_service: AbstractProfileService = Depends(Provide[Application.services.profile_service]),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> dict:
    log_service.info(f"Attempting to delete profile for user_id = {requesting_user.id}")
    try:
        await user_service.delete_user_by_id(requesting_user)
        log_service.info(f"User with user_id = {requesting_user.id} deleted successfully.")
    except NotFoundError as exc:
        log_service.error(f"User with ID {requesting_user.id} not found for deletion: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(status.HTTP_404_NOT_FOUND, str(exc))
    except Exception as exc:
        log_service.error(f"Unexpected error occurred while deleting profile for user {requesting_user.id}: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while deleting the user."
        )
    return {"message": "Profile deleted successfully"}
