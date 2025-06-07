"""Exception Data Module

This module defines the data structures for holding configuration constants
and the final, validated error data used in exceptions.
"""
from typing import Any, Dict, List, NamedTuple, Optional

from quarryforge.meta import immutable as _

__all__: List[str] = ['ERROR_FIELD', 'BUILDER_FIELD', 'ValidErrorData']


class ConfigErrorData(NamedTuple):
    """Configuration for valid QuarryForge Exception Fields."""
    code: str = 'code'
    details: str = 'details'
    message: str = 'message'
    user_message: str = 'user_message'
    timestamp: str = 'timestamp'


ERROR_FIELD: ConfigErrorData = ConfigErrorData()
"""Global constant for quarryforge exception fields."""


class ConfigBuilder(NamedTuple):
    """Configuration for ErrorBuilder data fields."""
    arg: str = 'arg'
    error_code: str = 'error_code'
    error_context: str = 'error_context'
    extra_details: str = 'extra_details'
    info: str = 'info'
    field: str = 'field'
    message: str = ERROR_FIELD.message
    user_message: str = ERROR_FIELD.user_message


BUILDER_FIELD: ConfigBuilder = ConfigBuilder()
"""Global constant for BuildError data fields."""


class ValidErrorData(_.ImmutableInstance, metaclass=_.ImmutableMetaClass):
    """An immutable data container for fully constructed exception information."""
    __slots__ = ERROR_FIELD._fields[:-1]

    code: Optional[str]
    message: Optional[str]
    user_message: Optional[str]
    details: Optional[Dict[str, Any]]

    def __init__(self,
        *,
        code: Optional[str] = None,
        message: Optional[str] = None,
        user_message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        object.__setattr__(self, ERROR_FIELD.code, code)
        object.__setattr__(self, ERROR_FIELD.message, message)
        object.__setattr__(self, ERROR_FIELD.user_message, user_message)
        object.__setattr__(self, ERROR_FIELD.details, details)


    def to_exception(self) -> Dict[str, Any]:
        """Assembles the data into a dictionary suitable for exception kwargs."""
        return {
            ERROR_FIELD.code: self.code,
            ERROR_FIELD.message: self.message,
            ERROR_FIELD.user_message: self.user_message,
            ERROR_FIELD.details: self.details
        }
