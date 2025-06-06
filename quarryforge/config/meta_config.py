"""Meta Subpackage Configuration Module.


"""
from typing import List, NamedTuple

from quarryforge.config.exception_conf.exception_data import BUILDER_FIELD


__all__: List[str] = []


class AttrModTypeConfig(NamedTuple):
    """Types of attribute modifications.

    Define the types of immutable modifications.
    """
    set_attribute: str = 'set attribute'
    delete_attribute: str = 'delete attribute'


MOD_TYPE: AttrModTypeConfig = AttrModTypeConfig()


class ErrorBuilderConfig(NamedTuple):
    """The meta.assembler.BuildError configuration.

    Define the default slots for all BuildError instances.
    """
    error_context: str = BUILDER_FIELD.error_context
    error_code: str = BUILDER_FIELD.error_code
    arg: str = BUILDER_FIELD.arg
    extra_details: str = BUILDER_FIELD.extra_details
    info: str = BUILDER_FIELD.info
    field: str = BUILDER_FIELD.field


BUILDER_CONFIG: ErrorBuilderConfig = ErrorBuilderConfig()
