from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import Provide, inject

from src.api.security import get_current_active_auth_user
from src.application.abstractions.accounts.account_management import AbstractAccountManagementService
from src.application.abstractions.logs.log import AbstractLogService
from src.application.dtos.user import UserAccessDTO
from src.domain.exceptions.forbidden import ForbiddenError
from src.infrastructure.dependencies.app import Application
from src.infrastructure.exceptions.repository_exceptions import UniqueConstraintError, ForeignKeyError, NotFoundError
from src.infrastructure.schemas.account import AccountResponse, AccountCreateRequest

from src.api.routes.staff.accounts.operation.loan import router as loan_router
from src.api.routes.staff.accounts.operation.transfer import router as transfer_router

router = APIRouter(prefix="/accounts", tags=["Accounts Management"])
router.include_router(loan_router)
router.include_router(transfer_router)


@router.get("/", response_model=list[AccountResponse], responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive or lacks required role to access this resource"},
    500: {"description": "Unexpected server error"}
})
@inject
async def get_user_accounts(
        user_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        account_management_service: AbstractAccountManagementService = Depends(
            Provide[Application.services.account_management_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> list[AccountResponse]:
    try:
        accounts = await account_management_service.get_accounts_by_user_id(
            user_id,
            requesting_user
        )
        log_service.info(f"Successfully fetched accounts for user ID {user_id}")
    except ForbiddenError as exc:
        raise exc
    except Exception as exc:
        raise exc
        log_service.error(f"An unexpected error occurred while fetching accounts for user ID {user_id}: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the list of accounts."
        )
    return accounts


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive or does not have permission"},
    404: {"description": "Account not found"},
    500: {"description": "Unexpected server error"}
})
@inject
async def delete_account_by_id(
        account_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        account_management_service: AbstractAccountManagementService = Depends(
            Provide[Application.services.account_management_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> None:
    log_service.info(f"Deleting account with ID {account_id}")
    try:
        await account_management_service.delete_account_by_id(account_id, requesting_user)
        log_service.info(f"Account with ID {account_id} deleted successfully")
    except NotFoundError as exc:
        log_service.warning(f"Account with ID {account_id} not found for deletion: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )
    except ForbiddenError as exc:
        log_service.error(f"Forbidden error while deleting the account with ID {account_id}: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc)
        )
    except Exception as exc:
        log_service.error(f"An unexpected error while deleting the account with ID {account_id}: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the account with id {account_id}."
        )
    return {"message": "Bank deleted successfully"}
