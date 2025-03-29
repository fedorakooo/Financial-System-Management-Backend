from abc import ABC, abstractmethod

from src.application.dtos.addition import AdditionReadDTO, AdditionCreateDTO
from src.application.dtos.user import UserAccessDTO


class AbstractAdditionProfileService(ABC):
    """Abstract service for managing user additions."""

    @abstractmethod
    async def get_additions_by_account_id(
            self,
            account_id: int,
            requesting_user: UserAccessDTO
    ) -> list[AdditionReadDTO]:
        """Retrieve additions associated with the requesting account."""
        pass

    @abstractmethod
    async def create_addition(
            self,
            account_id: int,
            addition_create_dto: AdditionCreateDTO,
            requesting_user: UserAccessDTO
    ) -> AdditionReadDTO:
        """Create a new addition for the requesting user."""
        pass
