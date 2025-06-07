"""Base Exception Config

The configuraiton for the exception base class of quarryforge errors.
"""
from typing import List, NamedTuple

from quarryforge.config import root
from quarryforge.config.exception_conf import exception_config as config
from quarryforge.meta import assembler
from quarryforge.meta import immutable
from quarryforge.util.decorator import validate_str_parameters


__all__: List[str] = ['BaseErrorBuilder']


class BaseConfig(metaclass=immutable.Namespace):
    """Base Config

    Define default path for all base exceptions.
    """
    PACKAGE: str = root.PACKAGE.name

    @staticmethod
    @validate_str_parameters
    def path(name: str) -> str:
        """Return valid path."""
        return f'{BaseConfig.PACKAGE}.{name}'


class BaseErrorPath(metaclass=immutable.Namespace):
    """Create Path strings for the Base Exceptions of QuarryForge

    These represent the base path contexts for different error types.
    """
    MODEL: str = BaseConfig.path(root.MODULE.model)
    FOSSIL: str = BaseConfig.path(root.MODULE.fossil)
    MAIN: str = BaseConfig.path(root.MODULE.main)
    META: str = BaseConfig.path(root.SUB_PACKAGE.meta)
    UTIL: str = BaseConfig.path(root.SUB_PACKAGE.util)

    @staticmethod
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
    unexpected_error_suffix: str = config.GENERIC_ERROR.unexpected_error
    unexpected_error_prefix: str = 'An unexpected error occurred within'
    default_module_suffix: str = 'module.'
    default_subpackage_suffix: str = 'subpackage.'
    default_package_suffix: str = 'package.'
    default_user_message: str = 'An internal application error occurred.'


BASE_ERROR_MSG: BaseErrorMessageConfig = BaseErrorMessageConfig()


class BaseErrorBuilder(assembler.ErrorBuilder):
    """Base implementaiton for constructing QuarryForge error data.

    This Builder orchestrates the creation of `ValidErrorData` objects for
    general QuarryForge package errors, module errors, and subpackage errors.
    """

    def code(self) -> str:
        """Generate the complete unique exception code for the error.

        Combines the full path context for the error with an error code.

        Returns:
            The full error code string for an exception.
        """
        return BaseErrorPath.get_full_error_code(
            self.error_context, self.error_code
        )

    def _type_message(self) -> str:
        """Generates a message for type errors."""
        info = self.info or config.DESC_MSG.unknown
        return (
            f'{self._base_message()} Expected type: {info}. Got '
            f'type {type(self.arg).__name__} with value {self.arg!r} instead.'
        )

    def _value_message(self) -> str:
        """Generates a message for value errors."""
        info = self.info or config.DESC_MSG.unknown
        return (
            f'{self._base_message()} Value {self.arg!r} is invalid. '
            f'Expected value: {info}.'
        )

    def _invalid_state_message(self) -> str:
        """Generates a message for invalid state errors.

        Exceptions for invalid states require an action and current_state.
        (e.g. use the extra_details dictionary: extra_details['action'] = ...)
        """
        action = 'an operation'
        current_state = f'an {config.DESC_MSG.unknown} state'

        if self.extra_details:
            action = str(self.extra_details.get('action'))
            current_state = str(self.extra_details.get('current_state'))

        return (
            f'{self._base_message()} Attempted {action} in {current_state}. '
            f'This state is invalid for this operation.'
        )

    def _config_message(self) -> str:
        """Generates a message for configuration errors.

        Exceptions for configuration require a configuration value & reason.
        (e.g. use the extra_details dictionary: extra_details['action'] = ...)
        """
        config_key = 'required configuration'
        reason = f'with {config.DESC_MSG.unknown} {config.DESC_MSG.reason}'

        if self.extra_details:
            config_key = str(self.extra_details.get('config_key'))
            reason = str(self.extra_details.get(config.DESC_MSG.reason))

        return (
            f'{self._base_message()} Missing or invalid configuration for '
            f'{config_key} {reason}.'
        )

    def _dependency_message(self) -> str:
        """Generates a message for external dependency errors.

        Exceptions for dependency errors require a dependency and reason.
        (e.g. use the extra_details dictionary: extra_details['action'] = ...)
        """
        dependency = (
            f'{config.DESC_MSG.unknown} {config.DESC_MSG.dependency}')
        reason = f'{config.DESC_MSG.unknown} {config.DESC_MSG.reason}'

        if self.extra_details:
            dependency = self.extra_details[config.DESC_MSG.dependency]
            reason = self.extra_details[config.DESC_MSG.reason]
        return (
            f'{self._base_message()} `{dependency}` failed due to: {reason}.'
        )

    def _not_implemented_message(self) -> str:
        """Generates a message for not implemented errors."""
        info = self.info or f'{config.DESC_MSG.unknown} feature'
        return f'{self._base_message()} {info} is not implemented.'

    def _unexpected_message(self) -> str:
        """Generates a message for unexpected errors."""
        context = self.error_context.split('.')
        if len(context) == 1 and context[0] == BaseConfig.PACKAGE:
            suffix = BASE_ERROR_MSG.default_package_suffix
        elif (
            len(context) == 2 and
            context[0] == BaseConfig.PACKAGE and
            context[1] in root.SUB_PACKAGE._fields
        ):
            suffix = BASE_ERROR_MSG.default_subpackage_suffix
        else:
            suffix = BASE_ERROR_MSG.default_module_suffix

        return (
            f'{BASE_ERROR_MSG.unexpected_error_prefix}'
            f' `{self.error_context}` {suffix}'
        )

    def message(self) -> str:
        """Builds a detailed, technical error message for base exceptions.

        Returns:
            A string representing the detailed error message.
        """
        error_message = ''

        match self.error_code:
            case config.GENERIC_ERROR.type_error:
                error_message = self._type_message()

            case config.GENERIC_ERROR.value_error:
                error_message = self._value_message()

            case config.GENERIC_ERROR.invalid_state:
                error_message = self._invalid_state_message()

            case config.GENERIC_ERROR.configuration_error:
                error_message = self._config_message()

            case config.GENERIC_ERROR.external_dependency_error:
                error_message = self._dependency_message()

            case config.GENERIC_ERROR.not_implemented_error:
                error_message = self._not_implemented_message()

            case config.GENERIC_ERROR.unexpected_error:
                error_message = self._unexpected_message()

            case _:
                error_message = (
                    f'{self._base_message()} Error code {self.error_code} '
                    f'unhandled {config.DESC_MSG.unexpected_error}.'
                )

        return error_message

    def user_message(self) -> str:
        """Builds a user-friendly error message for base exceptions.

        This method provides user-friendly messages for `GENERIC_ERROR` types,
        falling back to a general internal error message.

        Returns:
            A string representing the user-friendly error message.
        """
        error_message = ''

        match self.error_code:
            case config.GENERIC_ERROR.type_error:
                error_message = (
                    'An input was provided in an incorrect format.'
                )

            case config.GENERIC_ERROR.value_error:
                error_message = (
                    'An input value is not valid for this operation.'
                )

            case config.GENERIC_ERROR.invalid_state:
                error_message = (
                    'An operation attempted in an invalid application state.'
                )

            case config.GENERIC_ERROR.configuration_error:
                error_message = 'There is an issue with the configuration.'

            case config.GENERIC_ERROR.external_dependency_error:
                error_message = (
                    'An required tool or service encountered an issue.'
                )

            case config.GENERIC_ERROR.not_implemented_error:
                error_message = 'This feature is not available.'

            case config.GENERIC_ERROR.unexpected_error:
                error_message = BASE_ERROR_MSG.default_user_message

            case _:
                error_message = BASE_ERROR_MSG.default_user_message

        return error_message
