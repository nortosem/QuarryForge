"""Meta Subpackage Configuration Module.


"""
from typing import List, NamedTuple


__all__: List = []


class BuildErrorConfig(NamedTuple):
    """The meta.assembler.BuildError configuration.

    Define the default slots for all BuildError instances.
    """
    error_context: str = 'error_context'
    error_code: str = 'error_code'
    extra_details: str = 'extra_details'
    input_value: str = 'input_value'
