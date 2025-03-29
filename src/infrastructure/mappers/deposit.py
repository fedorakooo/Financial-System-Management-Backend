from src.infrastructure.mappers.account import AccountSchemaMapper
from src.infrastructure.schemas.loan import LoanTransactionResponse
from src.application.dtos.deposit import (
    DepositAccountReadDTO,
    DepositAccountCreateDTO,
    DepositTransactionCreateClientDTO, DepositTransactionReadDTO
)
from src.infrastructure.schemas.deposit import (
    DepositAccountResponse,
    DepositTransactionResponse,
    DepositAccountCreateRequest,
    DepositTransactionCreateClientRequest
)

class DepositSchemaMapper:
    """Utility class for mapping between Data Transfer Objects (DTOs) and Pydantic models for the Deposit entities."""

    @staticmethod
    def map_deposit_account_to_response(
            dto: DepositAccountReadDTO,
    ) -> DepositAccountResponse:
        account = AccountSchemaMapper.to_response(dto.account)
        return DepositAccountResponse(
            id=dto.id,
            interest_rate=dto.interest_rate,
            account=account,
            from_account_id=dto.from_account_id
        )

    @staticmethod
    def map_deposit_transfer_to_response(dto: DepositTransactionReadDTO) -> DepositTransactionResponse:
        return DepositTransactionResponse(
            id=dto.id,
            deposit_account_id=dto.deposit_account_id,
            type=dto.type,
            amount=dto.amount,
            created_at=dto.created_at
        )

    @staticmethod
    def map_deposit_account_from_create_request(
            request: DepositAccountCreateRequest,
            user_id: int
    ) -> DepositAccountCreateDTO:
        return DepositAccountCreateDTO(
            amount=request.amount,
            interest_rate=request.interest_rate,
            bank_id=request.interest_rate,
            user_id=user_id,
            from_account_id=request.from_account_id
        )

    @staticmethod
    def map_deposit_transaction_client_from_create_request(
            request: DepositTransactionCreateClientRequest,
            deposit_account_id: int
    ) -> DepositTransactionCreateClientDTO:
        return DepositTransactionCreateClientDTO(
            account_id=request.account_id,
            deposit_account_id=deposit_account_id
        )