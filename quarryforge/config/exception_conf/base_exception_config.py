"""Base Exception Config

The configuraiton for the exception base class of quarryforge errors.
"""
from quarryforge.config import root
from quarryforge.config.exception_conf import exception_config as msg


class BaseErrorContext(root.Config):
    """Context for the Base Exceptions of QuarryForge"""
    QUARRY_FORGE_ERROR = root.Valid.QUARRYFORGE.value

    MODEL_ERROR = (
        (msg.Default.DOT.value).join([
            root.Valid.QUARRYFORGE.value,
            root.TopModules.MODEL.value])
    )
    FOSSIL_ERROR = (
        (msg.Default.DOT.value).join([
            root.Valid.QUARRYFORGE.value,
            root.TopModules.FOSSIL.value])
    )
    MAIN_ERROR = (
        (msg.Default.DOT.value).join([
            root.Valid.QUARRYFORGE.value,
            root.TopModules.MAIN.value])
    )

    @classmethod
    def default_error(cls, model: BaseErrorContext):
        """Default Exception Context Code"""
        return (msg.Default.DOT.value.join([
            model.value, msg.Default.ERROR.value])
        )
