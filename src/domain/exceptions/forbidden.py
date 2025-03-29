class ForbiddenError(Exception):
    """Exception raised when a user tries to access a resource they don't have permission for."""

    def __init__(self):
        super().__init__("You do not have permission to perform this action.")


class UserInactiveError(Exception):
    """Exception raised when a user tries to access a resource but their account is inactive."""

    def __init__(self):
        super().__init__("User is inactive and cannot perform this action.")
