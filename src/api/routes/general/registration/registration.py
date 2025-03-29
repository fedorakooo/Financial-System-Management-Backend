from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.api.exceptions.exception_factory import HttpExceptionFactory
from src.application.abstractions.logs.log import AbstractLogService
from src.application.abstractions.registration.registration import AbstractUserRegistrationService
from src.infrastructure.dependencies.app import Application
from src.infrastructure.exceptions.repository_exceptions import UniqueConstraintError
from src.infrastructure.mappers.user import UserSchemaMapper
from src.infrastructure.schemas.user import UserResponse, UserCreateRequest

router = APIRouter(prefix="/registration", tags=["Registration"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, responses={
    409: {"description": "Conflict due to a unique constraint violation"},
    500: {"description": "Unexpected server error"}
})
@inject
async def user_registration(
        user_create_request: UserCreateRequest,
        registration_service: AbstractUserRegistrationService = Depends(
            Provide[Application.services.user_registration_service],
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service]),
) -> UserResponse:
    log_service.info(f"Attempting to register a new user with phone_number: {user_create_request.phone_number}")
    user_dto = UserSchemaMapper.from_create_request(user_create_request)
    try:
        created_user_dto = await registration_service.create_user_client(user_dto)
        log_service.info(
            f"User successfully registered with phone_number {created_user_dto.phone_number} and ID {created_user_dto.id}"
        )
    except UniqueConstraintError as exc:
        log_service.error(
            f"Unique constraint violation while creating user with phone_number {user_create_request.phone_number}: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except Exception as exc:
        log_service.error(f"Unexpected error occurred during user registration: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while user registration."
        )
    created_user = UserSchemaMapper.to_response(created_user_dto)
    return created_user
