class UserNotFoundError(Exception):
    """Custom exception for user not found errors."""
    pass

class PasswordMismatchError(Exception):
    """Custom exception for password mismatch errors."""
    pass