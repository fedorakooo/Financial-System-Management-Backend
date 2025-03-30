from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from dependency_injector.wiring import Provide, inject

from src.api.exceptions.exception_factory import HttpExceptionFactory
from src.application.abstractions.auth.auth import AbstractAuthService
from src.application.abstractions.logs.log import AbstractLogService
from src.application.dtos.user import UserAccessDTO
from src.domain.abstractions.database.uows.user import AbstractUserUnitOfWork
from src.domain.exceptions.forbidden import UserInactiveError
from src.infrastructure.dependencies.app import Application
from src.infrastructure.exceptions.jwt_exceptions import ExpiredTokenError, InvalidTokenError, TokenDecodeError
from src.infrastructure.exceptions.repository_exceptions import NotFoundError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@inject
async def get_current_active_auth_user(
        token: str = Depends(oauth2_scheme),
        user_uow: AbstractUserUnitOfWork = Depends(Provide[Application.uow.user_unit_of_work]),
        auth_service: AbstractAuthService = Depends(
            Provide[Application.services.auth_service]
        ),
        log_service: AbstractLogService = Depends(
            Provide[Application.services.log_service]
        )
) -> UserAccessDTO:
    try:
        identity = auth_service.get_current_active_auth_user(token)
        async with user_uow as uow:
            try:
                user = await uow.user_repository.get_user_by_id(identity.id)
            except NotFoundError:
                raise InvalidTokenError("Token user no longer exists")
        if not user.is_active:
            raise UserInactiveError()
        return UserAccessDTO(id=user.id, role=user.role)
    except ExpiredTokenError as exc:
        raise HttpExceptionFactory.create_http_exception(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    except InvalidTokenError as exc:
        raise HttpExceptionFactory.create_http_exception(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    except TokenDecodeError as exc:
        raise HttpExceptionFactory.create_http_exception(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    except UserInactiveError as exc:
        raise HttpExceptionFactory.create_http_exception(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
    except Exception as exc:
        log_service.error(f"Unexpected error occurred: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
