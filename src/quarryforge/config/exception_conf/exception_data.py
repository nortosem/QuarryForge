"""Defines the data structures valid error data.

These structure hold configuration constants and the final, validated error
data used in exceptions.
"""

from typing import Any, NamedTuple

from quarryforge.meta import immutable as _

__all__: list[str] = ['error_data_config', 'builder_config', 'ValidErrorData']


class ConfigErrorData(NamedTuple):
    """Configuration for valid QuarryForge Exception Fields."""

    code: str = 'code'
    details: str = 'details'
    message: str = 'message'
    user_message: str = 'user_message'
    timestamp: str = 'timestamp'


def error_data_config() -> ConfigErrorData:
    """Return the configuration of error data fields."""
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
    """Return the configuration for an ErrorBuilder."""
    return ConfigBuilder()


class ValidErrorData(_.ImmutableInstance, metaclass=_.ImmutableMetaClass):
    """Immutable data container for fully constructed exception information."""

    __slots__ = error_data_config()[:-1]

    code: str | None
    message: str | None
    user_message: str | None
    details: dict[str, Any] | None

    def __init__(
        self,
        *,
        code: str | None = None,
        message: str | None = None,
        user_message: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        object.__setattr__(self, error_data_config().code, code)
        object.__setattr__(self, error_data_config().message, message)
        object.__setattr__(self, error_data_config().user_message, user_message)
        object.__setattr__(self, error_data_config().details, details)

    def to_exception(self) -> dict[str, Any]:
        """Assemble the data into a dictionary suitable for exception kwargs."""
        return {
            error_data_config().code: self.code,
            error_data_config().message: self.message,
            error_data_config().user_message: self.user_message,
            error_data_config().details: self.details,
        }
