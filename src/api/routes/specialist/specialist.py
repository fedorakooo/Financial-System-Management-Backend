from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import Provide, inject

from src.api.security import get_current_active_auth_user
from src.application.abstractions.enterprises.enterprise_specialist import AbstractEnterpriseSpecialistService
from src.application.dtos.enterprise import (
    EnterpriseSpecialistReadDTO,
    EnterprisePayrollRequestReadDTO,
    EnterprisePayrollTransactionReadDTO,
    EnterprisePayrollRequestCreateDTO
)
from src.application.dtos.user import UserAccessDTO
from src.infrastructure.dependencies.app import Application
from src.infrastructure.exceptions.repository_exceptions import NotFoundError
from src.infrastructure.mappers.enterprise import EnterpriseSchemaMapper
from src.infrastructure.schemas.enterprise import (
    EnterpriseSpecialistResponse,
    EnterprisePayrollRequestResponse,
    EnterprisePayrollTransactionResponse, EnterprisePayrollRequestCreateRequest
)

router = APIRouter(prefix="/enterprises/specialists", tags=["Enterprise Specialist"])


@router.get("/profile", response_model=EnterpriseSpecialistResponse, responses={
    404: {"description": "Enterprise Specialist profile not found"},
    500: {"description": "Unexpected server error"}
})
@inject
async def get_enterprise_specialist_profile(
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        enterprise_specialist_service: AbstractEnterpriseSpecialistService = Depends(
            Provide[Application.services.enterprise_specialist_service]
        )
) -> EnterpriseSpecialistReadDTO:
    try:
        enterprise_specialist_dto = await enterprise_specialist_service.get_enterprise_specialist_profile(requesting_user)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
    return EnterpriseSchemaMapper.map_enterprise_specialist_to_response(enterprise_specialist_dto)


@router.get("/payroll_requests/{payroll_request_id}", response_model=EnterprisePayrollRequestResponse, responses={
    404: {"description": "Payroll Request not found"},
    500: {"description": "Unexpected server error"}
})
@inject
async def get_enterprise_payroll_request_by_id(
        payroll_request_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        enterprise_specialist_service: AbstractEnterpriseSpecialistService = Depends(
            Provide[Application.services.enterprise_specialist_service]
        )
) -> EnterprisePayrollRequestReadDTO:
    try:
        enterprise_payroll_request_dto = await enterprise_specialist_service.get_enterprise_payroll_request_by_id(
            payroll_request_id, requesting_user
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
    return EnterpriseSchemaMapper.map_enterprise_payroll_request_to_response(enterprise_payroll_request_dto)


@router.get("/payroll_transactions/{payroll_request_id}", response_model=EnterprisePayrollTransactionResponse, responses={
    404: {"description": "Payroll Transactions not found"},
    500: {"description": "Unexpected server error"}
})
@inject
async def get_payroll_transactions_by_enterprise_payroll_request_id(
        payroll_request_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        enterprise_specialist_service: AbstractEnterpriseSpecialistService = Depends(
            Provide[Application.services.enterprise_specialist_service]
        )
) -> list[EnterprisePayrollTransactionReadDTO]:
    try:
        payroll_transactions_dto = await enterprise_specialist_service.get_payroll_transactions_by_enterprise_payroll_request_id(
            payroll_request_id, requesting_user
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
    return [EnterpriseSchemaMapper.map_enterprise_payroll_transaction_to_response(transaction) for transaction in payroll_transactions_dto]


@router.post("/payroll_requests", response_model=EnterprisePayrollRequestResponse, responses={
    500: {"description": "Unexpected server error"}
})
@inject
async def create_enterprise_payroll_request(
        enterprise_payroll_request: EnterprisePayrollRequestCreateRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        enterprise_specialist_service: AbstractEnterpriseSpecialistService = Depends(
            Provide[Application.services.enterprise_specialist_service]
        )
) -> EnterprisePayrollRequestResponse:
    enterprise_payroll_request_dto = EnterpriseSchemaMapper.map_enterprise_payroll_request_from_create_request(enterprise_payroll_request)
    try:
        created_enterprise_payroll_request_dto = await enterprise_specialist_service.create_enterprise_payroll_request(
            enterprise_payroll_request_dto,
            requesting_user
        )
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
    return EnterpriseSchemaMapper.map_enterprise_payroll_request_to_response(created_enterprise_payroll_request_dto)


@router.post("/payroll_requests/{payroll_request_id}/make", response_model=EnterprisePayrollRequestResponse, responses={
    400: {"description": "Invalid request"},
    500: {"description": "Unexpected server error"}
})
@inject
async def make_enterprise_payroll_request(
        payroll_request_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        enterprise_specialist_service: AbstractEnterpriseSpecialistService = Depends(
            Provide[Application.services.enterprise_specialist_service]
        )
) -> EnterprisePayrollRequestResponse:
    try:
        await enterprise_specialist_service.make_enterprise_payroll_request(payroll_request_id, requesting_user)
        # Optionally, fetch the updated payroll request if needed after making the payment
        enterprise_payroll_request_dto = await enterprise_specialist_service.get_enterprise_payroll_request_by_id(
            payroll_request_id,
            requesting_user
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
    return EnterpriseSchemaMapper.map_enterprise_payroll_request_to_response(enterprise_payroll_request_dto)
