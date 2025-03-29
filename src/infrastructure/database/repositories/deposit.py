from typing import Any

from src.domain.abstractions.database.repositories.deposit import AbstractDepositRepository
from src.domain.entities.deposit import DepositAccount, DepositTransaction
from src.infrastructure.database.mappers.deposit import DepositDatabaseMapper
from src.infrastructure.exceptions.repository_exceptions import NotFoundError


class DepositRepository(AbstractDepositRepository):
    def __init__(self, connection: Any):
        self.connection = connection

    async def get_deposit_account_by_id(self, deposit_account_id: int) -> DepositAccount:
        stmt = "SELECT * FROM deposit_accounts WHERE id = $1"
        row = await self.connection.fetchrow(stmt, deposit_account_id)
        if row is None:
            raise NotFoundError(f"Deposit account with id = {deposit_account_id} not found")
        return DepositDatabaseMapper.from_db_row_to_deposit_account(row)

    async def create_deposit_transaction(self, deposit_transaction_create: DepositTransaction) -> DepositTransaction:
        loan_create_row = DepositDatabaseMapper.from_deposit_transaction_to_db_row(deposit_transaction_create)
        columns = ', '.join(loan_create_row.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(loan_create_row))])
        values = tuple(loan_create_row.values())

        stmt = f"INSERT INTO deposit_transactions ({columns}) VALUES ({placeholders}) RETURNING *"
        row = await self.connection.fetchrow(stmt, *values)
        return DepositDatabaseMapper.from_db_row_to_deposit_transaction(row)

    async def create_deposit_account(self, deposit_account_create: DepositAccount) -> DepositAccount:
        loan_create_row = DepositDatabaseMapper.from_deposit_account_to_db_row(deposit_account_create)
        columns = ', '.join(loan_create_row.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(loan_create_row))])
        values = tuple(loan_create_row.values())

        stmt = f"INSERT INTO deposit_accounts ({columns}) VALUES ({placeholders}) RETURNING *"
        row = await self.connection.fetchrow(stmt, *values)
        return DepositDatabaseMapper.from_db_row_to_deposit_account(row)
