"""Model Exception Configuration

1st check if arg is a string,
next strip if it is a string.
if it is empty string raise error.
else turn string into a path object.
expanduser and resolve.
must exist if is_new is False.
must be a file
must be fossilrrepor
if new repo true:
mst be path or path from string.
file does not exist.
is parent dir exist and writeable?
"""
from quarryforge.config import model_config
from quarryforge.config import root
from quarryforge.config.exception_conf import base_exception_config
from quarryforge.config.exception_conf import exception_config as msg
from quarryforge.meta import immutable


class ModelErrorContext(metaclass=immutable.Namespace):
    """Context for Model Errors"""
    FOSSIL_COMMIT = model_config.FOSSIL_COMMIT.path()
    FOSSIL_REPO = model_config.FOSSIL_REPO.path()
    FOSSIL_TIMELINE = model_config.FOSSIL_TIMELINE.path()

    @staticmethod
    def default_error(model: str):
        """Default Exception Context Code"""
        return f'{model}.{msg.Default.ERROR}'


class DefaultCode(metaclass=immutable.Namespace):
    """The Default Exception Codes for Model Exceptions."""
    fossil_repo = ModelErrorContext.default_error(
        ModelErrorContext.FOSSIL_REPO)
    fossil_commit = ModelErrorContext.default_error(
        ModelErrorContext.FOSSIL_COMMIT)
    fossil_timeline = ModelErrorContext.default_error(
        ModelErrorContext.FOSSIL_TIMELINE)


class DefaultMessage(metaclass=immutable.Namespace):
    """The Default Exception Messages for Model Exceptions."""
    fossil_repo = (
        f'{base_exception_config.unexpected_error} '
        f'{root.PACKAGE.name}.{root.Module.model}.{root.Model.fossil_repo}')
    fossil_commit = (
        f'{base_exception_config.unexpected_error} '
        f'{root.PACKAGE.name}.{root.Module.model}.{root.Model.fossil_commit}')
    fossil_timeline = (
        f'{base_exception_config.unexpected_error} '
        f'{root.PACKAGE.name}.{root.Module.model}.'
        f'{root.Model.fossil_timeline}')


class FossilRepoContext(metaclass=immutable.Namespace):
    """FossilRepo Context

    Messages for FossilRepo.
    """
    EMPTY_STR_MSG = ''
  #  msg.Argument.missing(
  #      ConfigFossilRepo.FILE, (msg.Default.SPC).join(
  #          msg.ErrorKind.STR,
  #          msg.Default.BAR,
  #          msg.ErrorKind.PATH)
  #      )
  #  EMPTY_STR_USER_MSG = msg.Required.field_empty(
  #      ConfigFossilRepo.file(), str
  #  )
  #  INVALID = (msg.Default.NL).join(
  #      [msg.Argument.invalid(
  #          ConfigFossilRepo.file()),
  #       msg.Required.field_type(ConfigFossilRepo.file())]
  #  )
    NOT_EXIST = ()
    NOT_FILE = ()
    NOT_READ = ()
    DIR_WRITE = ()
