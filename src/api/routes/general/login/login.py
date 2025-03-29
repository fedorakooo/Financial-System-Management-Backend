from fastapi import APIRouter, Depends, Form, status, HTTPException
from dependency_injector.wiring import inject, Provide

from src.api.exceptions.exception_factory import HttpExceptionFactory
from src.application.abstractions.auth.login import AbstractLoginService
from src.application.abstractions.logs.log import AbstractLogService
from src.infrastructure.dependencies.app import Application
from src.infrastructure.exceptions.jwt_exceptions import TokenCreationError, InvalidLoginError
from src.infrastructure.exceptions.repository_exceptions import NotFoundError
from src.infrastructure.schemas.token import TokenInfo

router = APIRouter(tags=["AuthJWT"])


@router.post("/login", response_model=TokenInfo, responses={
    401: {"description": "Invalid phone number or password"},
    404: {"description": "User not found"},
    500: {"description": "Unexpected server error"}
})
@inject
async def login(
        username: str = Form(...),
        password: str = Form(...),
        login_service: AbstractLoginService = Depends(Provide[Application.services.login_service]),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service]),
) -> TokenInfo:
    try:
        access_token = await login_service.authenticate_user(username, password)
    except NotFoundError as exc:
        log_service.error(f"User not found during login attempt for phone_number: {username}: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )
    except InvalidLoginError as exc:
        log_service.error(f"Token creation failed during login attempt for phone_number: {username}: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc)
        )
    except TokenCreationError as exc:
        log_service.error(f"Token creation failed during login attempt for phone_number: {username}: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the authentication token."
        )
    except Exception as exc:
        log_service.error(
            f"Unexpected error during login attempt for username with phone_number: {username}: {str(exc)}"
        )
        raise HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during the authentication process."
        )

    log_service.info(f"User with phone_number {username} successfully logged in.")
    return TokenInfo(
        access_token=access_token,
        token_type="Bearer"
    )
