from abc import ABC, abstractmethod
from typing import Optional

from src.application.dtos.profile import ProfileReadDTO, ProfileUpdateDTO
from src.application.dtos.user import UserAccessDTO
from src.domain.entities.user import User


class AbstractProfileService(ABC):
    """Abstract service for managing the profile of the currently authenticated user."""

    @abstractmethod
    async def get_profile(self, requesting_user: UserAccessDTO) -> Optional[ProfileReadDTO]:
        """Retrieve the profile information."""
        pass

    @abstractmethod
    async def update_profile_by_user_id(
            self,
            requesting_user: UserAccessDTO,
            profile_update_dto: ProfileUpdateDTO
    ) -> User:
        """Update the profile information."""
        pass

    @abstractmethod
    async def delete_user_by_id(self, requesting_user: UserAccessDTO) -> None:
        """Delete the user profile."""
        pass
