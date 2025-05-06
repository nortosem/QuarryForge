"""Exceptions Module

This module defines the custom exception hierarchy for the quarryforge package.
It includes a base exception class and specific exceptions for different
modules within the package.
"""
import datetime
from typing import Dict, Optional

from quarryforge.config import root
from quarryforge.config.exception_conf import message as Message

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
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):
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


class ModelError(QuarryForgeError):
    """Models Error

    Base exception class for all exceptions in the model module.
    """
    DEFAULT_CODE = root.TopModules.MODEL.value + Message.Default.ERROR.value

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.DEFAULT_CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message)


class FossilError(QuarryForgeError):
    """Fossil Error

    Base exception class for all exceptions in the fossil module.
    """
    DEFAULT_CODE = root.TopModules.FOSSIL.value + Message.Default.ERROR.value

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.DEFAULT_CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message)


class MainError(QuarryForgeError):
    """Main Error

    Base exception class for all exceptions in the main module.
    """
    DEFAULT_CODE = root.TopModules.MAIN.value + Message.Default.ERROR.value

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.DEFAULT_CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message)
