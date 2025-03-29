from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import Provide, inject

from src.api.routes.general.registration.registration import user_registration
from src.api.security import get_current_active_auth_user
from src.application.abstractions.enterprises.enterprise_management import AbstractEnterpriseManagementService
from src.application.abstractions.registration.registration import AbstractUserRegistrationService
from src.application.dtos.enterprise import EnterpriseReadDTO, EnterprisePayrollRequestReadDTO, EnterpriseCreateDTO
from src.application.dtos.user import UserAccessDTO
from src.infrastructure.dependencies.app import Application
from src.infrastructure.exceptions.repository_exceptions import NotFoundError
from src.infrastructure.mappers.enterprise import EnterpriseSchemaMapper
from src.infrastructure.mappers.user import UserSchemaMapper
from src.infrastructure.schemas.enterprise import EnterprisePayrollRequestResponse, EnterpriseResponse, \
    EnterpriseCreateRequest, EnterpriseSpecialistCreateRequest, EnterpriseSpecialistResponse
from src.infrastructure.schemas.user import UserCreateRequest

router = APIRouter(prefix="/enterprises", tags=["Enterprise Management"])


@router.get("/{enterprise_id}", response_model = EnterpriseResponse, responses={
    404: {"description": "Enterprise not found"},
    500: {"description": "Unexpected server error"}
})
@inject
async def get_enterprise_by_id(
        enterprise_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        enterprise_service: AbstractEnterpriseManagementService = Depends(
            Provide[Application.services.enterprise_management_service]
        )
) -> EnterpriseReadDTO:
    try:
        enterprise_dto = await enterprise_service.get_enterprise_by_id(enterprise_id, requesting_user)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
    return EnterpriseSchemaMapper.map_enterprise_to_response(enterprise_dto)

@router.post("/", response_model=EnterpriseResponse, responses={
    500: {"description": "Unexpected server error"}
})
@inject
async def create_enterprise(
        enterprise_create: EnterpriseCreateRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        enterprise_service: AbstractEnterpriseManagementService = Depends(
            Provide[Application.services.enterprise_management_service]
        )
) -> EnterpriseResponse:
    try:
        created_enterprise_dto = await enterprise_service.create_enterprise(enterprise_create, requesting_user)
    except Exception as exc:
        raise exc
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
    return EnterpriseSchemaMapper.map_enterprise_to_response(created_enterprise_dto)

@router.get("/payroll_requests/{payroll_request_id}", response_model=EnterprisePayrollRequestResponse)
@inject
async def get_enterprise_payroll_request_by_id(
        payroll_request_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        enterprise_service: AbstractEnterpriseManagementService = Depends(
            Provide[Application.services.enterprise_management_service]
        )
) -> EnterprisePayrollRequestResponse:
    try:
        enterprise_payroll_request_dto = await enterprise_service.get_enterprise_payroll_request_by_id(payroll_request_id, requesting_user)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
    enterprise_payload_request = EnterpriseSchemaMapper.map_enterprise_payroll_request_to_response(enterprise_payroll_request_dto)
    return enterprise_payload_request

@router.post("/payroll_requests/{payroll_request_id}", response_model=EnterprisePayrollRequestResponse, responses={
    400: {"description": "Invalid request"},
    500: {"description": "Unexpected server error"}
})
@inject
async def approve_enterprise_payroll_request(
        payroll_request_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        enterprise_service: AbstractEnterpriseManagementService = Depends(
            Provide[Application.services.enterprise_management_service]
        )
) -> EnterprisePayrollRequestResponse:
    try:
        enterprise_payroll_request_dto = await enterprise_service.approve_enterprise_payroll_request(payroll_request_id, requesting_user)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
    enterprise_payload_request = EnterpriseSchemaMapper.map_enterprise_payroll_request_to_response(enterprise_payroll_request_dto)
    return enterprise_payload_request

@router.post("/specialist", response_model=EnterpriseSpecialistResponse, responses={
    400: {"description": "Invalid request"},
    500: {"description": "Unexpected server error"}
})
@inject
async def create_enterprise_specialist(
        enterprise_specialist_create: EnterpriseSpecialistCreateRequest,
        user_create: UserCreateRequest,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        enterprise_service: AbstractEnterpriseManagementService = Depends(
            Provide[Application.services.enterprise_management_service]
        ),
        user_registration_service: AbstractUserRegistrationService = Depends(
            Provide[Application.services.user_registration_service]
        )
) -> EnterpriseSpecialistResponse:
    user_create_dto = UserSchemaMapper.from_create_request(user_create)
    created_user = await user_registration_service.create_user_specialist(user_create_dto)
    enterprise_specialist_create_dto = EnterpriseSchemaMapper.map_enterprise_specialist_from_create_request(
        enterprise_specialist_create,
        created_user.id
    )
    created_enterprise_specialist_dto = await enterprise_service.create_enterprise_specialist(
        enterprise_specialist_create_dto,
        requesting_user
    )
    enterprise_specialist = EnterpriseSchemaMapper.map_enterprise_specialist_to_response(created_enterprise_specialist_dto)
    return enterprise_specialist

