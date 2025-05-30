"""Exceptions Module

This module defines the custom exception hierarchy for the quarryforge package.
It includes a base exception class and specific exceptions for different
modules & subpackages within the QuarryForge package.
"""
import datetime
from typing import Any, Dict, Optional

from quarryforge.config.exception_conf import exception_data as _


class QuarryForgeError(Exception):
    """Base Exception Class for quarryforge

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
    def __init__(self,
                 message: str,
                 code: str,
                 user_message: str,
                 details: Optional[Dict[str, Any]] = None):
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

    def to_dict(self) -> Dict[str, Any]:
        """Returns a dictionary representation of the exception."""
        return {
            _.ERROR_FIELD.message: str(self),
            _.ERROR_FIELD.code: self.code,
            _.ERROR_FIELD.details: self.details,
            _.ERROR_FIELD.timestamp: self.timestamp.isoformat(),
            _.ERROR_FIELD.user_message: self.user_message,
        }

    def __str__(self) -> str:
        """Returns a formatted string representation of the exception."""
        message = super().__str__()
        parts = []
        if self.code:
            parts.append(f'[{self.code}]')
        if message:
            parts.append(message)

        if self.details:
            filtered_details = {}
            for key, value in self.details.items():
                if key not in [_.ERROR_FIELD.code,
                    _.ERROR_FIELD.message,
                    _.ERROR_FIELD.user_message
                ]:
                    filtered_details[key] = value

            if filtered_details:
                detail_str = ', '.join(
                    [f'{key}: {value}' for key, value in (
                        filtered_details.items()
                    )]
                )
                parts.append(f'({detail_str})')
        return (' ').join(parts)


class ModelError(QuarryForgeError):
    """Models Error

    Base exception class for all exceptions in the model module.
    """
    pass


class FossilError(QuarryForgeError):
    """Fossil Error

    Base exception class for all exceptions for the fossil module.
    """
    pass


class MainError(QuarryForgeError):
    """Main Error

    Base exception class for all exceptions in the main module.
    """
    pass


class MetaError(QuarryForgeError):
    """Meta Error

    Base exception class for all exceptions for the meta subpackage.
    """
    pass


class UtilError(QuarryForgeError):
    """Meta Error

    Base exception class for all exceptions for the util subpackage.
    """
    pass
