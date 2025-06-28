"""Meta Exception Configuration for meta_error exceptions."""

from enum import StrEnum, auto
from typing import NamedTuple

from quarryforge.config import root
from quarryforge.config.exception_conf import base_exception_config as base_conf
from quarryforge.config.exception_conf import exception_config as exc_conf

__all__ = ['MetaErrorBuilder']


class MetaErrorCode(exc_conf.ValidName):
    """Specific error codes for meta-related errors."""

    ASSEMBLER_ERROR = auto()
    IMMUTABILITY_VIOLATION = auto()


class MetaErrorMessages(NamedTuple):
    """User-facing message templates or parts for meta errors."""

    immutable_violation_user: str = 'Attempted to modify an immutable object.'
    assembler_error_user: str = (
        'A fatal error occured while assembling an error message.'
    )
    default_meta_user: str = 'An error occurred in the meta subpackage.'


def meta_error_message() -> MetaErrorMessages:
    """Return a default meta error message."""
    return MetaErrorMessages()


class MetaErrorPath(StrEnum):
    """Defines error context paths for meta-related exceptions."""

    META_ROOT_CONTEXT = base_conf.build_path(root.SubPackage.META)
    IMMUTABLE_CONTEXT = base_conf.get_full_error_code(
        META_ROOT_CONTEXT, root.MetaModule.IMMUTABLE
    )
    ASSEMBLER_CONTEXT = base_conf.get_full_error_code(
        META_ROOT_CONTEXT, root.MetaModule.ASSEMBLER
    )
    IMMUTABLE_NAMESPACE = base_conf.get_full_error_code(
        IMMUTABLE_CONTEXT, 'Namespace'
    )
    IMMUTABLE_INSTANCE = base_conf.get_full_error_code(
        IMMUTABLE_CONTEXT, 'Instance'
    )


class MetaErrorBuilder(base_conf.BaseErrorBuilder):
    """Build error data for meta-subpackage exceptions.

    Types of errors:
        assembler errors
        immutability errors.
    """

    def _immutable_error_message(self) -> str:
        """Generate a message for `meta.immutable.ImmutableError`.

        - self.arg should be the object (class or instance) being modified.
        - self.field should be the attribute name.
        - self.info can describe the operation
            (e.g., "set attribute", "delete attribute").
        """
        base_msg: str = self._base_message()
        obj_name = ''
        if self.arg:
            try:
                obj_name = (
                    self.arg.__name__
                    if isinstance(self.arg, type)
                    else type(self.arg).__name__
                )
            except AttributeError:
                obj_name = str(self.arg)
        else:
            obj_name = 'the target object'

        operation_desc = self.info or 'modify'
        attribute_name = (
            f'attribute: {self.field}' if self.field else 'an attribute'
        )

        return (
            f'{base_msg} Cannot {operation_desc.lower()} on immutable object '
            f'"{obj_name}". Attempted to modify {attribute_name}.'
        )

    def _assembler_error_message(self) -> str:
        """Generate a message for meta.assembler.ErrorBuilder errors."""
        base_msg: str = self._base_message()
        reason = self.info or 'an unspecified issue'
        return (
            f'{base_msg} Error builder assembly failure: {reason}. '
            f'Issue with field: {self.field or exc_conf.DescMsg.UNKNOWN}.'
        )

    def message(self) -> str:
        """Build a detailed, technical error message."""
        match self.error_code:
            case MetaErrorCode.IMMUTABILITY_VIOLATION:
                return self._immutable_error_message()
            case MetaErrorCode.ASSEMBLER_ERROR:
                return self._assembler_error_message()
            case _:
                return super().message()

    def user_message(self) -> str:
        """Build a user-friendly error message."""
        match self.error_code:
            case MetaErrorCode.IMMUTABILITY_VIOLATION:
                return meta_error_message().immutable_violation_user
            case MetaErrorCode.ASSEMBLER_ERROR:
                return meta_error_message().assembler_error_user
            case _ if self.error_code in exc_conf.GenericError:
                return super().user_message()
            case _:
                return meta_error_message().default_meta_user
