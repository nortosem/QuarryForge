"""Fossil Exception Configuration Module


"""
from quarryforge.config import fossil_config
from quarryforge.config.exception_conf import exception_config as msg
from quarryforge.meta import immutable


class ConfigFossilError(metaclass=immutable.Namespace):
    """Define the fossil error field configuration"""
    CMD = 'cmd'
    RETURN_CODE = 'returncode'
    STDOUT = 'stdout'
    STDERR = 'stderr'
    TIMEOUT = 'timeout'


class FossilErrorContext(metaclass=immutable.Namespace):
    """FossilErrorContext


    """
    FOSSIL_PROCESS = fossil_config.ConfigProcess.path()
    FOSSIL_TIMEOUT = fossil_config.ConfigTimeout.path()
    FOSSIL_TIMELINE = fossil_config.ConfigTimeline.path()
    FOSSIL_SETUP = fossil_config.ConfigSetup.path()
    FOSSIL_INFO = fossil_config.ConfigInfo.path()
    FOSSIL_DIFF = fossil_config.ConfigDiff.path()
    FOSSIL_CAT = fossil_config.ConfigCat.path()
    FOSSIL_BRANCH = fossil_config.ConfigBranch.path()
    FOSSIL_ADD = fossil_config.ConfigAdd.path()
    FOSSIL_COMMIT = fossil_config.ConfigCommit.path()

    @classmethod
    def default_error(cls, context: str):
        """Default Exception Context Code"""
        if not isinstance(context, str):
            raise TypeError('todo')

        return (
            f'{context.value}{msg.Default.DOT.value}{msg.Default.ERROR.value}'
        )
