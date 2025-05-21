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
from typing import List

from quarryforge.config import model_config
from quarryforge.config import root
from quarryforge.config.exception_conf import base_exception_config
from quarryforge.config.exception_conf import exception_config as msg
from quarryforge.meta import immutable


__all__: List[str] = [
    'DefaultCode',
    'DefaultMessage',
]


class ModelErrorContext(metaclass=immutable.Namespace):
    """Context for Model Errors"""
    FOSSIL_COMMIT: str = model_config.FOSSIL_COMMIT.path()
    FOSSIL_REPO: str = model_config.FOSSIL_REPO.path()
    FOSSIL_TIMELINE: str = model_config.FOSSIL_TIMELINE.path()

    @staticmethod
    def default_error(context: str):
        """Default Exception Context Code"""
        return f'{context}.{msg.Default.ERROR}'


class DefaultCode(metaclass=immutable.Namespace):
    """The Default Exception Codes for Model Exceptions."""
    fossil_repo: str = ModelErrorContext.default_error(
        ModelErrorContext.FOSSIL_REPO)
    fossil_commit: str = ModelErrorContext.default_error(
        ModelErrorContext.FOSSIL_COMMIT)
    fossil_timeline: str = ModelErrorContext.default_error(
        ModelErrorContext.FOSSIL_TIMELINE)


class DefaultMessage(metaclass=immutable.Namespace):
    """The Default Exception Messages for Model Exceptions."""
    fossil_repo: str = (
        f'{base_exception_config.DefaultMessage.unexpected_error} '
        f'{root.PACKAGE.name}.{root.Module.model}.{root.Model.fossil_repo}')
    fossil_commit: str = (
        f'{base_exception_config.DefaultMessage.unexpected_error} '
        f'{root.PACKAGE.name}.{root.Module.model}.{root.Model.fossil_commit}')
    fossil_timeline: str = (
        f'{base_exception_config.DefaultMessage.unexpected_error} '
        f'{root.PACKAGE.name}.{root.Module.model}.'
        f'{root.Model.fossil_timeline}')


class FossilRepoContext(metaclass=immutable.Namespace):
    """FossilRepo Context

    Messages for FossilRepo.
    """
    EMPTY_STR_MSG: str = ''
  #  msg.Argument.missing(
  #      ConfigFossilRepo.FILE, (msg.Default.SPC).join(
  #          msg.ErrorKind.STR,
  #          msg.Default.BAR,
  #          msg.ErrorKind.PATH)
  #      )
  #  EMPTY_STR_USER_MSG: str = msg.Required.field_empty(
  #      ConfigFossilRepo.file(), str
  #  )
  #  INVALID: str = (msg.Default.NL).join(
  #      [msg.Argument.invalid(
  #          ConfigFossilRepo.file()),
  #       msg.Required.field_type(ConfigFossilRepo.file())]
  #  )
    NOT_EXIST: str = ('')
    NOT_FILE: str = ('')
    NOT_READ: str = ('')
    DIR_WRITE: str = ('')
