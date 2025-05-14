"""Fossil Configuration

#TODO
"""
from quarryforge.config import root
from quarryforge.config.exception_conf import exception_config as msg


class FossilConfig(root.Valid):
    """Fossil Config

    Define the module path base for all models
    """
    PATH = (msg.Default.DOT.value).join([
        root.Valid.QUARRYFORGE.value,
        root.TopModules.FOSSIL.value
    ])

    @classmethod
    def path(cls, sub_path: str) -> str:
        return f'{cls.PATH}.{sub_path}'


class ConfigTimeline(root.Valid):
    """ConfigTimeline


    """
    @classmethod
    def path(cls):
        return ModelConfig.path(root.FossilCommand.TIMELINE.value)


class ConfigSetup(root.Valid):
    """ConfigSetup


    """
    @classmethod
    def path(cls):
        return ModelConfig.path(root.FossilCommand.SETUP.value)


class ConfigInfo(root.Valid):
    """ConfigInfo


    """
    @classmethod
    def path(cls):
        return ModelConfig.path(root.FossilCommand.INFO.value)


class ConfigDiff(root.Valid):
    """ConfigDiff


    """
    @classmethod
    def path(cls):
        return ModelConfig.path(root.FossilCommand.DIFF.value)


class ConfigCat(root.Valid):
    """ConfigCat


    """
    @classmethod
    def path(cls):
        return ModelConfig.path(root.FossilCommand.CAT.value)


class ConfigBranch(root.Valid):
    """ConfigBranch


    """
    @classmethod
    def path(cls):
        return ModelConfig.path(root.FossilCommand.BRANCH.value)


class ConfigAdd(root.Valid):
    """ConfigAdd


    """
    @classmethod
    def path(cls):
        return ModelConfig.path(root.FossilCommand.ADD.value)


class ConfigCommit(root.Valid):
    """ConfigCommit


    """
    @classmethod
    def path(cls):
        return ModelConfig.path(root.FossilCommand.COMMIT.value)
