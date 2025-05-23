"""Fault Builder


"""
from typing import NamedTuple


__all__: list = [
    'DESC_TYPE', 'ERROR_TYPE', 'ARG',
    'DEFAULT', 'IMMUTABLE', 'PATH_MSG', 'REQUIRED'
]


class DescType(NamedTuple):
    """Description strings for errors."""
    string: str = 'str'
    path: str = 'Path'
    empty: str = 'empty_string'
    exists: str = 'Path exists'
    is_file: str = 'Path is file'
    is_dir: str = 'Path is directory'
    is_readable: str = 'Path is readable'
    is_writable: str = 'Path is writable'
    is_list: str = 'List'
    str_list_content = 'List[str]'
    non_empty_list_content = 'List[str] is not empty'


DESC_TYPE: DescType = DescType()
"""Global ..."""


class ErrorType(NamedTuple):
    """"""
    type_error: str = 'TYPE_ERROR'


ERROR_TYPE: ErrorType = ErrorType()


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

    def message(self, arg: str, context: str, field: str) -> str:
        return (
            f'Type error in context "{context}" for field: {field}. '
            f'String expected, but got type {type(arg).__name__} instead.'
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
