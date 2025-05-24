"""Assembler Module


"""
import abc
from typing import Any, Dict, List, Optional

from quarryforge.config.exception_conf import exception_data as error


class BuildError(abc.ABC):
    """Build Error Abstract Base Class."""
    __slots__ = ('error_context', 'error_code', 'input_value', 'extra_details')

    def __init__(
        self,
        *,
        error_context: str = None,
        error_code: str = None,
        input_value: Any = None,
        extra_details: Dict[str, Any] = None
    ):
        self.error_context = error_context
        self.error_code = error_code
        self.input_value = input_value
        self.extra_details = extra_details

    @abc.abstractmethod
    def code(
        self,
        error_context: Optional[str] = None,
        error_code: Optional[str] = None
    ) -> str:
        """The unique exception code for an error."""

    @abc.abstractmethod
    def message(self, arg: Optional[str]) -> str:
        """Generate and return a message for a defined exception."""

    @abc.abstractmethod
    def user_message(self, arg: Optional[str], desc: Optional[str]) -> str:
        """Generate and return a user_message for a defined exception."""

    @abc.abstractmethod
    def details(self):
        """"""

    def data(
        self,
i       input_value: Any,
        context: str,
        field: str,
        error_code: str,
        message: Optional[str] = None,
        user_message: Optional[str] = None,
        expected_desc: Optional[str] = None,
        exception_code: Optional[str] = None,
        extra_details: Optional[Dict[str, Any]] = None
    ) -> error.ValidErrorData:
        """Construct a ValidErrorData object from the provided details."""
        details = {
            BUILDER_FIELD.input_value: input_value,
            BUILDER_FIELD.context: context,
            BUILDER_FIELD.field: field,
            BUILDER_FIELD.error_code: error_code,
            BUILDER_FIELD.message: message,
            BUILDER_FIELD.user_message: user_message,
            BUILDER_FIELD.expected_desc: expected_desc
        }
        if extra_details:
            details.update(extra_details)

        usr_msg = user_message if user_message is not None else message

        return error.ValidErrorData(
            code=exception_code,
            message=message,
            user_message=usr_msg,
            details=details,
        )
