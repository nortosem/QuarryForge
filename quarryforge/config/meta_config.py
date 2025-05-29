"""Meta Subpackage Configuration Module.


"""
from typing import List, NamedTuple


__all__: List = []


class ErrorBuilderConfig(NamedTuple):
    """The meta.assembler.BuildError configuration.

    Define the default slots for all BuildError instances.
    """
    error_context: str = 'error_context'
    error_code: str = 'error_code'
    arg: str = 'arg'
    extra_details: str = 'extra_details'
    expected_type: str = 'expected_type'
    field: str = 'field'


BUILDER_CONFIG: ErrorBuilderConfig = ErrorBuilderConfig()


class ErrorMessageBuilderConfig(NamedTuple):
    """The meta.assembler.ErrorMessageBuilder configuration.

    Define the default slots for all BuildErrorMessage instances.
    """
    error_context: str = BUILDER_CONFIG.error_context
    error_code: str = BUILDER_CONFIG.error_code
    arg: str = BUILDER_CONFIG.arg
    expected_type: str = BUILDER_CONFIG.expected_type
    field: str = BUILDER_CONFIG.field


MESSAGE_BUILDER_CONFIG: ErrorMessageBuilderConfig = ErrorMessageBuilderConfig()
