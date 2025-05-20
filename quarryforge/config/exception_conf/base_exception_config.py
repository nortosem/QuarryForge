"""Base Exception Config

The configuraiton for the exception base class of quarryforge errors.
"""
from quarryforge.config import root
from quarryforge.config.exception_conf import exception_config as msg
from quarryforge.meta import immutable


__all__: List[str] = ['DefaultCode', 'DefaultMessage']


class BaseConfig(metaclass=immutable.Namespace):
    """Base Config

    Define default path for all base exceptions.
    """
    PACKAGE: str = root.PACKAGE.name

    @classmethod
    def path(cls, module_name: str) -> str:
        return f'{cls.PACKAGE}.{module_name}'


class BaseErrorContext(metaclass=immutable.Namespace):
    """Context for the Base Exceptions of QuarryForge"""
    QUARRY_FORGE: str = BaseConfig.PACKAGE
    MODEL_ERROR: str = BaseConfig.path(root.MODULE.model)
    FOSSIL_ERROR: str = BaseConfig.path(root.MODULE.fossil)
    MAIN_ERROR: str = BaseConfig.path(root.MODULE.main)
    META_ERROR: str = BaseConfig.path(root.SUB_PACKAGE.meta)
    UTIL_ERROR: str = BaseConfig.path(root.SUB_PACKAGE.util)

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
            f'{context}.{msg.Default.ERROR}')


class DefaultCode(metaclass=immutable.Namespace):
    """Default Error Code message"""
    package_error: str = BaseErrorContext.package_error()
    model_error: str = BaseErrorContext.default_error(
        BaseErrorContext.MODEL_ERROR)
    fossil_error: str = BaseErrorContext.default_error(
        BaseErrorContext.FOSSIL_ERROR)
    main_error: str = BaseErrorContext.default_error(
        BaseErrorContext.MAIN_ERROR)
    meta_error: str = BaseErrorContext.default_error(
        BaseErrorContext.META_ERROR)
    util_error: str = BaseErrorContext.default_error(
        BaseErrorContext.UTIL_ERROR)


class DefaultMessage(metaclass=immutable.Namespace):
    """The default base_exception error messages."""
    unexpected_error: str = (
        'An unexpected error occurred within the')
    quarryforge_error: str = (
        f'{unexpected_error} {root.PACKAGE.name} package.')
    model_error: str = (
        f'{unexpected_error}  {root.PACKAGE.name}.{root.Module.model} module.')
    fossil_error: str = (
        f'{unexpected_error} {root.PACKAGE.name}.{root.Module.model} module.')
    main_error: str = (
        f'{unexpected_error} {root.PACKAGE.name}.{root.Module.model} module.')
    meta_error: str = (
        f'{unexpected_error} '
        f'{root.PACKAGE.name}.{root.SubPackage.meta} subpackage.')
    util_error: str = (
        f'{unexpected_error} '
        f'{root.PACKAGE.name}.{root.SubPackage.util} subpackage.')
