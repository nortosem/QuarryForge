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
    PACKAGE = root.PACKAGE.name

    @classmethod
    def path(cls, module_name: str) -> str:
        return f'{cls.PACKAGE}.{module_name}'


class BaseErrorContext(metaclass=immutable.Namespace):
    """Context for the Base Exceptions of QuarryForge"""
    QUARRY_FORGE = BaseConfig.PACKAGE
    MODEL_ERROR = BaseConfig.path(root.MODULE.model)
    FOSSIL_ERROR = BaseConfig.path(root.MODULE.fossil)
    MAIN_ERROR = BaseConfig.path(root.MODULE.main)
    META_ERROR = BaseConfig.path(root.SUB_PACKAGE.meta)
    UTIL_ERROR = BaseConfig.path(root.SUB_PACKAGE.util)

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
    package_error = BaseErrorContext.package_error()
    model_error = BaseErrorContext.default_error(
        BaseErrorContext.MODEL_ERROR)
    fossil_error = BaseErrorContext.default_error(
        BaseErrorContext.FOSSIL_ERROR)
    main_error = BaseErrorContext.default_error(
        BaseErrorContext.MAIN_ERROR)
    meta_error = BaseErrorContext.default_error(
        BaseErrorContext.META_ERROR)
    util_error = BaseErrorContext.default_error(
        BaseErrorContext.UTIL_ERROR)


class DefaultMessage(metaclass=immutable.Namespace):
    """The default base_exception error messages."""
    unexpected_error = (
        'An unexpected error occurred within the ')
    quarryforge_error = (
        f'{root.PACKAGE.name} package.')
    model_error = (
        f'{root.PACKAGE.name} {root.Module.model} module.')
    fossil_error = (
        f'{root.PACKAGE.name} {root.Module.model} module.')
    main_error = (
        f'{root.PACKAGE.name} {root.Module.model} module.')
    meta_error = (
        f'{root.PACKAGE.name} {root.SubPackage.meta} subpackage.')
    util_error = (
        f'{root.PACKAGE.name} {root.SubPackage.util} subpackage.')
