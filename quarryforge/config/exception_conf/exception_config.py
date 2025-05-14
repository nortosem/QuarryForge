"""Fault Builder


"""
from quarryforge.config.root import Valid


class ConfigQuarryForgeError(Valid):
    """Valid Error Message Fields"""
    CODE = 'code'
    MESSAGE = 'message'
    USER_MESSAGE = 'user_message'
    DETAILS = 'details'


class ConfigBuilder(Valid):
    """ValidErrorData Builder fields"""
    CONTEXT = 'context'
    FIELD = 'field'
    ERROR_TYPE = 'error_type'
    MESSAGE = 'message'
    USER_MESSAGE = 'user_message'
    INPUT_VALUE = 'input_value'
    EXPECTED_DESC = 'expected_desc'
    EXTRA_DETAILS = 'extra_details'


class ErrorType(Valid):
    """"""
    EMPTY = 'Empty_String'


class ErrorKind(Valid):
    """"""
    STR = 'str'
    PATH = 'Path'


class Argument(Valid):
    """Argument Messages


    """
    ARG = 'argument'
    INVALID = 'Invalid'
    MISSING = 'Missing'
    TYPE = 'type:'

    @classmethod
    def invalid(cls, name: Valid):
        return (Default.SPC.value).join(
            [cls.INVALID.value, name.value, cls.ARG.value]
        )

    @classmethod
    def missing(cls, name: Valid, kind: str):
        return (Default.SPC.value).join(
            [cls.MISSING.value,cls.ARG.value,name.value,cls.TYPE.value, kind]
        )


class Default(Valid):
    """Default Messages


    """
    DOT = '.'
    SPC = ' '
    BAR = ' | '
    NL = '\n'
    EMPTY = 'EMPTY'
    ERROR = 'ERROR'


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
    DNE = ' does not exist.'
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


class Required(Valid):
    """Field Missing Message


    """
    THE = 'The '
    EMPTY = ' field cannot be empty'
    REQUIRE = ' field requires a '

    @classmethod
    def field_type(cls, field: Valid, kind: type):
        return cls.THE.value + field.value + cls.REQUIRE.value + str(kind)

    @classmethod
    def field_empty(cls, field: Valid, kind: type):
        return cls.The.value + str(kind) + field.value + cls.EMPTY.value
