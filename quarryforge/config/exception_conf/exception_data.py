"""Exception Data Module


"""
from typing import Any, Dict, NamedTuple

from quarryforge.config.exception_conf import exception_config as error


__all__: list = ['ERROR_FIELD', 'BUILDER_FIELD', 'ValidErrorData']


class ConfigErrorData(NamedTuple):
    """Valid QuarryForge Exception Fields"""
    code: str = 'code'
    details: str = 'details'
    message: str = 'message'
    user_message: str = 'user_message'
    timestamp: str = 'timestamp'


ERROR_FIELD: ConfigErrorData = ConfigErrorData()
"""Global constant for quarryforge exception fields."""


class ConfigBuilder(NamedTuple):
    """BuildError Data fields"""
    context: str = 'context'
    field: str = 'field'
    error_type: str = 'error_type'
    message: str = 'message'
    user_message: str = 'user_message'
    input_value: str = 'input_value'
    expected_desc: str = 'expected_desc'
    extra_details: str = 'extra_details'


BUILDER_FIELD: ConfigBuilder = ConfigBuilder()
"""Global constant for BuildError data fields."""


class ValidErrorData(NamedTuple):
    """Data container for exception information"""
    code: str
    message: str
    user_message: str
    details: Dict[str, Any]

    def to_exception(self) -> Dict[str, Any]:
        """Assemble to convert keyword args for a QuarryForge exception."""
        return {
            ERROR_FIELD.code: self.code,
            ERROR_FIELD.message: self.message,
            ERROR_FIELD.user_message: self.user_message,
            ERROR_FIELD.details: self.details
        }
