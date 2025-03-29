from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.api.security import get_current_active_auth_user
from src.application.abstractions.loans.loan_management import AbstractLoanManagementService
from src.application.abstractions.logs.log import AbstractLogService
from src.application.dtos.user import UserAccessDTO
from src.infrastructure.dependencies.app import Application
from src.infrastructure.mappers.loan import LoanSchemaMapper
from src.infrastructure.schemas.loan import LoanAccountResponse
router = APIRouter(prefix="/loans")


@router.post("/{loan_account_id}")
@inject
async def approve_loan_account(
        loan_account_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        loan_management_service: AbstractLoanManagementService = Depends(
            Provide[Application.services.loan_management_service]
        ),
        log_service: AbstractLogService = Depends(
            Provide[Application.services.log_service]
        )
) -> LoanAccountResponse:
    approved_loan_account_dto = await loan_management_service.approve_loan_account_request(loan_account_id, requesting_user)
    approved_loan_account = LoanSchemaMapper.map_loan_account_to_response(approved_loan_account_dto)
    return approved_loan_account