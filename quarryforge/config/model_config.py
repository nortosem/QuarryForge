"""Models Configuration

#TODO
"""
from quarryforge.config import root
from quarryforge.config.exception_conf import exception_config as msg


class ModelConfig(root.Valid):
    """Model Config

    Define the module path base for all models
    """
    PATH = (
        f'{root.Valid.QUARRYFORGE.value}'
        f'{msg.Default.DOT.value}'
        f'{root.TopModules.MODEL.value}'
    )

    @classmethod
    def path(cls, sub_path: str) -> str:
        return f'{cls.PATH}{msg.Default.DOT.value}{sub_path}'


class ConfigFossilRepo(root.Valid):
    """FossilRepo Configuration

    The slots for a fossil repository.

    Attributes:
        FILE: the full path to a fossil repository
    """
    FILE = '_file'

    @classmethod
    def file(cls):
        return cls.File.value[1:]

    @classmethod
    def path(cls):
        return ModelConfig.path(root.ModelNames.FOSSIL_REPO.value)


class ConfigFossilCommit(root.Valid):
    """Fossil Commit Configuration

    The slots for a fossil checkin.

    Attributes:
        HASH = uuid for a commit entry
        DATE = date for a commit entry
        AUTHOR = author for a commit entry
        COMMENT = comment for a commit entry
        BRANCH = branch for a commit entry
        TAGS = tags for a commit entry
        PHASE = phase for a commit entry
        CHANGES = changes for a commit entry
    """
    HASH = 'uuid'
    DATE = 'date'
    AUTHOR = 'author'
    COMMENT = 'comment'
    BRANCH = 'branch'
    TAGS = 'tags'
    PHASE = 'phase'
    CHANGES = 'changes'

    @classmethod
    def path(cls):
        return ModelConfig.path(root.ModelNames.FOSSIL_COMMIT.value)
