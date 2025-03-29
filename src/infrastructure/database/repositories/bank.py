from typing import Any
from asyncpg.exceptions import UniqueViolationError

from src.domain.abstractions.database.repositories.banks import AbstractBankRepository
from src.domain.entities.bank import Bank
from src.infrastructure.exceptions.repository_exceptions import NotFoundError, NoFieldsToUpdateError
from src.infrastructure.database.mappers.bank import BankDatabaseMapper
from src.infrastructure.database.handlers.error_handler import ErrorHandler


class BankRepository(AbstractBankRepository):
    def __init__(self, connection: Any):
        self.connection = connection

    async def get_bank_by_id(self, bank_id: int) -> Bank:
        stmt = "SELECT * FROM banks WHERE id = $1"

        row = await self.connection.fetchrow(stmt, bank_id)

        if row is None:
            raise NotFoundError(f"Bank with id = {bank_id} not found")

        return BankDatabaseMapper.from_db_row(row)

    async def get_banks(self) -> list[Bank]:
        stmt = "SELECT * FROM banks"

        rows = await self.connection.fetch(stmt)

        return [BankDatabaseMapper.from_db_row(row) for row in rows]

    async def create_bank(self, bank_create: Bank) -> Bank:
        bank_create_row = BankDatabaseMapper.to_db_row(bank_create)

        columns = ', '.join(bank_create_row.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(bank_create_row))])
        values = tuple(bank_create_row.values())

        stmt = f"INSERT INTO banks ({columns}) VALUES ({placeholders}) RETURNING *"

        try:
            row = await self.connection.fetchrow(stmt, *values)
        except UniqueViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Bank", exc, bank_create)

        return BankDatabaseMapper.from_db_row(row)

    async def update_bank_by_id(self, bank_id: int, bank_update: Bank) -> Bank:
        bank_update_row = BankDatabaseMapper.to_db_row(bank_update)

        columns = ', '.join([f"{key} = ${i + 1}" for i, key in enumerate(bank_update_row.keys())])
        values = tuple(bank_update_row.values()) + (bank_id,)
        stmt = f"UPDATE banks SET {columns} WHERE id = ${len(values)} RETURNING *"

        try:
            row = await self.connection.fetchrow(stmt, *values)
        except UniqueViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Bank", exc, bank_update)

        if row:
            return BankDatabaseMapper.from_db_row(row)

        raise NotFoundError(f"Bank with id = {bank_id} not found")

    async def delete_bank_by_id(self, bank_id: int) -> None:
        stmt = "DELETE FROM banks WHERE id = $1"

        result = await self.connection.execute(stmt, bank_id)

        if result == "DELETE 0":
            raise NotFoundError(f"Bank with id = {bank_id} not found")
