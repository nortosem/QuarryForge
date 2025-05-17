"""Base Exception Config

The configuraiton for the exception base class of quarryforge errors.
"""
from quarryforge.config import root
from quarryforge.config.exception_conf import exception_config as msg
from quarryforge.meta import immutable


class BaseConfig(metaclass=immutable.Namespace):
    """Base Config

    Define default path for all base exceptions.
    """
    __slots__ = ('PACKAGE')

    PACKAGE = root.PACKAGE.name

    @classmethod
    def path(cls, module_name: str) -> str:
        return f'{cls.PACKAGE}.{module_name}'


class BaseErrorContext(metaclass=immutable.Namespace):
    """Context for the Base Exceptions of QuarryForge"""
    __slots__ = ('QUARRY_FORGE','MODEL_ERROR', 'FOSSIL_ERROR', 'MAIN_ERROR')

    QUARRY_FORGE = BaseConfig.PACKAGE
    MODEL_ERROR = BaseConfig.path(root.MODULE.model)
    FOSSIL_ERROR = BaseConfig.path(root.MODULE.fossil)
    MAIN_ERROR = BaseConfig.path(root.MODULE.main)

    @classmethod
    def package_error(cls):
        return f'{cls.QUARRY_FORGE}.{msg.Default.ERROR}'

    @classmethod
    def default_error(cls, context: str):
        """Default Exception Context Code"""
        if not isinstance(context, str):
            raise TypeError('todo')

        if context is BaseErrorContext.QUARRY_FORGE:
            return cls.package_error()

        return (
            f'{context}.{msg.Default.ERROR}'
        )
