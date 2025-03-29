from typing import Any
from inflection import tableize


class RepositoryError(Exception):
    """Base exception for repository handlers."""
    pass


class NotFoundError(RepositoryError):
    """Exception raised when a record is not found."""

    def __init__(self, message: str):
        super().__init__(message)


class UniqueConstraintError(RepositoryError):
    """Exception raised when a unique constraint is violated."""

    def __init__(self, entity: str, field: str, value: str):
        self.entity = tableize(entity)
        self.field = field
        self.value = value
        super().__init__(f"Value '{value}' for field '{field}' in {entity} violates unique constraint.")


class NoFieldsToUpdateError(RepositoryError):
    """Exception raised when there are no fields to update."""

    DEFAULT_MESSAGE = "No fields to update."

    def __init__(self):
        super().__init__(self.DEFAULT_MESSAGE)


class ForeignKeyError(RepositoryError):
    """Exception raised when a foreign key constraint is violated."""

    def __init__(self, entity: str, field: str, value: Any, referenced_table: str):
        self.entity = entity
        self.field = field
        self.value = value
        self.referenced_table = referenced_table

        super().__init__(
            f"Foreign key violation: {entity}.{field} = {value} does not exist in {referenced_table}."
        )