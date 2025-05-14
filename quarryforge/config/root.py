"""Root Config Module

#TODO
"""
from enum import Enum
from typing import Tuple


class Valid(Enum):
    """Valid

    Define class method to return member values as a tuple.
    """
    QUARRYFORGE = 'quarryforge'

    @classmethod
    def slots(cls) -> Tuple[str, ...]:
        return tuple(slot.value for slot in cls)



class Config(Enum):
    """Config

    Define class method to return config dictionary.
    """
    @classmethod
    def get(cls):
        return {element.name: element.value for element in cls}


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


class TopSubPackages(Valid):
    """Top level subpackages

    """
    CONFIG = 'config'
    EXCEPTIONS = 'exceptions'
    UTIL = 'util'


class ModelNames(Valid):
    """ModelNames


    """
    FOSSIL_COMMIT = 'FossilCommit'
    FOSSIL_REPO = 'FossilRepo'
    FOSSIL_TIMELINE = 'FossilTimeline'


class UtilNames(Valid):
    """Utility Names

    """
    FOSSIL_UTIL = 'fossil_util'
    MAIN_UTIL = 'main_util'
    META_UTIL = 'meta'
    MODEL_UTIL = 'model_util'
