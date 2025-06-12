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


def attribute_modifier_type() -> AttrModTypeConfig:
    """Return configuiration for set/delete attributes."""
    return AttrModTypeConfig()


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


def error_builder() -> ErrorBuilderConfig:
    """Return configuration for assembling exception data."""
    return ErrorBuilderConfig()
