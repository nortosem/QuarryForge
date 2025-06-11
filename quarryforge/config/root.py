"""Root Configuration Module for the QuarryForge Application.

This module defines various constants and structures used
throughout the QuarryForge application. It centralizes names for packages,
modules, sub-packages, data models, Fossil SCM commands, and utility modules.

Attributes:
    Package (StrEnum): Name for the main application package.
    Module (StrEnum): Names for top-level modules within the application.
    SubPackage (StrEnum): Names for sub-packages.
    Model (StrEnum): Data model names.
    FossilModule (StrEnum): Fossil SCM command names.
    UtilModule (StrEnum): Utility module names.
"""
from enum import StrEnum
from typing import List


__all__: List[str] = [
    'Package',
    'Module',
    'SubPackage',
    'MetaModule',
    'Model',
    'FossilModule',
    'UtilModule'
]


class Package(StrEnum):
    """Application package name"""
    NAME = 'quarryforge'


class Module(StrEnum):
    """Defines names for top-level modules within the application.

    Python files residing directly under the main package
    directory (e.g., `quarryforge/fossil.py`).

    Attributes:
        fossil (str): Name of the module handling Fossil SCM interactions.
        main (str): Name of the main application or entry point module.
        model (str): Name of the module defining core data models or structures.
    """
    FOSSIL = 'fossil'
    MAIN = 'main'
    MODEL = 'model'


class SubPackage(StrEnum):
    """Defines names for top-level sub-packages.

    These are the directories containing an `__init__.py` file, residing
    directly under the main package directory (e.g., `quarryforge/config/`).

    Attributes:
        config (str): Name of the sub-package for application configurations.
        exception (str): Name of the sub-package for custom exceptions.
        util (str): Name of the sub-package for utility modules.
    """
    CONFIG = 'config'
    EXCEPTION = 'exception'
    FOSSIL = 'fossil'
    META = 'meta'
    UTIL = 'util'


class MetaModule(StrEnum):
    """Defines names for modules within the utility sub-package (`meta`).

    These strings represent the file names (without the `.py` extension)
    of modules located under the `quarryforge/util/` directory.

    Attributes:
        assembler: The assembler module for package error handling.
        immutable: The immutable module defines the metaclasses for immutable
            class creation.
    """
    ASSEMBLER = 'assembler'
    IMMUTABLE = 'immutable'


class Model(StrEnum):
    """Defines names for quarryforge data models.

    Attributes:
        fossil_commit (str):
            Name of the model representing a Fossil commit.
        fossil_repo (str):
            Name of the model representing a Fossil repository.
        fossil_timeline (str):
            Name of the model representing a Fossil timeline entry.
    """
    FOSSIL_COMMIT = 'FossilCommit'
    FOSSIL_REPO = 'FossilRepo'
    FOSSIL_TIMELINE = 'FossilTimeline'


class FossilModule(StrEnum):
    """Defines Fossil SCM commands.

    These are the modules used to provide access to fossil commands via
    subprocess.

    Attributes:
        timeline (str): Module for the Fossil 'timeline' command.
        setup (str): Identifier for Fossil repository 'setup' operations.
        info (str): Identifier for the Fossil 'info' command.
        diff (str): Identifier for the Fossil 'diff' command.
        cat (str): Identifier for the Fossil 'cat' command.
        branch (str): Identifier for Fossil 'branch' related commands.
        add (str): Identifier for the Fossil 'add' command.
        commit (str): Identifier for the Fossil 'commit' command.
    """
    PROCESS = 'FossilProcess'
    TIMEOUT = 'FossilTimeoutExpired'
    TIMELINE = 'Timeline'
    SETUP = 'Setup'
    INFO = 'Info'
    DIFF = 'Diff'
    CAT = 'Cat'
    BRANCH = 'Branch'
    ADD = 'Add'
    COMMIT = 'Commit'


class UtilModule(StrEnum):
    """Defines names for modules within the utility sub-package (`util`).

    These strings represent the file names (without the `.py` extension)
    of modules located under the `quarryforge/util/` directory.

    Attributes:
        fossil_util (str):
            Name of the utility module for Fossil-specific helpers.
        main_util (str):
            Name of the utility module for general application utilities.
        model_util (str):
            Name of the utility module for model-related helpers.
    """
    DECORATOR = 'decorator'
    FOSSIL_UTIL = 'fossil_util'
    MAIN_UTIL = 'main_util'
    MODEL_UTIL = 'model_util'
    VALIDATION_UTIL = 'validation_util'
