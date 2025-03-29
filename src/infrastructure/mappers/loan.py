from src.application.dtos.loan import LoanReadDTO, LoanCreateDTO, LoanTransactionReadDTO, LoanAccountReadDTO, \
    LoanTransactionCreateDTO
from src.infrastructure.mappers.account import AccountSchemaMapper
from src.infrastructure.schemas.loan import (
    LoanResponse,
    LoanCreateRequest,
    LoanTransactionResponse,
    LoanAccountResponse,
    LoanTransactionCreateRequest
)

class LoanSchemaMapper:
    """Utility class for mapping between Data Transfer Objects (DTOs) and Pydantic models for the Loans entities."""

    @staticmethod
    def map_loan_to_response(dto: LoanReadDTO) -> LoanResponse:
        return LoanResponse(
            id=dto.id,
            amount=dto.amount,
            term_months=dto.term_months,
            interest_rate=dto.interest_rate,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @staticmethod
    def map_loan_account_to_response(dto: LoanAccountReadDTO) -> LoanAccountResponse:
        loan_response = LoanSchemaMapper.map_loan_to_response(dto.loan)
        account_response = AccountSchemaMapper.to_response(dto.account)
        return LoanAccountResponse(
            account_id=dto.account_id,
            account=account_response,
            loan_id=dto.loan_id,
            user_id=dto.user_id,
            loan=loan_response,
            id=dto.id
        )

    @staticmethod
    def map_loan_transaction_to_response(dto: LoanTransactionReadDTO) -> LoanTransactionResponse:
        return LoanTransactionResponse(
            loan_account_id=dto.loan_account_id,
            type=dto.type,
            amount=dto.amount,
            id=dto.id,
            created_at=dto.created_at
        )

    @staticmethod
    def map_loan_from_create_request(request: LoanCreateRequest) -> LoanCreateDTO:
        return LoanCreateDTO(
            amount=request.amount,
            term_months=request.term_months,
            interest_rate=request.interest_rate
        )

    @staticmethod
    def map_loan_transaction_from_create_request(
            request: LoanTransactionCreateRequest,
            loan_account_id: int
    ) -> LoanTransactionCreateRequest:
       return LoanTransactionCreateDTO(
           amount=request.amount,
           loan_account_id=loan_account_id
       )