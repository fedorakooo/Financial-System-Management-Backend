from decimal import Decimal
from typing import Any
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.entities.account import Account
from src.domain.enums.account import AccountStatus
from src.infrastructure.database.handlers.error_handler import ErrorHandler
from src.infrastructure.database.mappers.account import AccountDatabaseMapper
from src.infrastructure.exceptions.repository_exceptions import NotFoundError


class AccountRepository(AbstractAccountRepository):
    def __init__(self, db_connection: Any):
        self.connection = db_connection

    async def get_account_by_id(self, account_id) -> Account:
        stmt = "SELECT * FROM accounts WHERE id = $1"

        row = await self.connection.fetchrow(stmt, account_id)

        if row:
            return AccountDatabaseMapper.from_db_row(row)

        raise NotFoundError(f"Account with id {account_id} not found")

    async def get_accounts_by_user_id(self, user_id) -> list[Account]:
        stmt = "SELECT * FROM accounts WHERE user_id = $1"

        rows = await self.connection.fetch(stmt, user_id)

        return [AccountDatabaseMapper.from_db_row(row) for row in rows] if rows else []

    async def create_account(self, account_create: Account) -> Account:
        account_create_row = AccountDatabaseMapper.to_db_row(account_create)

        columns = ', '.join(account_create_row.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(account_create_row))])
        values = tuple(account_create_row.values())

        stmt = f"INSERT INTO accounts ({columns}) VALUES ({placeholders}) RETURNING *"

        try:
            row = await self.connection.fetchrow(stmt, *values)
        except UniqueViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Account", exc, account_create)
        except ForeignKeyViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Account", exc, account_create)

        return AccountDatabaseMapper.from_db_row(row)

    async def update_account(self, account_id: int, account_update: Account) -> Account:
        account_update_row = AccountDatabaseMapper.to_db_row(account_update)

        columns = ', '.join([f"{key} = ${i + 1}" for i, key in enumerate(account_update_row.keys())])
        values = tuple(account_update_row.values()) + (account_id,)
        stmt = f"UPDATE accounts SET {columns} WHERE id = ${len(values)} RETURNING *"

        try:
            row = await self.connection.fetchrow(stmt, *values)
        except UniqueViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Account", exc, account_update)

        if row:
            return AccountDatabaseMapper.from_db_row(row)

        raise NotFoundError(f"Account with id {account_id} not found")

    async def update_account_balance(self, account_id: int, new_balance: Decimal) -> None:
        stmt = "UPDATE accounts SET balance = $2 WHERE id = $1"

        await self.connection.execute(stmt, account_id, new_balance)

    async def update_account_status(self, account_id: int, new_status: AccountStatus) -> None:
        stmt = "UPDATE accounts SET status = $2 WHERE id = $1"

        await self.connection.execute(stmt, account_id, new_status.value)

    async def delete_account_by_id(self, account_id: int) -> None:
        stmt = "DELETE FROM accounts WHERE id = $1"

        result = await self.connection.execute(stmt, account_id)

        if result == "DELETE 0":
            raise NotFoundError(f"Account with id {account_id} not found")

