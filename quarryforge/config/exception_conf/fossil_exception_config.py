"""Fossil Exception Configuration Module


"""
from typing import NamedTuple

from quarryforge.config import fossil_config
from quarryforge.config.exception_conf import base_exception_config
from quarryforge.config.exception_conf import exception_config as msg
from quarryforge.config import root
from quarryforge.meta import immutable


__all__ = [
    'ERROR_FIELD',
    'DefaultCode',
    'DefaultMessage',
]


class ConfigFossilErrorField(NamedTuple):
    """Define the fossil error field configuration"""
    cmd: str = 'cmd'
    return_code: str = 'returncode'
    stdout: str = 'stdout'
    stderr: str = 'stderr'
    timeout: str = 'timeout'


ERROR_FIELD: ConfigFossilErrorField = ConfigFossilErrorField()


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
            f'{context}.{msg.Default.ERROR}')


class DefaultCode(metaclass=immutable.Namespace):
    """The Default Exception Codes for Fossil Exceptions."""
    fossil_process: str = FossilErrorContext.default_error(
        FossilErrorContext.FOSSIL_PROCESS)
    fossil_timeout: str = FossilErrorContext.default_error(
        FossilErrorContext.FOSSIL_TIMEOUT)
    fossil_timeline: str = FossilErrorContext.default_error(
        FossilErrorContext.FOSSIL_TIMELINE)
    fossil_setup: str = FossilErrorContext.default_error(
        FossilErrorContext.FOSSIL_SETUP)
    fossil_info: str = FossilErrorContext.default_error(
        FossilErrorContext.FOSSIL_SETUP)
    fossila_diff: str = FossilErrorContext.default_error(
        FossilErrorContext.FOSSIL_DIFF)
    fossil_cat: str = FossilErrorContext.default_error(
        FossilErrorContext.FOSSIL_CAT)
    fossil_branch: str = FossilErrorContext.default_error(
        FossilErrorContext.FOSSIL_BRANCH)
    fossil_add: str = FossilErrorContext.default_error(
        FossilErrorContext.FOSSIL_ADD)
    fossil_commit: str = FossilErrorContext.default_error(
        FossilErrorContext.FOSSIL_COMMIT)


class DefaultMessage(metaclass=immutable.Namespace):
    """The Default Exception Messages for Fossil Exceptions."""
    base_message: str = (
        f'{base_exception_config.DefaultMessage.unexpected_error}'
        f'.{root.Module.fossil}'
    )
    fossil_process: str = f'{base_message}: CalledProcessError.'
    fossil_timeout: str = f'{base_message}: TimeoutError.'
    fossil_timeline: str = f'{base_message}.{root.FossilCommand.timeline}'
    fossil_setup: str = f'{base_message}.{root.FossilCommand.setup}'
    fossil_info: str = f'{base_message}.{root.FossilCommand.info}'
    fossila_diff: str = f'{base_message}.{root.FossilCommand.diff}'
    fossil_cat: str = f'{base_message}.{root.FossilCommand.cat}'
    fossil_branch: str = f'{base_message}.{root.FossilCommand.branch}'
    fossil_add: str = f'{base_message}.{root.FossilCommand.add}'
    fossil_commit: str = f'{base_message}.{root.FossilCommand.commit}'
