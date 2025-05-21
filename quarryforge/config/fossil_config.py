"""Fossil Configuration

#TODO
"""
from quarryforge.config import root
from quarryforge.meta import immutable


class ConfigFossil(metaclass=immutable.Namespace):
    """Config Fossil

    Define the module path base for all fossil Namespaces.
    """
    default_timeout = 180 #seconds
    base_path = (
        f'{root.PACKAGE.name}.{root.Module.fossil}'
    )

    @classmethod
    def path(cls, sub_path: str) -> str:
        return f'{cls.base_path}.{sub_path}'


class ConfigProcess(metaclass=immutable.Namespace):
    """ConfigProcess


    """
    @staticmethod
    def path():
        return ConfigFossil.path('CalledProcessError')


class ConfigTimeout(metaclass=immutable.Namespace):
    """ConfigTimeout


    """
    @staticmethod
    def path():
        return ConfigFossil.path('TimeoutExpiredError')


class ConfigTimeline(metaclass=immutable.Namespace):
    """ConfigTimeline


    """
    @staticmethod
    def path():
        return ConfigFossil.path(root.FOSSIL_COMMAND.timeline)


class ConfigSetup(metaclass=immutable.Namespace):
    """ConfigSetup


    """
    @staticmethod
    def path():
        return ConfigFossil.path(root.FOSSIL_COMMAND.setup)


class ConfigInfo(metaclass=immutable.Namespace):
    """ConfigInfo


    """
    @staticmethod
    def path():
        return ConfigFossil.path(root.FOSSIL_COMMAND.info)


class ConfigDiff(metaclass=immutable.Namespace):
    """ConfigDiff


    """
    @staticmethod
    def path():
        return ConfigFossil.path(root.FOSSIL_COMMAND.diff)


class ConfigCat(metaclass=immutable.Namespace):
    """ConfigCat


    """
    @staticmethod
    def path():
        return ConfigFossil.path(root.FOSSIL_COMMAND.cat)


class ConfigBranch(metaclass=immutable.Namespace):
    """ConfigBranch


    """
    @staticmethod
    def path():
        return ConfigFossil.path(root.FOSSIL_COMMAND.branch)


class ConfigAdd(metaclass=immutable.Namespace):
    """ConfigAdd


    """
    @staticmethod
    def path():
        return ConfigFossil.path(root.FOSSIL_COMMAND.add)


class ConfigCommit(metaclass=immutable.Namespace):
    """ConfigCommit


    """
    @staticmethod
    def path():
        return ConfigFossil.path(root.FOSSIL_COMMAND.commit)
