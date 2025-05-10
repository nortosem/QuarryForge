"""Fossil Exception Module


"""
from quarryforge.exceptions import base_exception FossilError


class FossilTimelineError(FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = Message.Default.ERROR.value

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )


class FossilSetupError(FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = Message.Default.ERROR.value

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )


class FossilInfoError(FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = Message.Default.ERROR.value

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )


class FossilDiffError(FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = Message.Default.ERROR.value

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )


class FossilCatError(FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = Message.Default.ERROR.value

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )


class FossilBranchError(FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = Message.Default.ERROR.value

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )


class FossiAddError(FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = Message.Default.ERROR.value

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )


class FossilCommitError(FossilError):
    """

    Raised when a fossil command executed via subprocess returns a non-zero
    exit code, indicating an error in the command's execution.  Wraps the
    subprocess.CalledProcessError with a quarryforge specific exception.
    """
    CODE = Message.Default.ERROR.value

    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        effective_code = code if code is not None else self.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )
