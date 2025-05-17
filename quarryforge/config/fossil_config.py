"""Fossil Configuration

#TODO
"""
from quarryforge.config import root
from quarryforge.config.exception_conf import exception_config as msg


class FossilConfig(root.Valid):
    """Fossil Config

    Define the module path base for all models
    """
    PATH = (
        f'{root.Valid.QUARRYFORGE.value}'
        f'{msg.Default.DOT.value}'
        f'{root.TopModules.FOSSIL.value}'
    )

    def path(self, sub_path: str) -> str:
        return f'{self.PATH}.{sub_path}'


class ConfigProcess(root.Valid):
    """ConfigProcess


    """
    @staticmethod
    def path():
        return FossilConfig.path('CalledProcessError')


class ConfigTimeout(root.Valid):
    """ConfigTimeout


    """
    @staticmethod
    def path():
        return FossilConfig.path('TimeoutExpiredError')


class ConfigTimeline(root.Valid):
    """ConfigTimeline


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.TIMELINE.value)


class ConfigSetup(root.Valid):
    """ConfigSetup


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.SETUP.value)


class ConfigInfo(root.Valid):
    """ConfigInfo


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.INFO.value)


class ConfigDiff(root.Valid):
    """ConfigDiff


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.DIFF.value)


class ConfigCat(root.Valid):
    """ConfigCat


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.CAT.value)


class ConfigBranch(root.Valid):
    """ConfigBranch


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.BRANCH.value)


class ConfigAdd(root.Valid):
    """ConfigAdd


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.ADD.value)


class ConfigCommit(root.Valid):
    """ConfigCommit


    """
    @staticmethod
    def path():
        return FossilConfig.path(root.FossilCommand.COMMIT.value)
