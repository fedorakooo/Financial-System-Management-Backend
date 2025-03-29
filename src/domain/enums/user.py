from enum import Enum


class UserRole(Enum):
    CLIENT = "CLIENT"
    OPERATOR = "OPERATOR"
    MANAGER = "MANAGER"
    ADMINISTRATOR = "ADMINISTRATOR"
    SPECIALIST = "SPECIALIST"
