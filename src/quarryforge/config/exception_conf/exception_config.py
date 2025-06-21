"""Exception Configuration Module

This module defines various StrEnum configurations for standard error types
and common descriptive phrases used across the application's exception handling.
"""

from enum import StrEnum, auto
from typing import Any

__all__: list[str] = [
    'GenericError',
    'StringError',
    'PathError',
    'DescMsg',
]


class ValidName(StrEnum):
    """Assign the member's name as its value."""

    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[Any]
    ) -> Any:
        return name


class GenericError(ValidName):
    """The constants codes for generic types of errors.

    Attributes:
        type_error: Generic type mismatch
        value_error: Generic invaid value
        unexpected_error: Unforseen or unhandled error
        invalid_state: Operation attempted in an incorrect object/system state
        configuration_error: Application configuration issue
        external_dependency_error: External tool or service not found or failed
        not_implemented_error: Feature not implemented
    """

    TYPE_ERROR = auto()
    VALUE_ERROR = auto()
    UNEXPECTED_ERROR = auto()
    INVALID_STATE_ERROR = auto()
    CONFIGURATION_ERROR = auto()
    EXTERNAL_DEPENDENCY_ERROR = auto()
    NOT_IMPLEMENTED_ERROR = auto()


class StringError(ValidName):
    """The constant codes for errors involving strings.

    Attributes:
        empty: For empty or whitespace-only strings
        invalid_chars: For strings with unaccepted chars or patterns
    """

    EMPTY_STRING_ERROR = auto()
    INVALID_CHARS_ERROR = auto()


class PathError(ValidName):
    """The constant codes for errorw involving Path objects.

    Attributes:
        non_path_object:
            Error when argument is not a Path object or convertible string
        invalid_path_string:
            Error when a string cannot be interpreted asa valid path by the
            OS/library
        resolution:
            Error during path resolution (e.g., resolve() fails due to
            broken links, infinite loops, inaccessible components)
        nonexistent:
            Path is expected to exist, but doesn't (e.g., input file
            missing)
        existing:
            Path is expected not to exist (for creation), but already does
        parent_nonexistent:
            A path's parent directory doesn't exist, which is often a
            precondition for creating the path
        file_error:
            Path is expected to be a file, but isn't (e.g., it's a directory)
        dir_error:
            Path is expected to be a directory, but isn't (e.g., it's a file)
        unreadable: Path doesn't have read permissions
        unwritable: Path doesn't have write permissions
        unexecutable: Path doesn't have execute permissions
    """

    NON_PATH_OBJECT_ERROR = auto()
    INVALID_PATH_STRING_ERROR = auto()
    PATH_RESOLUTION_ERROR = auto()
    PATH_EXISTING_ERROR = auto()
    PATH_NONEXISTENT_ERROR = auto()
    PATH_NOT_A_FILE_ERROR = auto()
    PATH_NOT_A_DIRECTORY_ERROR = auto()
    PATH_NOT_READABLE_ERROR = auto()
    PATH_NOT_WRITABLE_ERROR = auto()
    PATH_NOT_EXECUTABLE_ERROR = auto()
    SAME_REPO_DIR_AND_WORK_DIR = auto()


class DescMsg(StrEnum):
    """Basic description partials with human-readable values."""

    DEPENDENCY = 'dependency'
    A_VALID_DICTIONARY = 'a valid dictionary'
    MUST_BE = 'must be'
    NONE = 'None'
    A_VALID_PATH = 'a valid path'
    REASON = 'reason'
    A_VALID_STRING = 'a valid string'
    A_NON_EMPTY_STRING = 'a non-empty string'
    IS_AN_UNEXPECTED_ERROR = 'is an unexpected error'
    UNKNOWN = 'unknown'
