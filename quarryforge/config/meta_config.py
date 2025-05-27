"""Meta Subpackage Configuration Module.


"""
from typing import List, NamedTuple


__all__: List = []


class ErrorBuilderConfig(NamedTuple):
    """The meta.assembler.BuildError configuration.

    Define the default slots for all BuildError instances.

    Attributes:
        error_context:
        error_code:
        extra_details:
        input_value:
    """
    error_context: str = 'error_context'
    error_code: str = 'error_code'
    extra_details: str = 'extra_details'
    input_value: str = 'input_value'


BUILDER_CONFIG: ErrorBuilderConfig = ErrorBuilderConfig()


class ErrorMessageBuilderConfig(NamedTuple):
    """The meta.assembler.ErrorMessageBuilder configuration.

    Define the default slots for all BuildErrorMessage instances.

    Attributes:
        error_context:
        error_code:
    """
    error_context: str = BUILDER_CONFIG.error_context
    error_code: str = BUILDER_CONFIG.error_code


MESSAGE_BUILDER_CONFIG: ErrorMessageBuilderConfig = ErrorMessageBuilderConfig()
