"""Exceptions Module

This module defines the custom exception hierarchy for the quarryforge package.
It includes a base exception class and specific exceptions for different
modules within the package.
"""
import datetime


class QuarryForgeError(Exception):
    """Base Exception Class for quarryforge

    Provides all common attributes and methods for QuarryForge exceptions.

    Attributes:
        code (str, optional):
            The error code for a specific exception
        details (dict, optional):
            A dictionary containing more detailed error information.
        timestamp (datetime.datetime):
            The time when the exception was raised.
        user_message (str, optional):
            A user-friendly message for display.

    Methods:
        to_dict(): Returns a dictionary representation of the exception.
        __str__(): Returns a formatted string representation of the exception.
    """
    def __init__(self,
                 message=None,
                 code=None,
                 details=None,
                 user_message=None):
        super().__init__(message)
        self.code = code
        self.details = details or {}
        self.timestamp = datetime.datetime.utcnow()
        self.user_message = user_message or message

    def to_dict(self):
        """Returns a dictionary representation of the exception."""
        return {
            'message': str(self),
            'code': self.code,
            'details': self.details,
            'timestamp': self.timestamp.isoformat(),
            'user_message': self.user_message,
        }

    def __str__(self):
        """Returns a formatted string representation of the exception."""
        message = super().__str__()
        parts = []
        if self.code:
            parts.append(f'[{self.code}]')
        if message:
            parts.append(message)

        if self.details:
            detail_str = ', '.join(
                [f'{key}: {value}' for key, value in self.details.items()]
            )
            parts.append(f'({detail_str})')
        return ' '.join(parts)


class ArgumentError(QuarryForgeError):
    """Argument Error exception for quarryforge

    Raised when invalid arguments or combinations escape argparse checks.
    """
    def __init__(self, message: str = 'A quarryforge argument error occurred'):
        super().__init__(message)
        self.message = message


class FossilCommandError(QuarryForgeError):
    """Fossil Command Error

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(self, message: str, returncode: int, cmd: str,
                 stdout: str = None, stderr: str = None):
        super().__init__(message)
        self.returncode = returncode
        self.cmd = cmd
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self) -> str:
        return (f'{self.__class__.__name__}: Fossil command failed with '
                f'return code {self.returncode}.  Command: {self.cmd}. '
                f'Error: {self.message}')


class ConfigError(ArgumentError):
    """Configuration Error

    Raised when there is an issue with the configuration of the quarryforge
    package, such as a missing or invalid configuration file, or missing
    required configuration values.
    """
    pass


class RepositoryOperationError(QuarryForgeError):
    """Repository Operation Error

    Raised when a general repository operation fails, such as creating a
    new repository, setting user configurations, or any other repository-level
    operation.
    """
    pass


class FileOperationError(QuarryForgeError):
    """File Operation Error

    Raised when an operation involving files fails, such as reading file
    content or determining file changes.
    """
    pass
