"""Fossil Exception Configuration Module

This module defines the builder pattern for constructing detailed error data
for Fossil SCM-related exceptions. It centralizes error contexts and message
generation logic specific to Fossil operations.
"""
from typing import Any, Dict, NamedTuple

from quarryforge.config import fossil_config
from quarryforge.config import root
from quarryforge.config.exception_conf import base_exception_config as _
from quarryforge.config.exception_conf import exception_config as config
from quarryforge.meta import immutable


__all__ = ['FossilErrorBuilder']


class FossilMessage(NamedTuple):
    """Collect and define default messages for fossil exceptions."""
    no_cmd: str = f'{fossil_config.FOSSIL.cmd}: {config.DESC_MSG.none}'
    no_output: str = f'{fossil_config.FOSSIL.output}: {config.DESC_MSG.none}'
    no_stderr: str = f'{fossil_config.FOSSIL.stderr}: {config.DESC_MSG.none}'
    expected_str_list: str = 'Expected str or list, got'
    expected_int: str = 'Expected int, got'
    expected_str_or_none: str = 'Expected str or None, got'
    timeline_detail: str = 'while processing Fossil timeline.'
    timeline_user: str = (
        'Could not retrieve or parse the Fossil repository timeline.'
    )
    setup_detail: str = 'during Fossil repository setup'
    setup_user: str = 'There was a problem setting up the Fossil repository.'
    info_detail: str = 'while fetching Fossil artifact information.'
    info_user: str = 'Could not get details for the specified Fossil artifact.'
    diff_detail: str = 'during Fossil diff operation.'
    diff_user: str = (
        'Could not generate or process differences for the Fossil repository.'
    )
    cat_detail: str = 'while retrieving file content using Fossil cat.'
    cat_user: str = (
        'Could not retrieve file content from the Fossil repository.'
    )
    branch_detail: str = 'during Fossil branch operation.'
    branch_user: str = 'There was a problem with a Fossil branch operation.'
    add_detail: str = 'while adding files using Fossil add.'
    add_user: str = (
        'Could not add the specified file(s) to the Fossil repository.'
    )
    commit_detail: str = 'during Fossil commit operation.'
    commit_user: str = 'Could not commit changes to the Fossil repository.'


FOSSIL_MSG: FossilMessage = FossilMessage()


class FossilErrorPath(metaclass=immutable.Namespace):
    """Defines complete error context paths for Fossil SCM related exceptions.

    These paths are used as the `error_context` attribute in `ErrorBuilder`
    to provide a unique identifier for where an error occurred within
    the Fossil SCM interaction layer.
    """
    # General Fossil execution errors
    FOSSIL_PROCESS: str = _.BaseErrorPath.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FOSSIL.process
    )
    FOSSIL_TIMEOUT: str = _.BaseErrorPath.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FOSSIL.timeout
    )
    # Specific Fossil command errors
    FOSSIL_TIMELINE: str = _.BaseErrorPath.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FOSSIL.timeline
    )
    FOSSIL_SETUP: str = _.BaseErrorPath.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FOSSIL.setup
    )
    FOSSIL_INFO: str = _.BaseErrorPath.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FOSSIL.info
    )
    FOSSIL_DIFF: str = _.BaseErrorPath.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FOSSIL.diff
    )
    FOSSIL_CAT: str = _.BaseErrorPath.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FOSSIL.cat
    )
    FOSSIL_BRANCH: str = _.BaseErrorPath.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FOSSIL.branch
    )
    FOSSIL_ADD: str = _.BaseErrorPath.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FOSSIL.add
    )
    FOSSIL_COMMIT: str = _.BaseErrorPath.get_full_error_code(
        _.BaseErrorPath.FOSSIL, root.FOSSIL.commit
    )


class FossilErrorBuilder(_.BaseErrorBuilder):
    """Builder for constructing error data specific to Fossil SCM operations.

    This builder extends `BaseErrorBuilder` to provide detailed and
    user-friendly messages for Fossil process execution errors
    (e.g., `CalledProcessError`, `TimeoutExpiredError`) and other
    command-specific issues.
    """
    def _get_reason_suffix(self) -> str:
        """Helper to get a reason suffix from extra_details if available."""
        if self.extra_details and config.DESC_MSG.reason in self.extra_details:
            return f' Reason: {self.extra_details[config.DESC_MSG.reason]}.'
        return ''


    def _process_error_message(self) -> str:
        """Generates a message for `subprocess.CalledProcessError`."""
        base_msg: str = self._base_message()
        details: Dict[str, Any] = self.extra_details or {}

        cmd: str = details.get(
            fossil_config.FOSSIL.cmd, FOSSIL_MSG.no_cmd)
        return_code: int = details.get(
            fossil_config.FOSSIL.return_code, config.DESC_MSG.unknown)
        stdout: str = details.get(
            fossil_config.FOSSIL.output, FOSSIL_MSG.no_output)
        stderr: str = details.get(
            fossil_config.FOSSIL.stderr, FOSSIL_MSG.no_stderr)

        return (
            f'{base_msg} Fossil command failed. '
            f'Command: "{cmd}". Return Code: {return_code}. '
            f'STDOUT: "{stdout.strip()}". STDERR: "{stderr.strip()}".'
        )

    def _timeout_expired_message(self) -> str:
        """Generates a message for `subprocess.TimeoutExpired` errors."""
        base_msg = self._base_message()
        details: Dict[str, Any] = self.extra_details or {}

        cmd = details.get(
            fossil_config.FOSSIL.cmd, FOSSIL_MSG.no_cmd)
        timeout = details.get(
            fossil_config.FOSSIL.timeout, config.DESC_MSG.unknown)
        stdout = details.get(
            fossil_config.FOSSIL.output, FOSSIL_MSG.no_output)
        stderr = details.get(
            fossil_config.FOSSIL.stderr, FOSSIL_MSG.no_stderr)

        return (
            f'{base_msg} Fossil command timed out after {timeout} seconds. '
            f'Command: "{cmd}". '
            f'STDOUT: "{stdout.strip()}". STDERR: "{stderr.strip()}".'
        )

    def message(self) -> str:
        """Builds a detailed, technical error message for Fossil exceptions.

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
                    f'{FOSSIL_MSG.timeline_detail}{reason_suffix}'
                )
            case FossilErrorPath.FOSSIL_SETUP:
                step_info = '.'
                step = 'step'
                if self.extra_details and 'step' in self.extra_details:
                    step_info = f' during {self.extra_details[step]}.'
                return (
                    f'{base_msg} Failure '
                    f'{FOSSIL_MSG.setup_detail}{step_info}{reason_suffix}'
                )
            case FossilErrorPath.FOSSIL_INFO:
                return (
                    f'{base_msg} Failure '
                    f'{FOSSIL_MSG.info_detail}{reason_suffix}'
                )
            case FossilErrorPath.FOSSIL_DIFF:
                return (
                    f'{base_msg} Failure '
                    f'{FOSSIL_MSG.diff_detail}{reason_suffix}'
                )
            case FossilErrorPath.FOSSIL_CAT:
                return (
                    f'{base_msg} Failure '
                    f'{FOSSIL_MSG.cat_detail}{reason_suffix}'
                )
            case FossilErrorPath.FOSSIL_BRANCH:
                return (
                    f'{base_msg} Failure '
                    f'{FOSSIL_MSG.branch_detail}{reason_suffix}'
                )
            case FossilErrorPath.FOSSIL_ADD:
                return (
                    f'{base_msg} Failure '
                    f'{FOSSIL_MSG.add_detail}{reason_suffix}'
                )
            case FossilErrorPath.FOSSIL_COMMIT:
                return (
                    f'{base_msg} Failure '
                    f'{FOSSIL_MSG.commit_detail}{reason_suffix}'
                )
            case _:
                if self.error_code in config.GENERIC_ERROR:
                    return super().message()
                return (
                    f'{base_msg} An unspecified Fossil operation '
                    f'failed{reason_suffix}'
                )

    def user_message(self) -> str:
        """Builds a user-friendly error message for Fossil exceptions.

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
                return ('A Fossil command took too long to complete '
                        'and was stopped.'
                )
            case FossilErrorPath.FOSSIL_TIMELINE:
                return FOSSIL_MSG.timeline_user
            case FossilErrorPath.FOSSIL_SETUP:
                return FOSSIL_MSG.setup_user
            case FossilErrorPath.FOSSIL_INFO:
                return FOSSIL_MSG.info_user
            case FossilErrorPath.FOSSIL_DIFF:
                return FOSSIL_MSG.diff_user
            case FossilErrorPath.FOSSIL_CAT:
                return FOSSIL_MSG.cat_user
            case FossilErrorPath.FOSSIL_BRANCH:
                return FOSSIL_MSG.branch_user
            case FossilErrorPath.FOSSIL_ADD:
                return FOSSIL_MSG.add_user
            case FossilErrorPath.FOSSIL_COMMIT:
                return FOSSIL_MSG.commit_user
            case _:
                if self.error_code in config.GENERIC_ERROR:
                    return super().user_message()
                return _.BASE_ERROR_MSG.default_user_message
