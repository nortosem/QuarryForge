"""Fault Builder


"""
from typing import NamedTuple


__all__ = ['ERROR_TYPE', 'ARG', 'DEFAULT', 'IMMUTABLE', 'PATH_MSG', 'REQUIRED']


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

    @classmethod
    def invalid(cls, name: str):
        return f'{cls.INVALID} {name} {cls.ARG}'

    @classmethod
    def missing(cls, name: str, kind: str):
        return f'{cls.MISSING} {cls.ARG} {name} {cls.TYPE} {kind}'


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

    @classmethod
    def error_message(cls, name: str):
        return f'{name} {cls.MESSAGE}'


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

    @classmethod
    def dir_not_allowed(cls, path: str):
        return f'{path} {cls.NO_DIR.value}'

    @classmethod
    def not_a_path(cls, path: str) -> str:
        return f'{path} {cls.NAP}'

    @classmethod
    def does_not_exist(cls, path: str) -> str:
        return f'{path} {cls.DNE}'

    @classmethod
    def not_a_file(cls, path: str) -> str:
        return f'{path} {cls.NAF}'

    @classmethod
    def not_a_directory(cls, path: str) -> str:
        return f'{path} {cls.NAD}'

    @classmethod
    def no_read_permission(cls, path: str) -> str:
        return f'{path} {cls.READ}'

    @classmethod
    def no_write_permission(cls, path: str) -> str:
        return f'{path} {cls.WRITE}'


PATH_MSG: PathMessage = PathMessage()
"""Global ..."""


class Required(NamedTuple):
    """Field Missing Message


    """
    THE = 'The'
    EMPTY = 'field cannot be empty'
    REQUIRE = 'field requires a'

    @classmethod
    def field_type(cls, field: str, kind: type):
        return f'{cls.THE} {field} {cls.REQUIRE} {str(kind)}'

    @classmethod
    def field_empty(cls, field: str, kind: type):
        return f'{cls.THE} {str(kind)} {field} {cls.EMPTY}'


REQUIRED: Required = Required()
"""Global ..."""
