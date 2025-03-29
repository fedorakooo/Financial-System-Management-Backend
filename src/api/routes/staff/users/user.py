from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.api.exceptions.exception_factory import HttpExceptionFactory
from src.api.security import get_current_active_auth_user
from src.application.abstractions.logs.log import AbstractLogService
from src.application.abstractions.users.user_management import AbstractUserManagementService
from src.application.dtos.user import UserAccessDTO, UserReadDTO
from src.infrastructure.dependencies.app import Application
from src.infrastructure.mappers.user import UserSchemaMapper
from src.infrastructure.schemas.user import UserResponse, UserUpdateRequest
from src.infrastructure.exceptions.repository_exceptions import (
    NotFoundError,
    UniqueConstraintError,
    NoFieldsToUpdateError
)

router = APIRouter(prefix="/users", tags=["Users Management"])


@router.get("/{user_id}", response_model=UserResponse, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive or lacks required role to access this resource"},
    404: {"description": "User not found"},
    500: {"description": "Unexpected server error"}
})
@inject
async def get_user_by_id(
        user_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        user_management_service: AbstractUserManagementService = Depends(
            Provide[Application.services.user_management_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> UserReadDTO:
    try:
        fetched_user_dto = await user_management_service.get_user_by_id(user_id, requesting_user)
        log_service.info(f"User with ID {requesting_user.id} successfully fetched user with ID {user_id}.")
    except NotFoundError as exc:
        log_service.warning(f"User with ID {requesting_user.id} failed to fetch user with ID {user_id}: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        log_service.error(
            f"User with ID {requesting_user.id} encountered an unexpected error while fetching user with ID {user_id}: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred fetching the user."
        )
    return UserSchemaMapper.to_response(fetched_user_dto)


@router.get("/", response_model=list[UserReadDTO], responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive or lacks required role to access this resource"},
    500: {"description": "Unexpected server error"}
})
@inject
async def get_users(
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        user_management_service: AbstractUserManagementService = Depends(
            Provide[Application.services.user_management_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> list[UserReadDTO]:
    try:
        fetched_users_dto = await user_management_service.get_all_users(requesting_user)
        log_service.info(f"User with ID {requesting_user.id} successfully fetched {len(fetched_users_dto)} users.")
    except Exception as exc:
        log_service.error(
            f"User with ID {requesting_user.id} encountered an unexpected error while fetching users: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred fetching fetching the list of users."
        )
    return [UserSchemaMapper.to_response(fetched_user_dto) for fetched_user_dto in fetched_users_dto]


@router.patch("/{user_id}", response_model=UserReadDTO, responses={
    400: {"description": "No fields to update"},
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive or lacks required role to access this resource"},
    404: {"description": "User not found"},
    409: {"description": "Conflict due to a unique constraint violation"},
    500: {"description": "Unexpected server error"}
})
@inject
async def update_user_by_id(
        user_id: int,
        user_update: UserUpdateRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        user_management_service: AbstractUserManagementService = Depends(
            Provide[Application.services.user_management_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> UserResponse:
    log_service.info(f"User with ID {requesting_user.id} is updating user with ID {user_id}")
    try:
        updated_user = await user_management_service.update_user_by_id(user_id, user_update)
        log_service.info(f"User with ID {requesting_user.id} successfully updated user with ID {user_id}")
    except NotFoundError as exc:
        log_service.error(
            f"User with ID {requesting_user.id} attempted to update user with ID {user_id}, but user not found: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except NoFieldsToUpdateError as exc:
        log_service.error(
            f"User with ID {requesting_user.id} attempted to update user with ID {user_id}, but no fields to update: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except UniqueConstraintError as exc:
        log_service.error(
            f"User with ID {requesting_user.id} attempted to update user with ID {user_id}, but a unique constraint violation occurred: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except Exception as exc:
        log_service.error(
            f"User with ID {requesting_user.id} encountered an unexpected error while updating user with ID {user_id}: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while updating the bank with id {user_id}."
        )
    return updated_user


@router.delete("/{user_id}", response_model=dict, status_code=status.HTTP_200_OK, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive or lacks required role to access this resource"},
    404: {"description": "User not found"},
    500: {"description": "Unexpected server error"}
})
@inject
async def delete_user_by_id(
        user_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        user_management_service: AbstractUserManagementService = Depends(
            Provide[Application.services.user_management_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> dict:
    log_service.info(f"User with ID {requesting_user.id} is attempting to delete user with ID {user_id}")
    try:
        await user_management_service.delete_user_by_id(user_id)
        log_service.info(f"User with ID {requesting_user.id} successfully deleted user with ID {user_id}")
    except NotFoundError as exc:
        log_service.warning(
            f"User with ID {requesting_user.id} attempted to delete user with ID {user_id}, but user not found: {str(exc)}"
        )
        HttpExceptionFactory.create_http_exception(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        log_service.error(
            f"User with ID {requesting_user.id} encountered an unexpected error while deleting user with ID {user_id}: {str(exc)}"
        )
        HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the user."
        )
    return {"message": "User deleted successfully"}
