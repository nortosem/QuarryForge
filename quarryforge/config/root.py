"""Root Config Module

#TODO
"""
from enum import Enum
from typing import Tuple


class Valid(Enum):
    """Package Enum Validator

    Define class method to return member values as a tuple.
    """
    @classmethod
    def slots(cls) -> Tuple[str]:
        return tuple(slot.value for slot in cls)


class ModelNames(Valid):
    """ModelNames


    """
    REPO_CONFIG = 'RepoConfig'
    COMMIT = 'Commit'
    TIMELINE = 'Timeline'
