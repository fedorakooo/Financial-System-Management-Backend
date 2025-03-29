from typing import Any
from asyncpg.exceptions import UniqueViolationError

from src.domain.abstractions.database.repositories.users import AbstractUserRepository
from src.domain.entities.user import User
from src.infrastructure.exceptions.repository_exceptions import NotFoundError
from src.infrastructure.database.mappers.user import UserDatabaseMapper
from src.infrastructure.database.handlers.error_handler import ErrorHandler


class UserRepository(AbstractUserRepository):
    def __init__(self, connection: Any):
        self.connection = connection

    async def get_user_by_id(self, user_id: int) -> User:
        stmt = "SELECT * FROM users WHERE id = $1"

        row = await self.connection.fetchrow(stmt, user_id)

        if row:
            return UserDatabaseMapper.from_db_row(row)

        raise NotFoundError(f"User with id = {user_id} not found")

    async def get_user_by_phone_number(self, phone_number: str) -> User:
        stmt = "SELECT * FROM users WHERE phone_number = $1"

        row = await self.connection.fetchrow(stmt, phone_number)

        if row:
            return UserDatabaseMapper.from_db_row(row)

        raise NotFoundError(f"User with phone_number = {phone_number} not found")

    async def get_user_hashed_password_by_phone_number(self, phone_number: str) -> str:
        stmt = "SELECT hashed_password FROM users WHERE phone_number = $1"

        row = await self.connection.fetchrow(stmt, phone_number)

        if row:
            return row['hashed_password']

        raise NotFoundError(f"User with phone_number = {phone_number} not found")

    async def get_users(self) -> list[User]:
        stmt = "SELECT * FROM users"

        rows = await self.connection.fetch(stmt)

        return [UserDatabaseMapper.from_db_row(row) for row in rows] if rows else []

    async def create_user(self, user_create: User) -> User:
        user_create_row = UserDatabaseMapper.to_db_row(user_create)

        columns = ', '.join(user_create_row.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(user_create_row))])
        values = tuple(user_create_row.values())

        stmt = f"INSERT INTO users ({columns}) VALUES ({placeholders}) RETURNING *"

        try:
            row = await self.connection.fetchrow(stmt, *values)
        except UniqueViolationError as exc:
            raise ErrorHandler.handle_unique_violation("User", exc, user_create)

        return UserDatabaseMapper.from_db_row(row)

    async def update_user_by_id(self, user_id: int, user_update: User) -> User:
        user_update_row = UserDatabaseMapper.to_db_row(user_update)

        columns = ', '.join([f"{key} = ${i + 1}" for i, key in enumerate(user_update_row.keys())])
        values = tuple(user_update_row.values()) + (user_id,)
        stmt = f"UPDATE users SET {columns} WHERE id = ${len(values)} RETURNING *"

        try:
            row = await self.connection.fetchrow(stmt, *values)
        except UniqueViolationError as exc:
            raise ErrorHandler.handle_unique_violation("User", exc, user_update)

        if row:
            return UserDatabaseMapper.from_db_row(row)

        raise NotFoundError(f"User with id = {user_id} not found")

    async def delete_user_by_id(self, user_id: int) -> None:
        stmt = "DELETE FROM users WHERE id = $1"

        result = await self.connection.execute(stmt, user_id)

        if result == "DELETE 0":
            raise NotFoundError(f"User with id = {user_id} not found")
