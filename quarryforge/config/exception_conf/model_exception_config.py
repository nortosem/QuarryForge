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
from typing import NamedTuple

from quarryforge.config import model_config
from quarryforge.config import root
from quarryforge.config.exception_conf import exception_config as msg
from quarryforge.config.exception_conf import exception_data
from quarryforge.meta import immutable


class ModelErrorContext(metaclass=immutable.Namespace):
    """Context for Model Errors"""
    FOSSIL_COMMIT = model_config.FOSSIL_COMMIT.path()
    FOSSIL_REPO = model_config.FOSSIL_REPO.path()
   # TIMELINE = (
   #     (msg.Default.DOT).join([
            #root.Valid.QUARRYFORGE,
   #         root.TopModules.MODEL,
   #         root.ModelNames.FOSSIL_TIMELINE])
   # )

    def default_error(self, model: str):
        """Default Exception Context Code"""
        return (msg.Default.DOT).join([
            model, msg.Default.ERROR])


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
