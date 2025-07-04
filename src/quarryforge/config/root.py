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

from enum import StrEnum, auto

__all__: list[str] = [
    'Package',
    'Module',
    'SubPackage',
    'MetaModule',
    'Model',
    'FossilModule',
    'UtilModule',
]


class Package(StrEnum):
    """Define the application package name."""

    NAME = 'quarryforge'


class Module(StrEnum):
    """Defines names for top-level modules within the application.

    Python files residing directly under the main package
    directory (e.g., `quarryforge/fossil.py`).

    Attributes:
        main (str): Name of the main application or entry point module.
        model (str): Name of the module defining core data models or structures.

    """

    MAIN = auto()
    MODEL = auto()


class SubPackage(StrEnum):
    """Defines names for top-level sub-packages.

    These are the directories containing an `__init__.py` file, residing
    directly under the main package directory (e.g., `quarryforge/config/`).

    Attributes:
        CONFIG (str): Name of the sub-package for application configurations.
        EXCEPTION (str): Name of the sub-package for custom exceptions.
        FOSSIL (str): Name of the sub-package for fossil command modules.
        META (str): Name of the sub-package for metaclass modules.
        UTIL (str): Name of the sub-package for utility modules.

    """

    CONFIG = auto()
    EXCEPTION = auto()
    FOSSIL = auto()
    META = auto()
    UTIL = auto()


class MetaModule(StrEnum):
    """Defines names for modules within the utility sub-package (`meta`).

    These strings represent the file names (without the `.py` extension)
    of modules located under the `quarryforge/util/` directory.

    Attributes:
        ASSEMBLER: The assembler module for package error handling.
        IMMUTABLE: The immutable module defines the metaclasses for immutable
            class creation.

    """

    ASSEMBLER = auto()
    IMMUTABLE = auto()


class Model(StrEnum):
    """Defines names for quarryforge data models.

    Attributes:
        FOSSIL_COMMIT (str):
            Name of the model representing a Fossil commit.
        FOSSIL_REPO (str):
            Name of the model representing a Fossil repository.
        FOSSIL_TIMELINE (str):
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
        TIMELINE (str): Module for the Fossil 'timeline' command.
        SETUP (str): Module for Fossil repository 'setup' operations.
        INFO (str): Module for the Fossil 'info' command.
        DIFF (str): Module for the Fossil 'diff' command.
        CAT (str): Module for the Fossil 'cat' command.
        BRANCH (str): Module for Fossil 'branch' related commands.
        ADD (str): Module for the Fossil 'add' command.
        COMMIT (str): Module for the Fossil 'commit' command.
        CONTROL (str): Module for Fossil scm control commands.

    """

    TIMELINE = 'Timeline'
    SETUP = 'Setup'
    INFO = 'Info'
    DIFF = 'Diff'
    CAT = 'Cat'
    BRANCH = 'Branch'
    ADD = 'Add'
    COMMIT = 'Commit'
    CONTROL = 'Control'


class UtilModule(StrEnum):
    """Defines names for modules within the utility sub-package (`util`).

    These strings represent the file names (without the `.py` extension)
    of modules located under the `quarryforge/util/` directory.

    Attributes:
        DECORATOR (str):
            Name of the module for decorators used in quarryforge.
        FOSSIL_UTIL (str):
            Name of the utility module for Fossil-specific helpers.
        MAIN_UTIL (str):
            Name of the utility module for general application utilities.
        MODEL_UTIL (str):
            Name of the utility module for model-related helpers.
        VALIDATION_UTIL (str):
            Name of the helper-utility for the model utility.

    """

    DECORATOR = auto()
    FOSSIL_UTIL = auto()
    MAIN_UTIL = auto()
    MODEL_UTIL = auto()
    VALIDATION_UTIL = auto()
