from abc import ABC, abstractmethod

from src.application.dtos.user import UserCreateDTO, UserReadDTO


class AbstractUserRegistrationService(ABC):
    """Abstract service for user registration, where each method handles creating a user with a specific role."""

    @abstractmethod
    async def create_user_client(self, user_create_dto: UserCreateDTO) -> UserReadDTO:
        """Creates a new user with the 'CLIENT' role."""
        pass

    @abstractmethod
    async def create_user_operator(self, user_create_dto: UserCreateDTO) -> UserReadDTO:
        """Creates a new user with the 'OPERATOR' role."""
        pass

    @abstractmethod
    async def create_user_manager(self, user_create_dto: UserCreateDTO) -> UserReadDTO:
        """Creates a new user with the 'MANAGER' role."""
        pass

    @abstractmethod
    async def create_user_admin(self, user_create_dto: UserCreateDTO) -> UserReadDTO:
        """Creates a new user with the 'ADMINISTRATOR' role."""
        pass

    @abstractmethod
    async def create_user_specialist(self, user_create_dto: UserCreateDTO) -> UserReadDTO:
        """Creates a new user with the 'SPECIALIST' role."""
        pass
