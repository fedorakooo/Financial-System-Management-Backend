from datetime import datetime

from src.application.dtos.account import AccountUpdateClientDTO, AccountCreateDTO, AccountUpdateStaffDTO, AccountReadDTO
from src.domain.entities.account import Account
from src.domain.enums.account import AccountType, AccountStatus


class AccountMapper:
    """Utility class for mapping between Account-related DTOs and domain entities."""

    @staticmethod
    def map_account_create_dto_to_account(
            dto: AccountCreateDTO,
            user_id: int,
            account_type: AccountType,
            account_status: AccountStatus
    ) -> Account:
        return Account(
            user_id=user_id,
            bank_id=dto.bank_id,
            type=account_type,
            status=account_status
        )

    @staticmethod
    def map_account_update_client_dto_to_account(dto: AccountUpdateClientDTO, current_account: Account) -> Account:
        return Account(
            id=current_account.id,
            bank_id=current_account.bank_id,
            user_id=current_account.user_id,
            balance=current_account.balance,
            status=dto.status if dto.status else current_account.status,
            type=current_account.type,
            created_at=current_account.created_at,
            updated_at=datetime.now()
        )

    @staticmethod
    def map_account_update_staff_dto_to_account(dto: AccountUpdateStaffDTO, current_account: Account) -> Account:
        return Account(
            id=current_account.id,
            bank_id=current_account.bank_id,
            user_id=current_account.user_id,
            balance=current_account.balance,
            status=dto.status if dto.status else current_account.status,
            created_at=current_account.created_at,
            type=current_account.type,
            updated_at=datetime.now()
        )

    @staticmethod
    def map_account_to_account_read_dto(account: Account) -> AccountReadDTO:
        return AccountReadDTO(
            id=account.id,
            user_id=account.user_id,
            bank_id=account.bank_id,
            balance=account.balance,
            status=account.status,
            type=account.type,
            created_at=account.created_at,
            updated_at=account.updated_at
        )
