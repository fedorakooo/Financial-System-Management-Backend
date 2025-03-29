from abc import ABC, abstractmethod

from src.application.dtos.user import UserUpdateDTO, UserReadDTO, UserAccessDTO


class AbstractUserManagementService(ABC):
    """Abstract service for staff-level users to manage users."""

    @abstractmethod
    async def get_user_by_id(self, user_id: int, requesting_user: UserAccessDTO) -> UserReadDTO:
        """Retrieve user information by its ID."""
        pass

    @abstractmethod
    async def get_all_users(self, requesting_user: UserAccessDTO) -> list[UserReadDTO]:
        """Retrieve a list of users."""
        pass

    @abstractmethod
    async def update_user_by_id(
            self,
            user_id: int,
            user_update_dto: UserUpdateDTO,
            requesting_user: UserAccessDTO
    ) -> UserUpdateDTO:
        """Update an existing user's information by its ID."""
        pass


    @abstractmethod
    async def delete_user_by_id(self, user_id: int, requesting_user: UserAccessDTO) -> None:
        """Delete a user by its ID"""
        pass
