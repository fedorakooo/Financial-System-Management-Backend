from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import Provide, inject

from src.api.security import get_current_active_auth_user
from src.application.abstractions.banks.bank_management import AbstractBankManagementService
from src.application.abstractions.logs.log import AbstractLogService
from src.application.dtos.user import UserAccessDTO
from src.infrastructure.dependencies.app import Application
from src.infrastructure.mappers.bank import BankSchemaMapper
from src.infrastructure.schemas.bank import BankResponse, BankCreateRequest, BankUpdateRequest
from src.infrastructure.exceptions.repository_exceptions import (
    NotFoundError,
    UniqueConstraintError,
    NoFieldsToUpdateError
)

router = APIRouter(prefix="/banks", tags=["Banks Management"])


@router.get("/{bank_id}", response_model=BankResponse, responses={
    404: {"description": "Bank not found"},
    500: {"description": "Unexpected server error"}
})
@inject
async def get_bank_by_id(
        bank_id: int,
        bank_management_service: AbstractBankManagementService = Depends(
            Provide[Application.services.bank_management_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> BankResponse:
    try:
        bank_dto = await bank_management_service.get_bank_by_id(bank_id)
        log_service.info(f"Successfully fetched bank with ID {bank_id}")
    except NotFoundError as exc:
        log_service.warning(f"Bank with ID {bank_id} not found: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )
    except Exception as exc:
        log_service.error(f"An unexpected error occurred while fetching the bank with ID {bank_id}: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the bank."
        )
    return BankSchemaMapper.to_response(bank_dto)


@router.get("/", response_model=list[BankResponse], responses={
    500: {"description": "Unexpected server error"}
})
@inject
async def get_banks(
        bank_management_service: AbstractBankManagementService = Depends(
            Provide[Application.services.bank_management_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> list[BankResponse]:
    try:
        banks = await bank_management_service.get_banks()
        log_service.info(f"Successfully fetched {len(banks)} banks")
    except Exception as exc:
        log_service.error(f"An unexpected error occurred while fetching the list of banks: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the list of banks."
        )
    return banks


@router.post("/", response_model=BankResponse, responses={
    409: {"description": "A bank with these details already exists"},
    500: {"description": "Unexpected server error"}
})
@inject
async def create_bank(
        bank_create: BankCreateRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        bank_management_service: AbstractBankManagementService = Depends(
            Provide[Application.services.bank_management_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> BankResponse:
    log_service.info(f"Creating bank with name {bank_create.name}")
    try:
        created_bank = await bank_management_service.create_bank(bank_create, requesting_user)
        log_service.info(f"Bank with name {created_bank.name} and ID {created_bank.id} successfully created")
    except UniqueConstraintError as exc:
        log_service.error(
            f"Unique constraint violation while creating the bank with name {bank_create.name}: {str(exc)}"
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        )
    except Exception as exc:
        log_service.error(
            f"An unexpected error occurred while creating the bank with name {bank_create.name}: {str(exc)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the bank."
        )
    return created_bank


@router.patch("/{bank_id}", response_model=BankResponse, responses={
    404: {"description": "Bank not found"},
    400: {"description": "No fields to update"},
    409: {"description": "Conflict due to a unique constraint violation"},
    500: {"description": "Unexpected server error"}
})
@inject
async def update_bank_by_id(
        bank_id: int,
        bank_update: BankUpdateRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        bank_management_service: AbstractBankManagementService = Depends(
            Provide[Application.services.bank_management_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> BankResponse:
    log_service.info(f"Updating bank with ID {bank_id}")
    try:
        updated_bank = await bank_management_service.update_bank_by_id(bank_id, bank_update, requesting_user)
        log_service.info(f"Bank with ID {bank_id} successfully updated")
    except NotFoundError as exc:
        log_service.error(f"Bank with ID {bank_id} not found for update: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )
    except NoFieldsToUpdateError as exc:
        log_service.error(f"No fields to update for bank with ID {bank_id}: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )
    except UniqueConstraintError as exc:
        log_service.error(f"Unique constraint violation while updating bank with ID {bank_id}: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        )
    except Exception as exc:
        raise exc
        log_service.error(f"An unexpected error while updating the bank with ID {bank_id}: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while updating the bank with id {bank_id}."
        )
    return updated_bank


@router.delete("/{bank_id}", response_model=dict, status_code=status.HTTP_200_OK, responses={
    404: {"description": "Bank not found"},
    500: {"description": "Unexpected server error"}
})
async def delete_bank_by_id(
        bank_id: int,
        bank_management_service: AbstractBankManagementService = Depends(
            Provide[Application.services.bank_management_service]
        ),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])

) -> dict:
    log_service.info(f"Deleting bank with ID {bank_id}")
    try:
        await bank_management_service.delete_bank_by_id(bank_id)
        log_service.info(f"Bank with ID {bank_id} deleted successfully")
    except NotFoundError as exc:
        log_service.warning(f"Bank with ID {bank_id} not found for deletion: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )
    except Exception as exc:
        log_service.error(f"An unexpected error while deleting the bank with ID {bank_id}: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the bank with id {bank_id}."
        )
    return {"message": "Bank deleted successfully"}
