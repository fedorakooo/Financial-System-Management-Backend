from typing import Any

from src.domain.abstractions.database.repositories.additions import AbstractAdditionRepository
from src.domain.entities.addition import Addition
from src.infrastructure.database.mappers.addition import AdditionDatabaseMapper
from src.infrastructure.exceptions.repository_exceptions import NotFoundError


class AdditionRepository(AbstractAdditionRepository):
    def __init__(self, db_connection: Any):
        self.connection = db_connection

    async def get_addition_by_id(self, addition_id: int) -> Addition:
        stmt = "SELECT * FROM additions WHERE id = $1"

        row = await self.connection.fetchrow(stmt, addition_id)

        if row:
            return AdditionDatabaseMapper.from_db_row(row)

        raise NotFoundError("Addition with id = {addition_id} not found")

    async def get_additions(self) -> list[Addition]:
        stmt = "SELECT * FROM additions"

        rows = await self.connection.fetch(stmt)

        return [AdditionDatabaseMapper.from_db_row(row) for row in rows]

    async def get_additions_by_account_id(self, account_id: int) -> list[Addition]:
        stmt = "SELECT * FROM additions WHERE account_id = $1"

        rows = await self.connection.fetch(stmt, account_id)

        return [AdditionDatabaseMapper.from_db_row(row) for row in rows]

    async def create_addition(self, addition_create: Addition) -> Addition:
        addition_create_row = AdditionDatabaseMapper.to_db_row(addition_create)

        columns = ', '.join(addition_create_row.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(addition_create_row))])
        values = tuple(addition_create_row.values())

        stmt = f"INSERT INTO additions ({columns}) VALUES ({placeholders}) RETURNING *"

        row = await self.connection.fetchrow(stmt, *values)

        return AdditionDatabaseMapper.from_db_row(row)
