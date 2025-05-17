"""Main Exceptions

#TODO
"""
from quarryforge.exception.base_exception import QuarryForgeError


class MainError(QuarryForgeError):
    """Main Error"""
    pass


class ArgumentError(MainError):
    """Argument Error exception for quarryforge

    Raised when invalid arguments or combinations escape argparse checks.
    """
    def __init__(self, message: str = 'A quarryforge argument error occurred'):
        super().__init__(message)
        self.message = message
