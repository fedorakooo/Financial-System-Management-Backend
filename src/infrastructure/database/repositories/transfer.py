from typing import Any

from src.domain.abstractions.database.repositories.transfer import AbstractTransferRepository
from src.domain.entities.transfer import Transfer
from src.domain.enums.transfer import TransferStatus
from src.infrastructure.database.mappers.transfer import TransferDatabaseMapper
from src.infrastructure.exceptions.repository_exceptions import NotFoundError


class TransferRepository(AbstractTransferRepository):
    def __init__(self, connection: Any):
        self.connection = connection

    async def get_transfer_by_id(self, transfer_id: int) -> Transfer:
        stmt = "SELECT * FROM transfers WHERE id = $1"

        row = await self.connection.fetchrow(stmt, transfer_id)

        if row:
            return TransferDatabaseMapper.from_db_row(row)

        raise NotFoundError("Transfer with id = {transfer_id} not found")

    async def get_transfers_by_account_id(self, account_id: int) -> list[Transfer]:
        stmt = "SELECT * FROM transfers WHERE from_account_id = $1 OR to_account_id = $1"

        rows = await self.connection.fetch(stmt, account_id)

        return [TransferDatabaseMapper.from_db_row(row) for row in rows]

    async def create_transfer(self, transfer_create: Transfer) -> Transfer:
        transfer_create_row = TransferDatabaseMapper.to_db_row(transfer_create)

        columns = ', '.join(transfer_create_row.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(transfer_create_row))])
        values = tuple(transfer_create_row.values())

        stmt = f"INSERT INTO transfers ({columns}) VALUES ({placeholders}) RETURNING *"

        row = await self.connection.fetchrow(stmt, *values)
        print(row["status"])
        return TransferDatabaseMapper.from_db_row(row)

    async def update_transfer_status_by_id(
            self,
            transfer_id: int,
            transfer_status: TransferStatus
    ) -> Transfer:
        stmt = f"UPDATE transfers SET status = $2 WHERE id = $1 RETURNING *"
        row = await self.connection.fetchrow(stmt, transfer_id, transfer_status.value)
        if row:
            return TransferDatabaseMapper.from_db_row(row)
        raise NotFoundError(f"Transfer with id = {transfer_id} not found")
