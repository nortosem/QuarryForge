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


class TopModules(Valid):
    """Top level Modules

    The module names in the top-level package directory.

    Attributes:
        FOSSIL: the fossil module
        MAIN: the main module
        MODEL: the model module
        PROTOCOL: the protocol module
    """
    FOSSIL = 'fossil'
    MAIN = 'main'
    MODEL = 'model'
    PROTOCOL = 'protocol'


class ModelNames(Valid):
    """ModelNames


    """
    ARG_STRING = 'ArgString'
    COMMIT = 'Commit'
    CAT_ARGS = 'CatArgs'
    FOSSIL_REPO = 'FossilRepo'
    FOSSIL_REBUILD = 'FossilRebuild'
    GET_TIMELINE_ARG = 'GetTimelineArg'
    INFO_ARGS = 'InfoArg'
    DIFF_ARGS = 'DiffArg'
    TIMELINE = 'Timeline'
