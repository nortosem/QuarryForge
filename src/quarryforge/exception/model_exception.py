"""Model Exceptions

This module defines specific exception classes for errors encountered within
the data models, leveraging builders for structured error data.
"""

from typing import Any

from quarryforge.exception import base_exception


class FossilRepoError(base_exception.ModelError):
    """FossilRepo Error

    Exception raised for errors related to the FossilRepo data model.
    This includes issues with path validation, file access, and repository
    state.
    """

    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: dict[str, Any],
    ):
        """Initializes the FossilRepoError.

        Args:
            code: The unique error code identifier.
            message: The detailed technical error message.
            user_message: A user-friendly message for display.
            details: A dictionary containing detailed error information.
        """
        super().__init__(
            code=code,
            message=message,
            user_message=user_message,
            details=details,
        )


class FossilCommitError(base_exception.ModelError):
    """FossilCommit Error

    Exception raised for errors related to the FossilCommit data model.
    This includes issues with commit data validation, parsing, and immutability.
    """

    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: dict[str, Any],
    ):
        """Initializes the FossilCommitError.

        Args:
            code: The unique error code identifier.
            message: The detailed technical error message.
            user_message: A user-friendly message for display.
            details: A dictionary containing detailed error information.
        """
        super().__init__(
            code=code,
            message=message,
            user_message=user_message,
            details=details,
        )


class FossilTimelineError(base_exception.ModelError):
    """Fossil Timeline Error

    Exception raised for errors related to the FossilTimeline data model.
    This typically involves issues with parsing timeline data or constructing
    the timeline object.
    """

    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: dict[str, Any],
    ):
        """Initializes the FossilTimelineError.

        Args:
            code: The unique error code identifier.
            message: The detailed technical error message.
            user_message: A user-friendly message for display.
            details: A dictionary containing detailed error information.
        """
        super().__init__(
            code=code,
            message=message,
            user_message=user_message,
            details=details,
        )
