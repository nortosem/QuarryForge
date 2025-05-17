"""Fossil Exception Configuration Module


"""
from quarryforge.config import fossil_config
from quarryforge.config.exception_conf import exception_config as msg
from quarryforge.meta import immutable


class ConfigFossilError(metaclass=immutable.Namespace):
    """Define the fossil error field configuration"""
    CMD: str = 'cmd'
    RETURN_CODE: str = 'returncode'
    STDOUT: str = 'stdout'
    STDERR: str = 'stderr'
    TIMEOUT: str = 'timeout'


class FossilErrorContext(metaclass=immutable.Namespace):
    """FossilErrorContext


    """
    FOSSIL_PROCESS: str = fossil_config.ConfigProcess.path()
    FOSSIL_TIMEOUT: str = fossil_config.ConfigTimeout.path()
    FOSSIL_TIMELINE: str = fossil_config.ConfigTimeline.path()
    FOSSIL_SETUP: str = fossil_config.ConfigSetup.path()
    FOSSIL_INFO: str = fossil_config.ConfigInfo.path()
    FOSSIL_DIFF: str = fossil_config.ConfigDiff.path()
    FOSSIL_CAT: str = fossil_config.ConfigCat.path()
    FOSSIL_BRANCH: str = fossil_config.ConfigBranch.path()
    FOSSIL_ADD: str = fossil_config.ConfigAdd.path()
    FOSSIL_COMMIT: str = fossil_config.ConfigCommit.path()

    @staticmethod
    def default_error(context: str):
        """Default Exception Context Code"""
        if not isinstance(context, str):
            raise TypeError('todo')

        return (
            f'{context.value}{msg.Default.DOT.value}{msg.Default.ERROR.value}'
        )
