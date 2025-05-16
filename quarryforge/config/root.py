"""Root Config Module

#TODO
"""
from typing import NamedTuple, Tuple


__all__ = [PACKAGE, MODULE, SUB_PACKAGE, MODEL, FOSSIL_COMMAND, UTIL_MODULE]

class Config(Enum):
    """Config

    Define class method to return config dictionary.
    """
    @classmethod
    def get(cls):
        return {element.name: element.value for element in cls}


class Package(NamedTuple):
    """Package name"""
    name: str


PACKAGE: Package = Package(name='quarryforge')


class Module(NamedTuple):
    """Top level Modules

    The module names in the top-level package directory.

    Attributes:
        fossil: the fossil module
        main: the main module
        meta: the meetaclass module
        model: the model module
    """
    fossil: str
    main: str
    model: str


MODULE: Module = Module(fossil='fossil', main='main', model='model')


class SubPackage(NamedTuple):
    """Top level subpackages

    Attributes:
        config: the configuration subpackage
        exception: the exception subpackage
        util: the utility subpackage
    """
    config: str
    exception: str
    util: str


SUB_PACKAGE: SubPackage = SubPackage(
    config = 'config',
    exception = 'exception',
    util = 'util'
)


class Model(NamedTuple):
    """Model names

    Attributes:

    """
    fossil_commit: str
    fossil_repo: str
    fossil_timeline:str


MODEL: Model = Model(
    fossil_commit = 'FossilCommit',
    fossil_repo = 'FossilRepo',
    fossil_timeline = 'FossilTimeline'
)


class FossilCommand(NamedTuple):
    """Fossil Command names"""
    timeline: str
    setup: str
    info: str
    diff: str
    cat: str
    branch: str
    add: str
    commit: str


FOSSIL_COMMAND: FossilCommand = FossilCommand(
    timeline = 'Timeline',
    setup = 'Setup',
    info = 'Info',
    diff = 'Diff',
    cat = 'Cat',
    branch = 'Branch',
    add = 'Add',
    commit = 'Commit'
)


class UtilModule(NamedTuple):
    """Utility Module Names

    """
    error_data_util: str
    fossil_util: str
    main_util: str
    model_util: str


UTIL_MODULE: UtilModule = UtilModule(
    error_data_util = 'error_data_util'
    fossil_util = 'fossil_util'
    main_util = 'main_util'
    model_util = 'model_util'
)
