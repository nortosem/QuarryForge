"""Fault Builder


"""
from typing import NamedTuple

from quarryforge.meta import immutable


__all__: list = [
    'DESC_TYPE', 'ERROR_TYPE', 'ARG',
    'DEFAULT', 'IMMUTABLE', 'PATH_MSG', 'REQUIRED'
]


class DescType(NamedTuple):
    """Description strings for errors."""
    unknown: str = 'Unknown'
    string: str = 'str'
    path: str = 'Path'
    empty: str = 'empty_string'
    exists: str = 'Path_exists'
    is_file: str = 'File_Path'
    is_dir: str = 'Directory_Path'
    is_readable: str = 'readable_Path'
    is_writable: str = 'writable_Path'
    is_executable: str = 'executable_Path'
    is_list: str = 'List'
    str_list_content = 'List[str]'
    non_empty_list_content = 'non-empty_List[str]'


DESC_TYPE: DescType = DescType()
"""Global ..."""


class GenericErrorType(NamedTuple):
    """A collection of constants for generic types of errors."""
    type_error: str = 'TYPE_ERROR'
    unexpected_error: str = 'UNEXPECTED_ERROR'
    value_error: str = 'VALUE_ERROR'


class StringErrorType(NamedTuple):
    """A collection of constants for errors involving strings."""
    empty: str = 'EMPTY_STRING_ERROR'
    invalid: str = 'INVALID_STRING_ERROR'


class PathErrorType(NamedTuple):
    """A collection of constants for error involving Path objects."""
    non_path_object: str = 'NON_PATH_OBJECT_ERROR'
    invalid_path_string: str = 'INVALID_PATH_STRING_ERROR'
    resolution: str = 'PATH_RESOLUTION_ERROR'
    nonexistent: str = 'NONEXISTENT_PATH_ERROR'
    parent_nonexistent: str = 'NONEXISTENT_PATH_PARENT_ERROR'
    file_error: str = 'PATH_NOT_A_FILE_ERROR'
    dir_error: str = 'PATH_NOT_A_DIRECTORY_ERROR'
    unreadable: str = 'PATH_NOT_READABLE_ERROR'
    unwritable: str = 'PATH_NOT_WRITABLE_ERROR'
    unexecutable: str = 'PATH_NOT_EXECUTABLE_ERROR'


class Argument(NamedTuple):
    """Argument Messages"""
    ARG: str = 'argument'
    INVALID: str = 'Invalid'
    MISSING: str = 'Missing'
    TYPE: str = 'type:'

    def invalid(self, name: str):
        return f'{self.INVALID} {name} {self.ARG}'

    def missing(self, name: str, kind: str) -> str:
        return f'{self.MISSING} {self.ARG} {name} {self.TYPE} {kind}'

    def type_message(
        self,
        arg: str,
        error: str,
        context: str,
        field: str,
        type_: str,
    ) -> str:
        return (
            f'{error} in context "{context}" for field: {field}. '
            f'{type_} expected, but got type {type(arg).__name__} instead.'
        )

ARG: Argument = Argument()
"""Global ..."""


class Default(NamedTuple):
    """Default message parts"""
    EMPTY: str = 'EMPTY'
    ERROR: str = 'DEFAULT_ERROR'


DEFAULT: Default = Default()
"""Global ..."""


class Immutable(NamedTuple):
    """Immutable Message"""
    MESSAGE: str = 'object is immutable.'

    def error_message(self, name: str):
        return f'{name} {self.MESSAGE}'


IMMUTABLE: Immutable = Immutable()
"""Global ..."""


class PathMessage(NamedTuple):
    """Filename Message


    """
    NAP: str = 'is not a path.'
    DNE: str = 'does not exist.'
    NAF: str = 'is not a file.'
    NAD: str = 'is not a directory.'
    READ: str = 'is not readable.'
    WRITE: str = 'is not writable.'
    NO_DIR: str = 'cannot write output to a directory.'

    def dir_not_allowed(self, path: str):
        return f'{path} {self.NO_DIR}'

    def not_a_path(self, path: str) -> str:
        return f'{path} {self.NAP}'

    def does_not_exist(self, path: str) -> str:
        return f'{path} {self.DNE}'

    def not_a_file(self, path: str) -> str:
        return f'{path} {self.NAF}'

    def not_a_directory(self, path: str) -> str:
        return f'{path} {self.NAD}'

    def no_read_permission(self, path: str) -> str:
        return f'{path} {self.READ}'

    def no_write_permission(self, path: str) -> str:
        return f'{path} {self.WRITE}'


PATH_MSG: PathMessage = PathMessage()
"""Global ..."""


class Required(NamedTuple):
    """Field Missing Message


    """
    THE: str = 'The'
    EMPTY: str = 'field cannot be empty'
    REQUIRE: str = 'field requires a'

    def field_type(self, field: str, kind: type):
        return f'{self.THE} {field} {self.REQUIRE} {str(kind)}'

    def field_empty(self, field: str, kind: type):
        return f'{self.THE} {str(kind)} {field} {self.EMPTY}'


REQUIRED: Required = Required()
"""Global ..."""


class ErrorMessageMaker(metaclass=immutable.Namespace):
    """ErrorMessageMaker creates error messages.

    ErrorTypes and context information determine which messages are produced.
    """

