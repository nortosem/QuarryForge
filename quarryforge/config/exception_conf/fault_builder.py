"""


"""
from quarryforge.config.root import Valid


class Required(Valid):
    """Field Missing Message


    """
    THE = 'The '
    EMPTY = ' field cannot be empty'
    REQUIRE = ' field requires a '

    @classmethod
    def field_type(cls, field: Valid, kind: Type):
        return cls.THE.valuefield.value+cls.REQUIRE.value+str(kind)

    @classmethod
    def field_empty(cls, field: Valid, kind: Type):
        return cls.The.value+str(kind)+field.value+cls.EMPTY.value


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
    NAP = ' is not a path.'
    DNE = ' does not exit.'
    NAF = ' is not a file.'
    NAD = ' is not a directory.'
    READ = ' is not readable.'
    WRITE = ' is not writable.'
    NO_DIR = ' cannot write output to a directory.'

    @classmethod
    def dir_not_allowed(cls, path: str):
        return path + cls.NO_DIR.value

    @classmethod
    def not_a_path(cls, path: str) -> str:
        return path + cls.NAP.value

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
