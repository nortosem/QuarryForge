"""Fault Builder


"""
from typing import NamedTuple


__all__: list = [
    'ERROR_TYPE', 'ARG', 'DEFAULT', 'IMMUTABLE', 'PATH_MSG', 'REQUIRED'
]


class ErrorType(NamedTuple):
    """Strings for types of errors."""
    STR = 'str'
    PATH = 'Path'
    EMPTY = 'empty_string'


ERROR_TYPE: ErrorType = ErrorType()
"""Global ..."""


class Argument(NamedTuple):
    """Argument Messages"""
    ARG = 'argument'
    INVALID = 'Invalid'
    MISSING = 'Missing'
    TYPE = 'type:'

    def invalid(self, name: str):
        return f'{self.INVALID} {name} {self.ARG}'

    def missing(self, name: str, kind: str):
        return f'{self.MISSING} {self.ARG} {name} {self.TYPE} {kind}'


ARG: Argument = Argument()
"""Global ..."""


class Default(NamedTuple):
    """Default message parts"""
    DOT = '.'
    SPC = ' '
    BAR = ' | '
    NL = '\n'
    EMPTY = 'EMPTY'
    ERROR = 'ERROR'


DEFAULT: Default = Default()
"""Global ..."""


class Immutable(NamedTuple):
    """Immutable Message"""
    MESSAGE = 'object is immutable.'

    def error_message(self, name: str):
        return f'{name} {self.MESSAGE}'


IMMUTABLE: Immutable = Immutable()
"""Global ..."""


class PathMessage(NamedTuple):
    """Filename Message


    """
    NAP = 'is not a path.'
    DNE = 'does not exist.'
    NAF = 'is not a file.'
    NAD = 'is not a directory.'
    READ = 'is not readable.'
    WRITE = 'is not writable.'
    NO_DIR = 'cannot write output to a directory.'

    def dir_not_allowed(self, path: str):
        return f'{path} {self.NO_DIR.value}'

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
    THE = 'The'
    EMPTY = 'field cannot be empty'
    REQUIRE = 'field requires a'

    def field_type(self, field: str, kind: type):
        return f'{self.THE} {field} {self.REQUIRE} {str(kind)}'

    def field_empty(self, field: str, kind: type):
        return f'{self.THE} {str(kind)} {field} {self.EMPTY}'


REQUIRED: Required = Required()
"""Global ..."""
