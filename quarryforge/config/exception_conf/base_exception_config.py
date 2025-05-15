"""Base Exception Config

The configuraiton for the exception base class of quarryforge errors.
"""
from quarryforge.config import root
from quarryforge.config.exception_conf import exception_config as msg


class BaseConfig(root.Valid):
    """Base Config

    Define default path for all base exceptions.
    """
    PACKAGE = root.Valid.QUARRYFORGE.value

    @classmethod
    def path(cls, module_name: str) -> str;
        return f'{cls.PACKAGE}.{module_name}'


class BaseErrorContext(root.Config):
    """Context for the Base Exceptions of QuarryForge"""
    QUARRY_FORGE = BaseConfig.PACKAGE.value
    MODEL_ERROR = BaseConfig.path(root.TopModules.MODEL.value)
    FOSSIL_ERROR = BaseConfig.path(root.TopModules.FOSSIL.value)
    MAIN_ERROR = BaseConfig.path(root.TopModules.MAIN.value)

    @classmethod
    def package_error(cls):
        return f'{cls.QUARRY_FORGE.value}.{msg.Default.ERROR.value}'

    @classmethod
    def default_error(cls, model: BaseErrorContext):
        """Default Exception Context Code"""
        if model is BaseErrorContext.QUARRY_FORGE:
            return cls.package_error()
        if model is not in BaseErrorContext:
            raise Exception #just raise qf exception most likely

        return (msg.Default.DOT.value.join([
            model.value, msg.Default.ERROR.value])
        )
