"""Fossil Configuration

#TODO
"""
from quarryforge.config import root
from quarryforge.meta import immutable


class FossilConfig(metaclass=immutable.Namespace):
    """Fossil Config

    Define the module path base for all models
    """
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
        return FossilConfig.path('CalledProcessError')


class ConfigTimeout(metaclass=immutable.Namespace):
    """ConfigTimeout


    """
    @staticmethod
    def path():
        return FossilConfig.path('TimeoutExpiredError')


class ConfigTimeline(metaclass=immutable.Namespace):
    """ConfigTimeline


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.TIMELINE.value)


class ConfigSetup(metaclass=immutable.Namespace):
    """ConfigSetup


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.SETUP.value)


class ConfigInfo(metaclass=immutable.Namespace):
    """ConfigInfo


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.INFO.value)


class ConfigDiff(metaclass=immutable.Namespace):
    """ConfigDiff


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.DIFF.value)


class ConfigCat(metaclass=immutable.Namespace):
    """ConfigCat


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.CAT.value)


class ConfigBranch(metaclass=immutable.Namespace):
    """ConfigBranch


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.BRANCH.value)


class ConfigAdd(metaclass=immutable.Namespace):
    """ConfigAdd


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.ADD.value)


class ConfigCommit(metaclass=immutable.Namespace):
    """ConfigCommit


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.COMMIT.value)
