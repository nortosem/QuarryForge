"""


"""
from quarryforge.config.root import Valid


class Required(Valid):
    """Field Missing Message


    """
    THE = 'The '
    EMPTY = ' field cannot be empty'
    REQUIRED = ' field is required'

    @classmethod
    def field_missing(cls, field: Valid):
        return cls.THE.value + field.value+cls.REQUIRED.value

    @classmethod
    def field_empty(cls, field: Valid):
        return cls.The.value + field.value+cls.EMPTY.value


class Immutable(Valid):
    """Immutable Message


    """
    MESSAGE = ' object is immutable.'

    @classmethod
    def error_message(cls, name: Valid):
        return name.value + cls.MESSAGE.value


class PathMessage(Valid):
    """Filename Message


    """
    DNE = ' does not exit.'
    NAF = ' is not a file.'
    NAD = ' is not a directory.'
    READ = ' is not readable.'
    WRITE = ' is not writable.'

    @classmethod
    def does_not_exist(cls, path: str) -> str:
        return path + cls.DNE.value

    @classmethod
    def not_a_file(cls, path: str) -> str:
        return path + cls.NAF.value

    @classmethod
    def not_a_directory(cls, path: str) -> str:
        return path + cls.NAD. value

    @classmethod
    def no_read_permission(cls, path: str) -> str:
        return path + cls.READ.value

    @classmethod
    def no_write_permission(cls, path: str) -> str:
        return path + cls.WRITE.value
