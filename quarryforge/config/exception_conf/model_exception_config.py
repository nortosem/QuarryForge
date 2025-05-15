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
from enum import Enum

from quarryforge.config import model_config
from quarryforge.config import root
from quarryforge.config.exception_conf import exception_config as msg
from quarryforge.config.exception_conf import exception_data


class ModelErrorContext(root.Config):
    """Context for Model Errors"""
    FOSSIL_COMMIT = model_config.ConfigFossilCommit.path()
    FOSSIL_REPO = model_config.ConfigFossilRepo.path()
    TIMELINE = (
        (msg.Default.DOT.value).join([
            root.Valid.QUARRYFORGE.value,
            root.TopModules.MODEL.value,
            root.ModelNames.FOSSIL_TIMELINE.value])
    )

    @classmethod
    def default_error(cls, model: ModelErrorContext):
        """Default Exception Context Code"""
        return (msg.Default.DOT.value.join([
            model.value, msg.Default.ERROR.value])
        )



