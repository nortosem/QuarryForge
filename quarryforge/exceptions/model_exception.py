"""Model Exceptions

#TODO
"""
from typing import Dict, Optional

from quarryforge.config import root as get
from quarryforge.config.exception_conf import message as Message
from quarryforge.exceptions import base_exception


class FossilRepoError(base_exception.ModelError):
    """FossilRepo Error

    Base exception for the FossilRepo class.
    """
    CODE = get.ModelNames.FOSSIL_REPO.value + Message.Default.ERROR.value

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


class FossilSetupError(base_exception.ModelError):
    """


    """
    CODE = get.TopModules.MODEL.value + Message.Default.ERROR.value

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


class CommitError(base_exception.ModelError):
    """Commit Error

    Base exception for the Commit class.
    """
    CODE = get.TopModules.MODEL.value + Message.Default.ERROR.value

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


class TimelineError(base_exception.ModelError):
    """Timeline Parsing Error

    Raised when there is an error parsing the output of the `fossil timeline`
    command.  This might occur if the output format is unexpected or if
    there are issues extracting data from the timeline text.
    """
    CODE = get.TopModules.MODEL.value + Message.Default.ERROR.value

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
