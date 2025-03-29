from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from src.api.exceptions.exception_factory import HttpExceptionFactory
from src.application.abstractions.banks.bank_public import AbstractBankPublicService
from src.application.abstractions.logs.log import AbstractLogService
from src.infrastructure.dependencies.app import Application
from src.infrastructure.exceptions.repository_exceptions import NotFoundError
from src.infrastructure.mappers.bank import BankSchemaMapper
from src.infrastructure.schemas.bank import BankResponse

router = APIRouter(prefix="/banks", tags=["Banks"])


@router.get("/{bank_id}", response_model=BankResponse, responses={
    404: {"description": "Bank not found"},
    500: {"description": "Unexpected server error"}
})
@inject
async def get_bank_by_id(
        bank_id: int,
        bank_public_service: AbstractBankPublicService = Depends(Provide[Application.services.bank_info_service]),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> BankResponse:
    try:
        fetched_bank_dto = await bank_public_service.get_bank_by_id(bank_id)
        log_service.info(f"Successfully fetched bank with ID {bank_id}")
    except NotFoundError as exc:
        raise HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )
    except Exception as exc:
        log_service.error(f"An unexpected error occurred while fetching the bank with ID {bank_id}: {str(exc)}")
        raise HttpExceptionFactory.create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the bank."
        )
    bank = BankSchemaMapper.to_response(fetched_bank_dto)
    return bank


@router.get("/", response_model=list[BankResponse], responses={
    500: {"description": "Unexpected server error"}
})
@inject
async def get_banks(
        bank_info_service: AbstractBankPublicService = Depends(Provide[Application.services.bank_info_service]),
        log_service: AbstractLogService = Depends(Provide[Application.services.log_service])
) -> list[BankResponse]:
    try:
        fetched_banks_dto = await bank_info_service.get_banks()
        log_service.info(f"Successfully fetched {len(fetched_banks_dto)} banks")
    except Exception as exc:
        log_service.error(f"An unexpected error occurred while fetching the list of banks: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the list of banks."
        )
    banks = [BankSchemaMapper.to_response(bank_dto) for bank_dto in fetched_banks_dto]
    return banks
