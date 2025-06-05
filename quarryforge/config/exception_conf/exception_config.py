"""Exception Configuration Module

This module defines various NamedTuple configurations for standard error types
and common descriptive phrases used across the application's exception handling.
"""
from typing import List, NamedTuple


__all__: List[str] = [
    'GENERIC_ERROR',
    'STRING_ERROR',
    'PATH_ERROR',
    'DESC_MSG',
]


class GenericErrorType(NamedTuple):
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
    type_error: str = 'TYPE_ERROR'
    value_error: str = 'VALUE_ERROR'
    unexpected_error: str = 'UNEXPECTED_ERROR'
    invalid_state: str = 'INVALID_STATE_ERROR'
    configuration_error: str = 'CONFIGURATION_ERROR'
    external_dependency_error: str = 'EXTERNAL_DEPENDENCY_ERROR'
    not_implemented_error: str = 'NOT_IMPLEMENTED_ERROR'


GENERIC_ERROR = GenericErrorType()
"""Global instance for general error types."""


class StringErrorType(NamedTuple):
    """The constant codes for errors involving strings.

    Attributes:
        empty: For empty or whitespace-only strings
        invalid_chars: For strings with unaccepted chars or patterns
    """
    empty: str = 'EMPTY_STRING_ERROR'
    invalid_chars: str = 'INVALID_CHARS_ERROR'


STRING_ERROR: StringErrorType = StringErrorType()
"""Global instance for string error types."""


class PathErrorType(NamedTuple):
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
    non_path_object: str = 'NON_PATH_OBJECT_ERROR'
    invalid_path_string: str = 'INVALID_PATH_STRING_ERROR'
    resolution: str = 'PATH_RESOLUTION_ERROR'
    existing: str = 'PATH_EXISTING_ERROR'
    nonexistent: str = 'PATH_NONEXISTENT_ERROR'
    file_error: str = 'PATH_NOT_A_FILE_ERROR'
    dir_error: str = 'PATH_NOT_A_DIRECTORY_ERROR'
    unreadable: str = 'PATH_NOT_READABLE_ERROR'
    unwritable: str = 'PATH_NOT_WRITABLE_ERROR'
    unexecutable: str = 'PATH_NOT_EXECUTABLE_ERROR'
    same_dir: str = 'SAME_REPO_DIR_AND_WORK_DIR'


PATH_ERROR: PathErrorType = PathErrorType()
"""Global instance for path error types."""


class DescMsg(NamedTuple):
    """Basic description partials."""
    dependency: str = 'dependency'
    dictionary: str = 'a valid dictionary'
    must_be: str = 'must be'
    none: str = 'None'
    path: str = 'a valid path'
    reason: str = 'reason'
    string: str = 'a valid string'
    unempty: str = 'a non-empty string'
    unexpected_error: str = 'is an unexpected error'
    unknown: str = 'unknown'


DESC_MSG = DescMsg()
"""Global instance for description parts."""
