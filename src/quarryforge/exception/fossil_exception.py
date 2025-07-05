"""Define specific exception classes for Fossil SCM operations."""

import subprocess
from typing import Any

from quarryforge.config import fossil_config as config
from quarryforge.config.exception_conf import fossil_exception_config as _
from quarryforge.exception import base_exception


__all__: list[str] = [
    'FossilProcessError', 'FossilTimeoutError', 'FossilOperationError'
]


class FossilProcessError(
    base_exception.FossilError, subprocess.CalledProcessError
):
    """Raise when a Fossil subprocess command returns a non-zero exit code."""

    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: dict[str, Any],
    ):
        """Initialize FossilProcessError.

        Args:
            code: The unique error code identifier.
            message: The detailed technical error message.
            user_message: A user-friendly message.
            details: A dictionary containing detailed error information,
                expected to include `cmd`, `returncode`, `stdout`, `stderr`.

        """
        cmd = details.get(config.Fossil.CMD, _.FossilMessage.NO_CMD)
        returncode = details.get(
            config.Fossil.RETURN_CODE,
            int(config.Fossil.DEFAULT_RETURN_CODE)
        )
        output = details.get(config.Fossil.OUTPUT, _.FossilMessage.NO_OUTPUT)
        stderr = details.get(config.Fossil.STDERR, _.FossilMessage.NO_STDERR)

        if not isinstance(cmd, (str, list)):
            raise TypeError(
                f'{_.FossilMessage.EXPECTED_STR_LIST}, but got '
                f'{type(cmd).__name__}'
            )
        if not isinstance(returncode, int):
            raise TypeError(
                f'{_.FossilMessage.EXPECTED_INT}, but got '
                f'{type(returncode).__name__}'
            )
        if output is not None and not isinstance(output, (str, bytes)):
            raise TypeError(
                f'{_.FossilMessage.EXPECTED_STR_OR_NONE}, but got '
                f'{type(output).__name__}'
            )
        if stderr is not None and not isinstance(stderr, (str, bytes)):
            raise TypeError(
                f'{_.FossilMessage.EXPECTED_STR_OR_NONE}, but got '
                f'{type(stderr).__name__}'
            )

        subprocess.CalledProcessError.__init__(
            self,
            returncode=returncode,
            cmd=cmd,
            output=output,
            stderr=stderr
        )

        base_exception.FossilError.__init__(
            self,
            code=code,
            message=message,
            user_message=user_message,
            details=details,
        )


class FossilTimeoutError(base_exception.FossilError, subprocess.TimeoutExpired):
    """Raise when a fossil subprocess command returns a timeout error."""

    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: dict[str, Any],
    ):
        """Initialize FossilTimeoutError.

        Args:
            code: The unique error code identifier.
            message: The detailed technical error message.
            user_message: A user-friendly message.
            details: A dictionary containing detailed error information,
                     expected to include `cmd`, `timeout`, `stdout`, `stderr`.

        """
        cmd = details.get(config.Fossil.CMD, _.FossilMessage.NO_CMD)
        timeout = details.get(
            config.Fossil.TIMEOUT,
            float(config.Fossil.DEFAULT_TIMEOUT)
        )
        output = details.get(config.Fossil.OUTPUT, _.FossilMessage.NO_OUTPUT)
        stderr = details.get(config.Fossil.STDERR, _.FossilMessage.NO_STDERR)

        cmd = details.get(config.Fossil.CMD, _.FossilMessage.NO_CMD)
        timeout = details.get(
            config.Fossil.TIMEOUT,
            float(config.Fossil.DEFAULT_TIMEOUT)
        )
        output = details.get(config.Fossil.OUTPUT, _.FossilMessage.NO_OUTPUT)
        stderr = details.get(config.Fossil.STDERR, _.FossilMessage.NO_STDERR)

        if not isinstance(cmd, (str, list)):
            raise TypeError(
                f'{_.FossilMessage.EXPECTED_STR_LIST}, but got '
                f'{type(cmd).__name__}'
            )
        if not isinstance(timeout, (int, float)):
            raise TypeError(
                f'Expected int or float for timeout, but got '
                f'{type(timeout).__name__}'
            )
        if output is not None and not isinstance(output, (str, bytes)):
            raise TypeError(
                f'{_.FossilMessage.EXPECTED_STR_OR_NONE}, but got '
                f'{type(output).__name__}'
        )
        if stderr is not None and not isinstance(stderr, (str, bytes)):
            raise TypeError(
                f'{_.FossilMessage.EXPECTED_STR_OR_NONE}, but got '
                f'{type(stderr).__name__}'
            )
        subprocess.TimeoutExpired.__init__(
            self,
            cmd=cmd,
            timeout=timeout,
            output=output,
            stderr=stderr
        )

        base_exception.FossilError.__init__(
            self,
            code=code,
            message=message,
            user_message=user_message,
            details=details,
        )


class FossilOperationError(base_exception.FossilError):
    """Raise when a Fossil-related operation fails due to logic or parsing.

    Indicates a `fossil` command succeeds (exit code 0) but the application
    logic that processes its output encounters an error.
    For example, failing to parse the string returned by `fossil timeline`.
    """
    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: dict[str, Any],
    ):
        """Initialize FossilOperationError."""
        super().__init__(
            code=code,
            message=message,
            user_message=user_message,
            details=details,
        )
