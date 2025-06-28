"""Base exception module defines the custom exception hierarchy.

It includes a base exception class and specific exceptions for different
modules & subpackages within the QuarryForge package.
"""

import datetime
from typing import Any

from quarryforge.config.exception_conf import exception_data as _


class QuarryForgeError(Exception):
    """Define Base Exception Class for quarryforge.

    Provides all common attributes and methods for QuarryForge exceptions.

    Attributes:
        message (str, optional):
            The error message for the developer.
        code (str, optional):
            The error code for a specific exception.
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

    def __init__(
        self,
        message: str,
        code: str,
        user_message: str,
        details: dict[str, Any] | None = None,
    ):
        """Initialize a new QuarryForgeError instance.

        This constructor expects pre-built error information, typically from an
        `ErrorBuilder`'s `data().to_exception()` method.

        Args:
            code: The unique error code identifier.
            message: The detailed technical error message.
            user_message: A user-friendly message for display.
            details:
                An optional dictionary containing more detailed error
                information.

        """
        super().__init__(message)
        self.code = code
        self.details = details or {}
        self.timestamp = datetime.datetime.now(datetime.UTC)
        self.user_message = user_message

    def to_dict(self) -> dict[str, Any]:
        """Return a dictionary representation of the exception."""
        return {
            _.error_data_config().message: str(self),
            _.error_data_config().code: self.code,
            _.error_data_config().details: self.details,
            _.error_data_config().timestamp: self.timestamp.isoformat(),
            _.error_data_config().user_message: self.user_message,
        }

    def __str__(self) -> str:
        """Return a formatted string representation of the exception."""
        message = super().__str__()
        parts = []
        if self.code:
            parts.append(f'[{self.code}]')
        if message:
            parts.append(message)

        if self.details:
            filtered_details = {}
            for key, value in self.details.items():
                if key not in [
                    _.error_data_config().code,
                    _.error_data_config().message,
                    _.error_data_config().user_message,
                ]:
                    filtered_details[key] = value

            if filtered_details:
                detail_str = ', '.join(
                    [
                        f'{key}: {value}'
                        for key, value in (filtered_details.items())
                    ]
                )
                parts.append(f'({detail_str})')
        return (' ').join(parts)


class ModelError(QuarryForgeError):
    """Base exception class for all exceptions in the model module."""

    pass


class FossilError(QuarryForgeError):
    """Base exception class for all exceptions for the fossil module."""

    pass


class MainError(QuarryForgeError):
    """Base exception class for all exceptions in the main module."""

    pass


class MetaError(QuarryForgeError):
    """Base exception class for all exceptions for the meta subpackage."""

    pass


class UtilError(QuarryForgeError):
    """Base exception class for all exceptions for the util subpackage."""

    pass
