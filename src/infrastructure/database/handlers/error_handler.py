from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from dataclasses import asdict, is_dataclass
from src.infrastructure.exceptions.repository_exceptions import UniqueConstraintError, ForeignKeyError


class ErrorHandler:
    """Class for handling database handlers."""

    @staticmethod
    def handle_unique_violation(
            entity: str,
            error: UniqueViolationError,
            item: object
    ) -> UniqueConstraintError:
        """Handles unique constraint violation handlers."""

        if not is_dataclass(item):
            raise ValueError("Item must be a dataclass instance")

        error_message = str(error).lower()
        item_dict = asdict(item)

        for column in item_dict.keys():
            if column in error_message:
                return UniqueConstraintError(entity, column, item_dict[column])

        return UniqueConstraintError(entity, "unknown_column", "unknown_value")

    @staticmethod
    def handle_foreign_key_violation(
            entity: str,
            error: ForeignKeyViolationError
    ) -> ForeignKeyError:
        """Handles foreign key constraint violation handlers."""

        import re
        match = re.search(r"Key \((.*?)\)=\((.*?)\) is not present", error.detail)
        if match:
            field, value = match.group(1), match.group(2)
        else:
            field, value = "unknown_field", "unknown_value"

        referenced_table = error.constraint_name.split("_")[0] if error.constraint_name else "unknown_table"
        return ForeignKeyError(entity, field, value, referenced_table)
