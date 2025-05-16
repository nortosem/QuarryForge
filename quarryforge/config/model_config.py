"""Model Configuration

#TODO
"""
from typing import NamedTuple, Tuple

from quarryforge.config import root


__all__ = ['FOSSIL_REPO_CONFIG','FOSSIL_COMMIT_CONFIG']


class ModelConfig(NamedTuple):
    """Model Config

    Define the module path base for all models
    """
    PATH = f'{root.PACKAGE.name}.{root.MODULE.model}'

    @classmethod
    def path(cls, sub_path: str) -> str:
        return f'{cls.PATH}.{sub_path}'

model_config: ModelConfig = ModelConfig()


class ConfigFossilRepo(NamedTuple):
    """FossilRepo Configuration

    The slots for a fossil repository.

    Attributes:
        FILE: the full path to a fossil repository
    """
    file = '_file'

    @classmethod
    def slots(cls) -> Tuple[str, ...]:
        return tuple(cls._fields)

    @classmethod
    def field_name(cls):
        return cls.file.value[1:]

    @classmethod
    def path(cls):
        return model_config.path(root.MODEL.fossil_repo)


FOSSIL_REPO_CONFIG: ConfigFossilRepo = ConfigFossilRepo()
"""Global constant for FossilRepo configuration."""

class ConfigFossilCommit(NamedTuple):
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
    uuid = 'uuid'
    date = 'date'
    author = 'author'
    comment = 'comment'
    branch = 'branch'
    tags = 'tags'
    phase = 'phase'
    changes = 'changes'

    @classmethod
    def slots(cls) -> Tuple[str, ...]:
        return tuple(cls._fields)

    @classmethod
    def path(cls):
        return model_config.path(root.MODEL.fossil_commit)


FOSSIL_COMMIT_CONFIG: ConfigFossilCommit = ConfigFossilCommit()
"""Global constant for FossilCommit configuration."""
