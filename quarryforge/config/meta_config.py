"""Meta Subpackage Configuration Module.


"""
from typing import List, NamedTuple

from quarryforge.config.exception_conf.exception_data import builder_config


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
    error_context: str = builder_config().error_context
    error_code: str = builder_config().error_code
    arg: str = builder_config().arg
    extra_details: str = builder_config().extra_details
    info: str = builder_config().info
    field: str = builder_config().field


def error_builder() -> ErrorBuilderConfig:
    """Return configuration for assembling exception data."""
    return ErrorBuilderConfig()
