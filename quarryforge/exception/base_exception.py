"""Exceptions Module

This module defines the custom exception hierarchy for the quarryforge package.
It includes a base exception class and specific exceptions for different
modules within the package.
"""
import datetime
from typing import Dict, Optional

from quarryforge.config import root
from quarryforge.config.exception_conf import base_exception_config as code
from quarryforge.config.exception_conf import exception_config as msg
from quarryforge.config.exception_conf.exception_data import ERROR_FIELD


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
    CODE = code.BaseErrorContext.package_error()

    def __init__(
        self,
        message: Optional[str] = None,
        code: Optional[str] = None,
        details: Optional[Dict] = None,
        user_message: Optional[str] = None
    ):
        """Initialize default exception for the QuarryForge package"""
        effective_code = code if code is not None else self.__class__.CODE

        super().__init__(message)

        self.code = effective_code
        self.details = details or {}
        self.timestamp = datetime.datetime.now(datetime.UTC).__str__()
        self.user_message = user_message or message

    def to_dict(self):
        """Returns a dictionary representation of the exception."""
        return {
            ERROR_FIELD.message: str(self),
            ERROR_FIELD.code: self.code,
            ERROR_FIELD.details: self.details,
            ERROR_FIELD.timestamp: self.timestamp.isoformat(),
            ERROR_FIELD.user_message: self.user_message,
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
        return (' ').join(parts)


class ModelError(QuarryForgeError):
    """Models Error

    Base exception class for all exceptions in the model module.
    """
    CODE = code.BaseErrorContext.default_error(
        code.BaseErrorContext.MODEL_ERROR
    )
    def __init__(
        self,
        message: Optional[str] = None,
        code: Optional[str] = None,
        details: Optional[Dict] = None,
        user_message: Optional[str] = None
    ):
        """Intialize a QuarryForge.ModelError"""
        effective_code = code if code is not None else self.__class__.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message)


class FossilError(QuarryForgeError):
    """Fossil Error

    Base exception class for all exceptions for the fossil module.
    """
    CODE = code.BaseErrorContext.default_error(
        code.BaseErrorContext.FOSSIL_ERROR
    )
    def __init__(
        self,
        message: Optional[str] = None,
        code: Optional[str] = None,
        details: Optional[Dict] = None,
        user_message: Optional[str] = None
    ):
        """Initialize the QuarryForge.FossilError"""
        effective_code = code if code is not None else self.__class__.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message)


class MainError(QuarryForgeError):
    """Main Error

    Base exception class for all exceptions in the main module.
    """
    CODE = code.BaseErrorContext.default_error(
        code.BaseErrorContext.MAIN_ERROR
    )
    def __init__(
        self,
        message: Optional[str] = None,
        code: Optional[str] = None,
        details: Optional[Dict] = None,
        user_message: Optional[str] = None
    ):
        """Initialize the QuarryForge.MainError"""
        effective_code = code if code is not None else self.__class__.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message)


class MetaError(QuarryForgeError):
    """Meta Error

    Base exception class for all exceptions for the meta module.
    """
    CODE = 'todo'

    def __init__(
        self,
        message: Optional[str] = None,
        code: Optional[str] = None,
        details: Optional[Dict] = None,
        user_message: Optional[str] = None
    ):
        """Initialize the QuarryForge.MetaError"""
        effective_code = code if code is not None else self.__class__.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message)
