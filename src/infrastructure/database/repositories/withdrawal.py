from typing import Any

from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from src.domain.abstractions.database.repositories.withdrawals import AbstractWithdrawalRepository
from src.domain.entities.withdrawal import Withdrawal
from src.infrastructure.database.handlers.error_handler import ErrorHandler
from src.infrastructure.database.mappers.withdrawal import WithdrawalDatabaseMapper
from src.infrastructure.exceptions.repository_exceptions import NotFoundError


class WithdrawalRepository(AbstractWithdrawalRepository):
    def __init__(self, connection: Any):
        self.connection = connection

    async def get_withdrawal_by_id(self, withdrawal_id: int) -> Withdrawal:
        stmt = "SELECT * FROM withdrawals WHERE id = $1"

        row = await self.connection.fetchrow(stmt, withdrawal_id)

        if row:
            return WithdrawalDatabaseMapper.from_db_row(row)

        raise NotFoundError("withdrawal with id = {withdrawal_id} not found")

    async def get_withdrawals(self) -> list[Withdrawal]:
        stmt = "SELECT * FROM withdrawals"

        rows = await self.connection.fetch(stmt)

        return [WithdrawalDatabaseMapper.from_db_row(row) for row in rows]

    async def get_withdrawals_by_account_id(self, account_id: int) -> list[Withdrawal]:
        stmt = "SELECT * FROM withdrawals WHERE account_id = $1"

        rows = await self.connection.fetch(stmt, account_id)

        return [WithdrawalDatabaseMapper.from_db_row(row) for row in rows]

    async def create_withdrawal(self, withdrawal_create: Withdrawal) -> Withdrawal:
        withdrawal_create_row = WithdrawalDatabaseMapper.to_db_row(withdrawal_create)

        columns = ', '.join(withdrawal_create_row.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(withdrawal_create_row))])
        values = tuple(withdrawal_create_row.values())

        stmt = f"INSERT INTO withdrawals ({columns}) VALUES ({placeholders}) RETURNING *"
        try:
            row = await self.connection.fetchrow(stmt, *values)
        except UniqueViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Withdrawal", exc, withdrawal_create)
        except ForeignKeyViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Withdrawal", exc, withdrawal_create)

        return WithdrawalDatabaseMapper.from_db_row(row)
