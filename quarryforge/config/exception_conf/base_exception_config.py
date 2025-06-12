"""Base Exception Config

The configuraiton for the exception base class of quarryforge errors.
"""
from enum import StrEnum
from typing import List, NamedTuple

from quarryforge.config import root
from quarryforge.config.exception_conf import exception_config as config
from quarryforge.meta import assembler
from quarryforge.util.decorator import validate_str_parameters


__all__: List[str] = ['BaseErrorBuilder']


@validate_str_parameters
def _build_path(suffix: str) -> str:
    """Return valid path."""
    return f'{root.Package.NAME}.{suffix}'


class BaseErrorPath(StrEnum):
    """Create Path strings for the Base Exceptions of QuarryForge

    These represent the base path contexts for different error types.
    """
    MODEL = _build_path(root.Module.MODEL)
    FOSSIL = _build_path(root.SubPackage.FOSSIL)
    MAIN = _build_path(root.Module.MAIN)
    META = _build_path(root.SubPackage.META)
    UTIL = _build_path(root.SubPackage.UTIL)


@validate_str_parameters
def get_full_error_code(context_path: str, type_suffix: str) -> str:
    """Constructs a full error code from context path and type suffix."""
    return f'{context_path}.{type_suffix}'


class BaseErrorMessageConfig(NamedTuple):
    """Base error message string configuration.

    Attributes:
        unexpected_error_code_suffix:
            The suffix used for unexpected error codes.
        unexpected_error_prefix:
            Common prefix for unexpected error messages.
        default_module_suffix:
            Suffix for messages related to modules.
        default_subpackage_suffix:
            Suffix for messages related to subpackages.
        default_package_suffix:
            Suffix for messages related to the main package.
        default_user_message:
            A generic user-friendly message.
    """
    unexpected_error_suffix: str = config.GenericError.UNEXPECTED_ERROR
    unexpected_error_prefix: str = 'An unexpected error occurred within'
    default_module_suffix: str = 'module.'
    default_subpackage_suffix: str = 'subpackage.'
    default_package_suffix: str = 'package.'
    default_user_message: str = 'An internal application error occurred.'


def base_error_message() -> BaseErrorMessageConfig:
    """Return configuration for base message error strings."""
    return BaseErrorMessageConfig()


class BaseErrorBuilder(assembler.ErrorBuilder):
    """Base implementaiton for constructing QuarryForge error data.

    This Builder orchestrates the creation of `ValidErrorData` objects for
    general QuarryForge package errors, module errors, and subpackage errors.
    """

    def code(self) -> str:
        """Generate the complete unique exception code for the error."""
        return get_full_error_code(
            self.error_context, self.error_code
        )

    def _type_message(self) -> str:
        """Generates a message for type errors."""
        info = self.info or config.DescMsg.UNKNOWN
        return (
            f'{self._base_message()} Expected type: {info}. Got '
            f'type {type(self.arg).__name__} with value {self.arg!r} instead.'
        )

    def _value_message(self) -> str:
        """Generates a message for value errors."""
        info = self.info or config.DescMsg.UNKNOWN
        return (
            f'{self._base_message()} Value {self.arg!r} is invalid. '
            f'Expected value: {info}.'
        )

    def _invalid_state_message(self) -> str:
        """Generates a message for invalid state errors.

        Exceptions for invalid states require an action and current_state.
        (e.g. use the extra_details dictionary: extra_details['action'] = ...)
        """
        details = self.extra_details or {}
        action = details.get('action', 'an operation')
        current_state = details.get(
            'current_state', f'an {config.DescMsg.UNKNOWN} state'
        )
        return (
            f'{self._base_message()} Attempted {action} in {current_state}. '
            f'This state is invalid for this operation.'
        )

    def _config_message(self) -> str:
        """Generates a message for configuration errors.

        Exceptions for configuration require a configuration value & reason.
        (e.g. use the extra_details dictionary: extra_details['action'] = ...)
        """
        details = self.extra_details or {}
        config_key =  details.get('config_key', 'required configuration')
        reason = details.get(
            config.DescMsg.REASON,
            f'with {config.DescMsg.UNKNOWN} {config.DescMsg.REASON}'
        )
        return (
            f'{self._base_message()} Missing or invalid configuration for '
            f'{config_key}. Reason: {reason}.'
        )

    def _dependency_message(self) -> str:
        """Generates a message for external dependency errors.

        Exceptions for dependency errors require a dependency and reason.
        (e.g. use the extra_details dictionary: extra_details['action'] = ...)
        """
        details = self.extra_details or {}
        dependency = details.get(
            config.DescMsg.DEPENDENCY,
            f'{config.DescMsg.UNKNOWN} {config.DescMsg.DEPENDENCY}'
        )
        reason = details.get(
            config.DescMsg.REASON,
            f'{config.DescMsg.UNKNOWN} {config.DescMsg.REASON}'
        )
        return (
            f'{self._base_message()} `{dependency}` failed due to: {reason}.'
        )

    def _not_implemented_message(self) -> str:
        """Generates a message for not implemented errors."""
        info = self.info or f'{config.DescMsg.UNKNOWN} feature'
        return f'{self._base_message()} {info} is not implemented.'

    def _unexpected_message(self) -> str:
        """Generates a message for unexpected errors."""
        context = self.error_context.split('.')
        cfg = base_error_message()

        if len(context) == 1 and context[0] == root.Package.NAME:
            suffix = cfg.default_package_suffix
        elif (
            len(context) > 1 and
            context[0] == root.Package.NAME and
            context[1] in root.SubPackage.__members__
        ):
            suffix = cfg.default_subpackage_suffix
        else:
            suffix = cfg.default_module_suffix

        return (
            f'{cfg.unexpected_error_prefix} `{self.error_context}` {suffix}'
        )

    def message(self) -> str:
        """Builds a detailed, technical error message for base exceptions.

        Returns:
            A string representing the detailed error message.
        """
        match self.error_code:
            case config.GenericError.TYPE_ERROR:
                return self._type_message()

            case config.GenericError.VALUE_ERROR:
                return self._value_message()

            case config.GenericError.INVALID_STATE_ERROR:
                return self._invalid_state_message()

            case config.GenericError.CONFIGURATION_ERROR:
                return self._config_message()

            case config.GenericError.EXTERNAL_DEPENDENCY_ERROR:
                return self._dependency_message()

            case config.GenericError.NOT_IMPLEMENTED_ERROR:
                return self._not_implemented_message()

            case config.GenericError.UNEXPECTED_ERROR:
                return self._unexpected_message()

            case _:
                return (
                    f'{self._base_message()} Error code {self.error_code} '
                    f'unhandled {config.DescMsg.IS_AN_UNEXPECTED_ERROR}.'
                )


    def user_message(self) -> str:
        """Builds a user-friendly error message for base exceptions.

        This method provides user-friendly messages for `GenericError` types,
        falling back to a general internal error message.

        Returns:
            A string representing the user-friendly error message.
        """
        cfg = base_error_message()

        match self.error_code:
            case config.GenericError.TYPE_ERROR:
                return (
                    'An input was provided in an incorrect format.'
                )

            case config.GenericError.VALUE_ERROR:
                return (
                    'An input value is not valid for this operation.'
                )

            case config.GenericError.INVALID_STATE_ERROR:
                return (
                    'An operation attempted in an invalid application state.'
                )

            case config.GenericError.CONFIGURATION_ERROR:
                return 'There is an issue with the configuration.'

            case config.GenericError.EXTERNAL_DEPENDENCY_ERROR:
                return (
                    'An required tool or service encountered an issue.'
                )

            case config.GenericError.NOT_IMPLEMENTED_ERROR:
                return 'This feature is not available.'

            case config.GenericError.UNEXPECTED_ERROR:
                return cfg.default_user_message

            case _:
                return cfg.default_user_message
