"""Exception Data Module

This module defines the data structures for holding configuration constants
and the final, validated error data used in exceptions.
"""
from typing import Any, Dict, List, NamedTuple, Optional

from quarryforge.meta import immutable as _

__all__: List[str] = [
    'error_data_config',
    'builder_config',
    'ValidErrorData'
]


class ConfigErrorData(NamedTuple):
    """Configuration for valid QuarryForge Exception Fields."""
    code: str = 'code'
    details: str = 'details'
    message: str = 'message'
    user_message: str = 'user_message'
    timestamp: str = 'timestamp'


def error_data_config() -> ConfigErrorData:
    """Returns the configuration of error data fields."""
    return ConfigErrorData()


class ConfigBuilder(NamedTuple):
    """Configuration for ErrorBuilder data fields."""
    arg: str = 'arg'
    error_code: str = 'error_code'
    error_context: str = 'error_context'
    extra_details: str = 'extra_details'
    info: str = 'info'
    field: str = 'field'
    message: str = error_data_config().message
    user_message: str = error_data_config().user_message


def builder_config() -> ConfigBuilder:
    """Returns the configuration for an ErrorBuilder."""
    return ConfigBuilder()


class ValidErrorData(_.ImmutableInstance, metaclass=_.ImmutableMetaClass):
    """An immutable data container for fully constructed exception information.
    """
    __slots__ = error_data_config()[:-1]

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
        object.__setattr__(self, error_data_config().code, code)
        object.__setattr__(self, error_data_config().message, message)
        object.__setattr__(self, error_data_config().user_message, user_message)
        object.__setattr__(self, error_data_config().details, details)


    def to_exception(self) -> Dict[str, Any]:
        """Assembles the data into a dictionary suitable for exception kwargs.
        """
        return {
            error_data_config().code: self.code,
            error_data_config().message: self.message,
            error_data_config().user_message: self.user_message,
            error_data_config().details: self.details
        }
