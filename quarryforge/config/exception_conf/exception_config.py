"""Exception Configuration Module


"""
from typing import List, NamedTuple


__all__: List = [
    'GENERIC_ERROR',
    'STRING_ERROR',
    'PATH_ERROR',
]


class GenericErrorType(NamedTuple):
    """The constants codes for generic types of errors."""
    type_error: str = 'TYPE_ERROR'
    unexpected_error: str = 'UNEXPECTED_ERROR'
    value_error: str = 'VALUE_ERROR'


GENERIC_ERROR = GenericErrorType()
"""Global instance for general error types."""


class StringErrorType(NamedTuple):
    """The constant codes for errors involving strings."""
    type_error: str = 'STRING'
    empty_error: str = 'EMPTY_STRING'
    invalid_error: str = 'INVALID_STRING'


STRING_ERROR: StringErrorType = StringErrorType()
"""Global instance for string error types."""


class PathErrorType(NamedTuple):
    """The constant codes for errorw involving Path objects."""
    non_path_object: str = 'NON_PATH_OBJECT_ERROR'
    invalid_path_string: str = 'INVALID_PATH_STRING_ERROR'
    resolution: str = 'PATH_RESOLUTION_ERROR'
    existing: str = 'EXISTING_PATH_ERROR'
    nonexistent: str = 'NONEXISTENT_PATH_ERROR'
    file_error: str = 'PATH_NOT_A_FILE_ERROR'
    dir_error: str = 'PATH_NOT_A_DIRECTORY_ERROR'
    unreadable: str = 'PATH_NOT_READABLE_ERROR'
    unwritable: str = 'PATH_NOT_WRITABLE_ERROR'
    unexecutable: str = 'PATH_NOT_EXECUTABLE_ERROR'


PATH_ERROR: PathErrorType = PathErrorType()
"""Global instance for path error types."""


class DescType(NamedTuple):
    """Basic description partials."""
    must_be: str = 'must be'
    string: str = 'a valid string'
    path: str = 'a valid path'
    unempty: str = 'a non-empty string'
    unknown: str = 'is an unknown error'


DESC_TYPE = DescType()
"""Global instance for description parts."""
