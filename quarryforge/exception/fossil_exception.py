"""Fossil Exception Module

This module defines specific exception classes for errors encountered during
Fossil SCM operations, leveraging the `FossilErrorBuilder` for structured
error data.
"""
import subprocess
from typing import Any, Dict

from quarryforge.config import fossil_config as config
from quarryforge.config.exception_conf import fossil_exception_config as _
from quarryforge.exception import base_exception


class FossilProcessError(
        base_exception.FossilError,
        subprocess.CalledProcessError
):
    """Fossil Called Process Error

    Raised when a Fossil subprocess command returns a non-zero exit code.
    This exception extends `subprocess.CalledProcessError` to retain its
    attributes while integrating with the QuarryForge exception structure via
    `FossilErrorBuilder`.
    """
    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: Dict[str, Any]
    ):
        """Initialize FossilProcessError.

        Args:
            code: The unique error code identifier.
            message: The detailed technical error message.
            user_message: A user-friendly message.
            details: A dictionary containing detailed error information,
                expected to include `cmd`, `returncode`, `stdout`, `stderr`.
        """
        cmd: str = _.FossilMessage.no_cmd
        return_code: int = config.FOSSIL.default_return_code
        output: str = _.FossilMessage.no_output
        stderr: str = _.FossilMessage.no_stderr

        if details[config.FOSSIL.cmd]:
            if not isinstance(cmd, (str, list)):
                raise TypeError(
                    f'{_.FossilMessage.expected_str_list} {type(cmd).__name__}'
                )
            cmd = details.get(config.FOSSIL.cmd, cmd)

        if details[config.FOSSIL.return_code]:
            if not isinstance(return_code, int):
                raise TypeError(
                    f'{_.FossilMessage.expected_int} '
                    f'{type(return_code).__name__}'
                )
            return_code = details.get(
                config.FOSSIL.return_code, return_code
            )

        if details[config.FOSSIL.output]:
            if not isinstance(output, str):
                raise TypeError(
                    f'{_.FossilMessage.expected_str_or_none} '
                    f'{type(stderr).__name__}'
                )
            output = details.get(config.FOSSIL.output, output)

        if details[config.FOSSIL.stderr]:
            if not isinstance(stderr, str):
                raise TypeError(
                    f'{_.FossilMessage.expected_str_or_none} '
                    f'{type(stderr).__name__}'
                )
            stderr = details.get(config.FOSSIL.stderr, stderr)

        subprocess.CalledProcessError.__init__(
            self, return_code, cmd, output=output, stderr=stderr)

        base_exception.FossilError.__init__(
            self,
            code=code,
            message=message,
            user_message=user_message,
            details=details
        )


class FossilTimeoutError(
    base_exception.FossilError,
    subprocess.TimeoutExpired
):
    """Fossil Timeout Error


    """
    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: Dict[str, Any]
    ):
        """Initialize FossilTimeoutError.

        Args:
            code: The unique error code identifier.
            message: The detailed technical error message.
            user_message: A user-friendly message.
            details: A dictionary containing detailed error information,
                     expected to include `cmd`, `timeout`, `stdout`, `stderr`.
        """
        cmd: str = _.FossilMessage.no_cmd
        timeout: int = config.FOSSIL.default_timeout
        output: str = _.FossilMessage.no_output
        stderr: str = _.FossilMessage.no_stderr

        if details[config.FOSSIL.cmd]:
            if not isinstance(cmd, (str, list)):
                raise TypeError(
                    f'{_.FossilMessage.expected_str_list} {type(cmd).__name__}'
                )
            cmd = details.get(config.FOSSIL.cmd, cmd)
        if details[config.FOSSIL.timeout]:
            if not isinstance(timeout, int):
                raise TypeError(
                    f'{_.FossilMessage.expected_int} {type(timeout).__name__}'
                )
            timeout = details.get(config.FOSSIL.timeout, timeout)
        if details[config.FOSSIL.output]:
            if not isinstance(output, str):
                raise TypeError(
                    f'{_.FossilMessage.expected_str_or_none} '
                    f'{type(output).__name__}'
                )
            output = details.get(config.FOSSIL.output, output)
        if details[config.FOSSIL.stderr]:
            if not isinstance(stderr, str):
                raise TypeError(
                    f'{_.FossilMessage.expected_str_or_none} '
                    f'{type(stderr).__name__}'
                )
            stderr = details.get(config.FOSSIL.stderr, stderr)


        subprocess.TimeoutExpired.__init__(
            self, cmd, timeout, output=output, stderr=stderr)

        base_exception.FossilError.__init__(
            self,
            code=code,
            message=message,
            user_message=user_message,
            details=details
        )


class FossilTimelineError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: Dict[str, Any]
    ):
        """Fossil Timeline Error Init"""
        super().__init__(
            code=code,
            message=message,
            user_message=user_message,
            details=details,
        )


class FossilSetupError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: Dict[str, Any]
    ):
        """Fossil Setup Error Init"""
        super().__init__(
            code=code,
            message=message,
            user_message=user_message,
            details=details,
        )


class FossilInfoError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: Dict[str, Any]
    ):
        """Fossil Info Error Init"""
        super().__init__(
            code=code,
            message=message,
            user_message=user_message,
            details=details,
        )


class FossilDiffError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: Dict[str, Any]
    ):
        """Fossil Diff Error Init"""
        super().__init__(
            code=code,
            message=message,
            user_message=user_message,
            details=details,
        )


class FossilCatError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: Dict[str, Any]
    ):
        """Fossil Cat Error Init"""
        super().__init__(
            code=code,
            message=message,
            user_message=user_message,
            details=details,
        )


class FossilBranchError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: Dict[str, Any]
    ):
        """Fossil Branch Error Init"""
        super().__init__(
            code=code,
            message=message,
            user_message=user_message,
            details=details,
        )


class FossilAddError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: Dict[str, Any]
    ):
        """Fossil Add Error Init"""
        super().__init__(
            code=code,
            message=message,
            user_message=user_message,
            details=details,
        )


class FossilCommitError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: Dict[str, Any]
    ):
        """Fossil Commit Error Init"""
        super().__init__(
            code=code,
            message=message,
            user_message=user_message,
            details=details,
        )
