"""Exception Data Module


"""
from typing import Any, Dict, NamedTuple

from quarryforge.config.exception_conf import exception_config as error


class ConfigErrorData(NamedTuple):
    """Valid QuarryForge Exception Fields"""
    code: str = 'code'
    details: str = 'details'
    message: str = 'message'
    user_message: str = 'user_message'
    timestamp: str = 'timestamp'


ERROR_DATA: ConfigErrorData = ConfigErrorData()
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


ERROR_DATA_CONFIG: ConfigBuilder = ConfigBuilder()
"""Global constant for BuildError data fields."""


class ValidErrorData(NamedTuple):
    """Data container for exception information"""
    code: str
    message: str
    user_message: str
    details: Dict[str, Any]

    @classmethod
    def to_exception(cls) -> Dict[str, Any]:
        """Assemble to convert keyword args for a QuarryForge exception."""
        return {
            ERROR_DATA.code: cls.code,
            ERROR_DATA.message: cls.message,
            ERROR_DATA.user_message: cls.user_message,
            ERROR_DATA.details: cls.details
        }
