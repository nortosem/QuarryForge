"""Assembler Module


"""
import abc
from typing import Any, Dict, Optional, Tuple

from quarryforge.config import meta_config
from quarryforge.config.exception_conf import exception_config as config
from quarryforge.config.exception_conf import exception_data as error


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
            f'{value!r} {config.DESC_TYPE.must_be}'
            f' {config.DESC_TYPE.string}'
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
            f'{value!r} {config.DESC_TYPE.must_be}'
            f' {config.DESC_TYPE.unempty}'
        )
    return value


def _validate_init(context_value: str, type_value: str) -> Tuple[str, str]:
    """Applies type and non-empty validation to two string values.

    This helper is used in __init__ methods for common string arguments.

    Args:
        context_value: The first string value (e.g., error context).
        type_value: The second string value (e.g., error type or code).

    Returns:
        A tuple containing the validated context_value and type_value.

    Raises:
        TypeError: If either value is not a string.
        ValueError: If either value is an empty string.
    """
    context_value = _valid_str_type(_valid_str_value(context_value))
    type_value = _valid_str_type(_valid_str_value(type_value))
    return context_value, type_value


class ErrorMessageBuilder(abc.ABC):
    """Build error message Abstract Base Class.

    This ABC provides a common interface for constructing various error
    messages (e.g., detailed technical messages, user-friendly messages).
    It ensures consistency in how error messages are generated based on
    context and type.

    Attributes:
        error_context (str): The package path context for an error
            (e.g., 'quarryforge.core.module').
        error_code (str): The error code type suffix for an error
            (e.g., 'TYPE_ERROR', 'VALUE_ERROR').
    """
    __slots__ = meta_config.MESSAGE_BUILDER_CONFIG._fields

    def __init__(
        self,
        error_context: str,
        error_code: str,
    ):
        """Initialize an error message builder with error information.

        Args:
            error_context: The package path context for the error.
            error_code: The specific type or code of the error.

        Raises:
            TypeError: If error_context or error_type are not strings.
            ValueError: If error_context or error_type are empty strings.
        """
        self.error_context, self.error_code = _validate_init(
            error_context, error_code
        )

    def prefix_message(self, input_value: Optional[Any]) -> str:
        """Generates a common error message prefix.

        This prefix typically includes the error type and context, and
        optionally the input value that caused the error.

        Args:
            input_value: The argument value associated with an error,
                if applicable. Can be of any type.

        Returns:
            A detailed error message common for most exceptions.
        """
        message = f'{self.error_code} in `{self.error_context}`'
        value = f' for the input: {input_value!r}' if input_value else ''
        return message+value


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


class ErrorBuilder(abc.ABC):
    """Build Error Abstract Base Class.

    This ABC provides a structured way to construct comprehensive error
    data objects (`ValidErrorData`). It combines error context, code,
    input values, and additional details into a single, consistent format.

    Attributes:
        error_context (str): The package path context for the error.
        error_code (str): The unique error code identifier.
        input_value (Optional[Any]):
            The argument value associated with the error.
        extra_details (Optional[Dict[str, Any]]):
            A dictionary for additional error details.
    """
    __slots__ = meta_config.BUILDER_CONFIG._fields

    def __init__(
        self,
        *,
        error_context: str,
        error_code: str,
        input_value: Optional[Any] = None,
        extra_details: Optional[Dict[str, Any]] = None
    ):
        """Default exception constructor initialization.

        Args:
            error_context: The package path context where the error occurred.
            error_code: The unique identifier for this specific error type.
            input_value: The value that caused the error (optional).
            extra_details:
                A dictionary of additional context or details for the error
                (optional).

        Raises:
            TypeError: If error_context or error_code are not strings.
            ValueError: If error_context or error_code are empty strings.
        """
        self.error_context, self.error_code = _validate_init(
            error_context, error_code
        )
        self.input_value = input_value
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
    def details(self) -> Dict[str, Any]:
        """Abstract method to generate and return specific error details.

        Subclasses must implement this method to provide a dictionary of
        additional details relevant to the error.

        Returns:
            A dictionary containing specific error details.
        """
        pass

    def data(
        self,
        *,
        field: Optional[str] = None,
        context: Optional[str] = None,
        error_code: Optional[str] = None,
        message_builder: Optional[ErrorMessageBuilder] = None,
        input_value: Optional[Any] = None,
        extra_details: Optional[Dict[str, Any]] = None
    ) -> error.ValidErrorData:
        """Constructs a ValidErrorData object from the provided details.

        This method combines the instance's inherent error context, code,
        and input value with additional parameters to form a comprehensive
        error data structure. It prioritizes explicit parameters over
        instance attributes when both are provided.

        Args:
            field: An optional string identifying the specific field related to
                the error.
            context: An optional string overriding the instance's error
                context.
            error_code: An optional string overriding the instance's error
                code.
            message: An optional ErrorMessageBuilder instance for the detailed
                error message.
                If None, the message attribute of ValidErrorData will be None.
            user_message: An optional ErrorMessageBuilder instance for the
                user-friendly message.
                If None, it defaults to the 'message' parameter.
            input_value: An optional value associated with the error,
                overriding instance's input_value.
        extra_details: An optional dictionary for additional key-value details.

        Returns:
            A `quarryforge.config.exception_conf.exception_data.ValidErrorData`
            object containing the structured error information.
        """
        message_str = None
        user_message_str = None

        if message_builder:
            if message_builder.message():
                message_str = message_builder.message()

            if message_builder.user_message():
                user_message_str = message_builder.user_message()
            elif message_builder.message():
                user_message_str = message_builder.message()

        final_error_code = (
            self.error_code if error_code is None else error_code
        )
        details = {
            error.BUILDER_FIELD.input_value: (
                self.input_value if input_value is None else input_value),
            error.BUILDER_FIELD.context: (
                self.error_context if context is None else context),
            error.BUILDER_FIELD.error_code: final_error_code,
            error.BUILDER_FIELD.message: message_str,
            error.BUILDER_FIELD.user_message: user_message_str,
        }
        if field:
            details[error.BUILDER_FIELD.field] = field

        if extra_details:
            details.update(extra_details)


        return error.ValidErrorData(
            error_code=final_error_code,
            message=message_str,
            user_message=user_message_str,
            details=details,
        )
