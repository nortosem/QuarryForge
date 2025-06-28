"""Defines the builder pattern for constructing detailed error data.

Fossil SCM-related exceptions are centralized to provide error contexts and
message generation logic specific to Fossil operations.
"""

from enum import StrEnum
from typing import Any

from quarryforge.config import fossil_config, root
from quarryforge.config.exception_conf import base_exception_config as _
from quarryforge.config.exception_conf import exception_config as config

__all__ = ['FossilErrorBuilder']


class FossilMessage(StrEnum):
    """Collect and define default messages for fossil exceptions."""

    NO_CMD = f'{fossil_config.Fossil.CMD}: {config.DescMsg.NONE}'
    NO_OUTPUT = f'{fossil_config.Fossil.OUTPUT}: {config.DescMsg.NONE}'
    NO_STDERR = f'{fossil_config.Fossil.STDERR}: {config.DescMsg.NONE}'
    EXPECTED_STR_LIST = 'Expected str or list, got'
    EXPECTED_INT = 'Expected int, got'
    EXPECTED_STR_OR_NONE = 'Expected str or None, got'
    TIMELINE_DETAIL = 'while processing Fossil timeline.'
    TIMELINE_USER = (
        'Could not retrieve or parse the Fossil repository timeline.'
    )
    SETUP_DETAIL = 'during Fossil repository setup'
    SETUP_USER = 'There was a problem setting up the Fossil repository.'
    INFO_DETAIL = 'while fetching Fossil artifact information.'
    INFO_USER = 'Could not get details for the specified Fossil artifact.'
    DIFF_DETAIL = 'during Fossil diff operation.'
    DIFF_USER = (
        'Could not generate or process differences for the Fossil repository.'
    )
    CAT_DETAIL = 'while retrieving file content using Fossil cat.'
    CAT_USER = 'Could not retrieve file content from the Fossil repository.'
    BRANCH_DETAIL = 'during Fossil branch operation.'
    BRANCH_USER = 'There was a problem with a Fossil branch operation.'
    ADD_DETAIL = 'while adding files using Fossil add.'
    ADD_USER = 'Could not add the specified file(s) to the Fossil repository.'
    COMMIT_DETAIL = 'during Fossil commit operation.'
    COMMIT_USER = 'Could not commit changes to the Fossil repository.'


class FossilErrorPath(StrEnum):
    """Defines complete error context paths for Fossil SCM related exceptions.

    These paths are used as the `error_context` attribute in `ErrorBuilder`
    to provide a unique identifier for where an error occurred within
    the Fossil SCM interaction layer.
    """

    # General Fossil execution errors
    FOSSIL_PROCESS = _.get_full_error_code(
        _.BaseErrorPath.FOSSIL, fossil_config.Fossil.PROCESS_ERROR
    )
    FOSSIL_TIMEOUT = _.get_full_error_code(
        _.BaseErrorPath.FOSSIL, fossil_config.Fossil.TIMEOUT_ERROR
    )
    # Specific Fossil command errors
    FOSSIL_TIMELINE = _.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FossilModule.TIMELINE
    )
    FOSSIL_SETUP = _.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FossilModule.SETUP
    )
    FOSSIL_INFO = _.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FossilModule.INFO
    )
    FOSSIL_DIFF = _.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FossilModule.DIFF
    )
    FOSSIL_CAT = _.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FossilModule.CAT
    )
    FOSSIL_BRANCH = _.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FossilModule.BRANCH
    )
    FOSSIL_ADD = _.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FossilModule.ADD
    )
    FOSSIL_COMMIT = _.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FossilModule.COMMIT
    )


class FossilErrorBuilder(_.BaseErrorBuilder):
    """Builder for constructing error data specific to Fossil SCM operations.

    This builder extends `BaseErrorBuilder` to provide detailed and
    user-friendly messages for Fossil process execution errors
    (e.g., `CalledProcessError`, `TimeoutExpiredError`) and other
    command-specific issues.
    """

    def _get_reason_suffix(self) -> str:
        """Use helper to get reason suffix from extra_details if available."""
        details = self.extra_details or {}
        reason = details.get(config.DescMsg.REASON)
        return f' Reason: {reason}.' if reason else ''

    def _process_error_message(self) -> str:
        """Generate a message for `subprocess.CalledProcessError`."""
        base_msg: str = self._base_message()
        details: dict[str, Any] = self.extra_details or {}

        cmd: str = details.get(fossil_config.Fossil.CMD, FossilMessage.NO_CMD)
        return_code: int | None = details.get(
            fossil_config.Fossil.RETURN_CODE,
            fossil_config.Fossil.DEFAULT_RETURN_CODE,
        )
        stdout: str = (
            details.get(fossil_config.Fossil.OUTPUT, FossilMessage.NO_OUTPUT)
        ).strip()
        stderr: str = (
            details.get(fossil_config.Fossil.STDERR, FossilMessage.NO_STDERR)
        ).strip()

        return (
            f'{base_msg} Fossil command failed. '
            f'Command: "{cmd}". Return Code: {return_code}. '
            f'STDOUT: "{stdout}". STDERR: "{stderr}".'
        )

    def _timeout_expired_message(self) -> str:
        """Generate a message for `subprocess.TimeoutExpired` errors."""
        base_msg = self._base_message()
        details: dict[str, Any] = self.extra_details or {}

        cmd: str = details.get(fossil_config.Fossil.CMD, FossilMessage.NO_CMD)
        timeout: str = details.get(
            fossil_config.Fossil.TIMEOUT, fossil_config.Fossil.DEFAULT_TIMEOUT
        )
        stdout: str = (
            details.get(fossil_config.Fossil.OUTPUT, FossilMessage.NO_OUTPUT)
        ).strip()
        stderr: str = (
            details.get(fossil_config.Fossil.STDERR, FossilMessage.NO_STDERR)
        ).strip()

        return (
            f'{base_msg} Fossil command timed out after {timeout} seconds. '
            f'Command: "{cmd}". '
            f'STDOUT: "{stdout}". STDERR: "{stderr}".'
        )

    def message(self) -> str:
        """Build a detailed, technical error message for Fossil exceptions.

        Overrides `BaseErrorBuilder`'s message to provide specific details for
        Fossil process and timeout related errors.
        """
        base_msg: str = self._base_message()
        reason_suffix: str = self._get_reason_suffix()
        match self.error_context:
            case FossilErrorPath.FOSSIL_PROCESS:
                return self._process_error_message()
            case FossilErrorPath.FOSSIL_TIMEOUT:
                return self._timeout_expired_message()
            case FossilErrorPath.FOSSIL_TIMELINE:
                return (
                    f'{base_msg} Failure '
                    f'{FossilMessage.TIMELINE_DETAIL}{reason_suffix}'
                )
            case FossilErrorPath.FOSSIL_SETUP:
                step_info = '.'
                step = 'step'
                if self.extra_details and 'step' in self.extra_details:
                    step_info = f' during {self.extra_details[step]}.'
                return (
                    f'{base_msg} Failure '
                    f'{FossilMessage.SETUP_DETAIL}{step_info}{reason_suffix}'
                )
            case FossilErrorPath.FOSSIL_INFO:
                return (
                    f'{base_msg} Failure '
                    f'{FossilMessage.INFO_DETAIL}{reason_suffix}'
                )
            case FossilErrorPath.FOSSIL_DIFF:
                return (
                    f'{base_msg} Failure '
                    f'{FossilMessage.DIFF_DETAIL}{reason_suffix}'
                )
            case FossilErrorPath.FOSSIL_CAT:
                return (
                    f'{base_msg} Failure '
                    f'{FossilMessage.CAT_DETAIL}{reason_suffix}'
                )
            case FossilErrorPath.FOSSIL_BRANCH:
                return (
                    f'{base_msg} Failure '
                    f'{FossilMessage.BRANCH_DETAIL}{reason_suffix}'
                )
            case FossilErrorPath.FOSSIL_ADD:
                return (
                    f'{base_msg} Failure '
                    f'{FossilMessage.ADD_DETAIL}{reason_suffix}'
                )
            case FossilErrorPath.FOSSIL_COMMIT:
                return (
                    f'{base_msg} Failure '
                    f'{FossilMessage.COMMIT_DETAIL}{reason_suffix}'
                )
            case _:
                if self.error_code in config.GenericError:
                    return super().message()
                return (
                    f'{base_msg} An unspecified Fossil operation '
                    f'failed{reason_suffix}'
                )

    def user_message(self) -> str:
        """Build a user-friendly error message for Fossil exceptions.

        Overrides the base implementation to provide more specific user messages
        for Fossil process and timeout errors.
        """
        match self.error_context:
            case FossilErrorPath.FOSSIL_PROCESS:
                return (
                    'An issue occurred while running a Fossil command. '
                    'Please check logs for details.'
                )
            case FossilErrorPath.FOSSIL_TIMEOUT:
                return (
                    'A Fossil command took too long to complete '
                    'and was stopped.'
                )
            case FossilErrorPath.FOSSIL_TIMELINE:
                return FossilMessage.TIMELINE_USER
            case FossilErrorPath.FOSSIL_SETUP:
                return FossilMessage.SETUP_USER
            case FossilErrorPath.FOSSIL_INFO:
                return FossilMessage.INFO_USER
            case FossilErrorPath.FOSSIL_DIFF:
                return FossilMessage.DIFF_USER
            case FossilErrorPath.FOSSIL_CAT:
                return FossilMessage.CAT_USER
            case FossilErrorPath.FOSSIL_BRANCH:
                return FossilMessage.BRANCH_USER
            case FossilErrorPath.FOSSIL_ADD:
                return FossilMessage.ADD_USER
            case FossilErrorPath.FOSSIL_COMMIT:
                return FossilMessage.COMMIT_USER
            case _:
                # For generic errors, fall back to the base implementation.
                if self.error_code in config.GenericError:
                    return super().user_message()
                # Otherwise, provide a default fossil-specific user message.
                return _.base_error_message().default_user_message
