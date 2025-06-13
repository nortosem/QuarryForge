"""Assembler Module

This module provides abstract base classes and utility functions for
constructing structured error messages and comprehensive error data objects.
"""
import abc
from typing import Any, Dict, List, Optional, Tuple

from quarryforge.config import meta_config
from quarryforge.config.exception_conf import exception_config as config
from quarryforge.config.exception_conf import exception_data as error


__all__: List[str] = ['ErrorBuilder']


def _valid_str_type(value: str) -> str:
    """Validates if the input value is a string.

    Args:
        value: The value to check.

    Returns:
        The original value if it is a string.

    Raises:
        TypeError: If the value is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(
            f'{value!r} {config.DescMsg.MUST_BE}'
            f' {config.DescMsg.A_VALID_STRING}'
        )
    return value


def _valid_str_value(value: str) -> str:
    """Validates if the input string value is non-empty.

    Args:
        value: The string value to check.

    Returns:
        The original value if it is a non-empty string.

    Raises:
        ValueError: If the value is an empty string.
    """
    if not value:
        raise ValueError(
            f'{value!r} {config.DescMsg.MUST_BE}'
            f' {config.DescMsg.A_NON_EMPTY_STRING}'
        )
    return value


def _validate_init(context_value: Any,
                   code_value: Any,
                   field_value: Any = None,
                   info_value: Any = None
                   ) -> Tuple[str, str, str | None, str | None]:
    """Applies type and non-empty validation to two string values.

    This helper is used in __init__ methods for common string arguments.

    Args:
        context_value: The first string value (e.g., error context).
        code_value: The second string value (e.g., error type or code).
        field: The specific field name related to the error (optional).
        info_value: error specific info hints (optional)
        (e.g., 'str', 'int', 'Path', 'action: state etc.').
    Returns:
        A tuple containing the validated context_value and type_value.

    Raises:
        TypeError: If either value is not a string.
        ValueError: If either value is an empty string.
    """
    context_value = _valid_str_value(_valid_str_type(context_value))
    code_value = _valid_str_value(_valid_str_type(code_value))

    if field_value:
        field_value = _valid_str_value(_valid_str_type(field_value))

    if info_value:
        info_value = _valid_str_value(
            _valid_str_type(info_value))

    return (context_value, code_value, field_value, info_value)


class ErrorBuilder(abc.ABC):
    """Build Error Abstract Base Class.

    This ABC provides a structured way to construct comprehensive error
    data objects (`ValidErrorData`). It combines error context, code,
    arg values, and additional details into a single, consistent format.

    Attributes:
        error_context (str): The package path context for the error.
        error_code (str): The unique error code identifier.
        arg (Optional[Any]):
            The argument value associated with the error.
        extra_details (Optional[Dict[str, Any]]):
            A dictionary for additional error details.
        info (str): The error info associated with an error.
        field (str): The class field or attribute affected by the error.
    """
    __slots__ = meta_config.error_builder().slots()

    def __init__(self,
                 *,
                 error_context: str,
                 error_code: str,
                 arg: Optional[Any] = None,
                 field: Optional[str] = None,
                 info: Optional[str] = None,
                 extra_details: Optional[Dict[str, Any]] = None):
        """Default exception constructor initialization.

        Args:
            error_context: The package path context for the error.
            error_code: The specific type or code of the error.
            arg: The argument/value that caused the error (optional).
            field: The specific field name related to the error (optional).
            info: The name of the type (e.g., 'str', 'int', 'Path')
            extra_details:
                A dictionary of additional context or details for the error
                (optional).

        Raises:
            TypeError: If error_context or error_code are not strings.
            ValueError: If error_context or error_code are empty strings.
        """
        self.arg = arg

        error_context, error_code, field, info = _validate_init(
            error_context,
            error_code,
            field,
            info
        )
        self.error_context = error_context
        self.error_code = error_code
        self.field = field
        self.info = info

        if extra_details:
            if not isinstance(extra_details, dict):
                raise TypeError(
                    f'{extra_details!r} {config.DescMsg.MUST_BE}'
                    f' {config.DescMsg.dictionary}'
                )
        self.extra_details = extra_details

    @abc.abstractmethod
    def code(self) -> str:
        """Abstract method to get the unique exception code for an error.

        Subclasses must implement this method to construct the full error
        code, often by combining context and type.

        Returns:
            The unique exception code as a string.
        """
        pass

    @abc.abstractmethod
    def message(self) -> str:
        """Abstract method to build a detailed, technical error message.

        Returns:
        A string representing the detailed error message
        """
        pass

    @abc.abstractmethod
    def user_message(self) -> str:
        """Abstract method to build a user-friendly error message.

        Returns:
        A string representing the user-friendly error message.
        """
        pass

    def _base_message(self) -> str:
        """Generates a common error message prefix.

        This provides a consistent header for all technical error messages.
        """
        return (
            f'Error in `{self.error_context}` (Code: {self.error_code}).'
        )

    def details(self) -> Dict[str, Any]:
        """Abstract method to generate and return specific error details.

        Subclasses must implement this method to provide a dictionary of
        additional details relevant to the error.

        Returns:
            A dictionary containing specific error details.
        """

        details = {
            error.builder_config().error_context: self.error_context,
            error.builder_config().error_code: self.error_code,
            error.builder_config().message: self.message(),
            error.builder_config().user_message: self.user_message(),
        }
        if self.arg:
            details[error.builder_config().arg] = self.arg
        if self.field:
            details[error.builder_config().field] = self.field
        if self.info:
            details[error.builder_config().info] = self.info
        if self.extra_details:
            details.update(self.extra_details)

        return details

    def data(self) -> error.ValidErrorData:
        """Constructs a ValidErrorData object from the provided details.

        This method combines the instance's inherent error context, code,
        and arg with additional parameters to form a comprehensive
        error data structure. It prioritizes explicit parameters over
        instance attributes when both are provided.

        Returns:
            A `quarryforge.config.exception_conf.exception_data.ValidErrorData`
            object containing the structured error information.
        """
        code = self.code()
        details = self.details()

        return error.ValidErrorData(
            code=code,
            message=details[error.builder_config().message],
            user_message=details[error.builder_config().user_message],
            details=details,
        )
