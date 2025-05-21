"""Model Exceptions

#TODO
"""
from typing import Dict, Optional

from quarryforge.config.exception_conf import model_exception_config as _
from quarryforge.exception import base_exception


class FossilRepoError(base_exception.ModelError):
    """FossilRepo Error

    Base exception for the FossilRepo class.
    """
    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        super().__init__(
            message=message or _.DefaultMessage.fossil_repo,
            code=code or _.DefaultCode.fossil_repo,
            details=details,
            user_message=user_message
        )


class FossilCommitError(base_exception.ModelError):
    """FossilCommit Error

    Base exception for the Commit class.
    """
    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        super().__init__(
            message=message or _.DefaultMessage.fossil_commit,
            code=code or _.DefaultCode.fossil_commit,
            details=details,
            user_message=user_message
        )


class FossilTimelineError(base_exception.ModelError):
    """Fossil Timeline Error

    """
    def __init__(self,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        super().__init__(
            message=message or _.DefaultMessage.fossil_timeline,
            code=code or _.DefaultCode.fossil_timeline,
            details=details,
            user_message=user_message
        )
