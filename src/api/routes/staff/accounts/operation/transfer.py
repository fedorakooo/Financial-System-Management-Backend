from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.api.security import get_current_active_auth_user
from src.application.abstractions.logs.log import AbstractLogService
from src.application.abstractions.transfers.transfer_management import AbstractTransferManagementService
from src.application.dtos.user import UserAccessDTO
from src.infrastructure.dependencies.app import Application
from src.infrastructure.mappers.transfer import TransferSchemaMapper
from src.infrastructure.schemas.transfer import TransferResponse

router = APIRouter(prefix="/transfers")


@router.get("/{transfer_id}", response_model=TransferResponse)
@inject
async def get_transfer_by_id(
        transfer_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        transfer_management_service: AbstractTransferManagementService = Depends(
            Provide[Application.services.transfer_management_service]
        ),
        log_service: AbstractLogService = Depends(
            Provide[Application.services.log_service]
        )
) -> TransferResponse:
    fetched_transfer_dto = await transfer_management_service.get_transfer_by_id(transfer_id, requesting_user)
    fetched_transfer = TransferSchemaMapper.to_response(fetched_transfer_dto)
    return fetched_transfer


@router.post("/{transfer_id}", response_model=TransferResponse)
@inject
async def reverse_transfer(
        transfer_id: int,
        requesting_user: UserAccessDTO = Depends(get_current_active_auth_user),
        transfer_management_service: AbstractTransferManagementService = Depends(
            Provide[Application.services.transfer_management_service]
        ),
        log_service: AbstractLogService = Depends(
            Provide[Application.services.log_service]
        )
) -> TransferResponse:
    reversed_transfer_dto = await transfer_management_service.reverse_transfer_by_id(
        transfer_id,
        requesting_user
    )
    reversed_transfer = TransferSchemaMapper.to_response(reversed_transfer_dto)
    return reversed_transfer
