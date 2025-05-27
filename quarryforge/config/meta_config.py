"""Meta Subpackage Configuration Module.


"""
from typing import List, NamedTuple


__all__: List = []


class BuildErrorConfig(NamedTuple):
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


class ErrorMessageBuilder(NamedTuple):
    """The meta.assembler.ErrorMessageBuilder configuration.

    Define the default slots for all BuildErrorMessage instances.

    Attributes:
        error_types: The error types that messages are built for.
    """
    error_types: str = 'error_types'
