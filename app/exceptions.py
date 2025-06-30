class UserNotFoundError(Exception):
    """Custom exception for user not found errors."""
    pass

class PasswordMismatchError(Exception):
    """Custom exception for password mismatch errors."""
    pass


class BusStopNotFoundError(Exception):
    pass

class RouteNotFoundError(Exception):
    """Custom exception for route not found errors."""
    pass