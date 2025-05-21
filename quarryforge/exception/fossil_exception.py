"""Fossil Exception Module


"""
import subprocess
from typing import Dict, List, Optional, Union

from quarryforge.config.exception_conf import fossil_exception_config as _
from quarryforge.exception import base_exception


class FossilProcessError(
    base_exception.FossilError,
    subprocess.CalledProcessError):
    """Fossil Called Process Error

    Raised for a fossil subprocess throws a called process error (cpe).
    """
    def __init__(self,
                 returncode: int,
                 cmd: Union[str, List[str]],
                 stdout: Optional[Union[str, bytes]] = None,
                 stderr: Optional[Union[str, bytes]] = None,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):
        """FossilProcessError Init"""
        if details is None:
            self.details = {}

        subprocess.CalledProcessError.__init__(
            self, returncode, cmd, output=stdout, stderr=stderr)

        base_exception.FossilError.__init__(
            message=message or _.DefaultMessage.fossil_process,
            code=code or _.DefaultCode.fossil_process,
            details=details,
            user_message=user_message)

        self.details[_.ERROR_FIELD.cmd] = self.cmd
        self.details[_.ERROR_FIELD.return_code] = self.returncode
        if self.stdout is not None:
            self.details[_.ERROR_FIELD.stdout] = self.stdout if isinstance(
                self.stdout, str) else self.stdout.decode(errors='replace')
        if self.stderr is not None:
            self.details[_.ERROR_FIELD.stderr] = self.stderr if isinstance(
                self.stderr, str) else self.stderr.decode(errors='replace')


class FossilTimeoutError(
    base_exception.FossilError,
    subprocess.TimeoutExpired):
    """Fossil Timeout Error


    """
    def __init__(self,
                 cmd: Union[str, List[str]],
                 timeout: float,
                 stdout: Optional[Union[str, bytes]] = None,
                 stderr: Optional[Union[str, bytes]] = None,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict[str, any]] = None,
                 user_message: Optional[str] = None):
        """FossilTimeoutError Init"""
        if details is None:
            self.details = {}

        subprocess.TimeoutExpired.__init__(
            self, cmd, timeout, output=stdout, stderr=stderr)

        base_exception.FossilError.__init__(
            message=message or _.DefaultMessage.fossil_timeout,
            code=code or _.DefaultCode.fossil_timeout,
            details=details,
            user_message=user_message)

        self.details[_.ERROR_FIELD.cmd] = self.cmd
        self.details[_.ERROR_FIELD.timeout] = self.timeout
        if self.stdout is not None:
            self.details[_.ERROR_FIELD.stdout] = self.stdout if isinstance(
                self.stdout, str) else self.stdout.decode(errors='replace')
        if self.stderr is not None:
            self.details[_.ERROR_FIELD.stderr] = self.stderr if isinstance(
                self.stderr, str) else self.stderr.decode(errors='replace')


class FossilTimelineError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):
        """Fossil Timeline Error Init"""
        super().__init__(
            message=message or _.DefaultMessage.fossil_timeline,
            code=code or _.DefaultCode.fossil_timeline,
            details=details,
            user_message=user_message)


class FossilSetupError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):
        """Fossil Setup Error Init"""
        super().__init__(
            message=message or _.DefaultMessage.fossil_setup,
            code=code or _.DefaultCode.fossil_setup,
            details=details,
            user_message=user_message)


class FossilInfoError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):
        """Fossil Info Error Init"""
        super().__init__(
            message=message or _.DefaultMessage.fossil_info,
            code=code or _.DefaultCode.fossil_info,
            details=details,
            user_message=user_message)


class FossilDiffError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):
        """Fossil Diff Error Init"""
        super().__init__(
            message=message or _.DefaultMessage.fossila_diff,
            code=code or _.DefaultCode.fossila_diff,
            details=details,
            user_message=user_message)


class FossilCatError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):
        """Fossil Cat Error Init"""
        super().__init__(
            message=message or _.DefaultMessage.fossil_cat,
            code=code or _.DefaultCode.fossil_cat,
            details=details,
            user_message=user_message)


class FossilBranchError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):
        """Fossil Branch Error Init"""
        super().__init__(
            message=message or _.DefaultMessage.fossil_branch,
            code=code or _.DefaultCode.fossil_branch,
            details=details,
            user_message=user_message)


class FossilAddError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):
        """Fossil Add Error Init"""
        super().__init__(
            message=message or _.DefaultMessage.fossil_add,
            code=code or _.DefaultCode.fossil_add,
            details=details,
            user_message=user_message)


class FossilCommitError(base_exception.FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):
        """Fossil Commit Error Init"""
        super().__init__(
            message=message or _.DefaultMessage.fossil_commit,
            code=code or _.DefaultCode.fossil_commit,
            details=details,
            user_message=user_message)
