"""Fossil Exception Module


"""
import subprocess
from typing import Dict, List, Optional, Union

from quarryforge.config.exception_conf import fossil_exception_config as _
from quarryforge.config.exception_conf.fossil_exception_config import ConfigFossilError as config
from quarryforge.exceptions import base_exception


class FossilProcessError(
    base_exception.FossilError,
    subprocess.CalledProcessError
):
    """Fossil Called Process Error

    Raised for a fossil subprocess throws a called process error (cpe).
    """
    CODE = _.FossilErrorContext.default_error(
        _.FossilErrorContext.FOSSIL_PROCESS
    )

    def __init__(
        self,
        returncode: int,
        cmd: Union[str, List[str]],
        stdout: Optional[Union[str, bytes]] = None,
        stderr: Optional[Union[str, bytes]] = None,
        message: Optional[str] = None,
        code: Optional[str] = None,
        details: Optional[Dict] = None,
        user_message: Optional[str] = None):

        if details is None:
            self.details = {}

        subprocess.CalledProcessError.__init__(
            self, returncode, cmd, output=stdout, stderr=stderr)

        if message is None:
            message = str(self)

        effective_code = code if code is not None else self.__class__.CODE

        base_exception.FossilError.__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message)

        self.details[config.CMD.value] = self.cmd
        self.details[config.RETURN_CODE.value] = self.returncode
        if self.stdout is not None:
            self.details[config.STDOUT.value] = self.stdout if isinstance(
                self.stdout, str) else self.stdout.decode(errors='replace')
        if self.stderr is not None:
            self.details[config.STDERR.value] = self.stderr if isinstance(
                self.stderr, str) else self.stderr.decode(errors='replace')


class FossilTimeoutError(
    base_exception.FossilError,
    subprocess.TimeoutExpired
):
    """Fossil Timeout Error


    """
    CODE = _.FossilErrorContext.default_error(
        _.FossilErrorContext.FOSSIL_TIMEOUT
    )

    def __init__(
        self,
        cmd: Union[str, List[str]],
        timeout: float,
        stdout: Optional[Union[str, bytes]] = None,
        stderr: Optional[Union[str, bytes]] = None,
        message: Optional[str] = None,
        code: Optional[str] = None,
        details: Optional[Dict[str, any]] = None,
        user_message: Optional[str] = None
    ):
        if details is None:
            self.details = {}

        subprocess.TimeoutExpired.__init__(
            self, cmd, timeout, output=stdout, stderr=stderr)

        if message is None:
            message = str(self)

        effective_code = code if code is not None else self.__class__.CODE

        base_exception.FossilError.__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message)

        self.details[config.CMD.value] = self.cmd
        self.details[config.TIMEOUT.value] = self.timeout
        if self.stdout is not None:
            self.details[config.STDOUT.value] = self.stdout if isinstance(
                self.stdout, str) else self.stdout.decode(errors='replace')
        if self.stderr is not None:
            self.details[config.STDERR.value] = self.stderr if isinstance(
                self.stderr, str) else self.stderr.decode(errors='replace')


class FossilTimelineError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = _.FossilErrorContext.default_error(
        _.FossilErrorContext.FOSSIL_TIMELINE
    )

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.__class__.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )


class FossilSetupError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = _.FossilErrorContext.default_error(
        _.FossilErrorContext.FOSSIL_SETUP
    )

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.__class__.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )


class FossilInfoError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = _.FossilErrorContext.default_error(
        _.FossilErrorContext.FOSSIL_INFO
    )

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.__class__.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )


class FossilDiffError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = _.FossilErrorContext.default_error(
        _.FossilErrorContext.FOSSIL_DIFF
    )

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.__class__.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )


class FossilCatError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = _.FossilErrorContext.default_error(
        _.FossilErrorContext.FOSSIL_CAT
    )

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.__class__.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )


class FossilBranchError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = _.FossilErrorContext.default_error(
        _.FossilErrorContext.FOSSIL_BRANCH
    )

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.__class__.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )


class FossilAddError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = _.FossilErrorContext.default_error(
        _.FossilErrorContext.FOSSIL_ADD
    )

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.__class__.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )


class FossilCommitError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = _.FossilErrorContext.default_error(
        _.FossilErrorContext.FOSSIL_COMMIT
    )

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.__class__.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )
