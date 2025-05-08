"""Models Configuration

#TODO
"""
from quarryforge.config.root import Valid


class ConfigFossilRepo(Valid):
    """FossilRepo Configuration

    The slots for a fossil repository.

    Attributes:
        FILE: the full path to a fossil repository
    """
    FILE = '_file'


class ConfigCommit(Valid):
    """Commit Configuration

    The slots for a Commit.

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
