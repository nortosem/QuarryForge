"""Root Configuration Module for the QuarryForge Application.

This module defines various constants and structures used
throughout the QuarryForge application. It centralizes names for packages,
modules, sub-packages, data models, Fossil SCM commands, and utility modules.

Attributes:
    PACKAGE (Package): Name for the main application package.
    MODULE (Module): Names for top-level modules within the application.
    SUB_PACKAGE (SubPackage): Names for sub-packages.
    MODEL (Model): Data model names.
    FOSSIL_COMMAND (FossilCommand): Fossil SCM command names.
    UTIL_MODULE (UtilModule): Utility module names.
"""
from typing import NamedTuple


__all__: list = [
    'PACKAGE',
    'MODULE',
    'SUB_PACKAGE',
    'META_MODULE',
    'MODEL',
    'FOSSIL_COMMAND',
    'UTIL_MODULE'
]


class Package(NamedTuple):
    """Application package name"""
    name: str = 'quarryforge'


PACKAGE: Package = Package()
"""Global constant for the main package name."""

class Module(NamedTuple):
    """Defines names for top-level modules within the application.

    Python files residing directly under the main package
    directory (e.g., `quarryforge/fossil.py`).

    Attributes:
        fossil (str): Name of the module handling Fossil SCM interactions.
        main (str): Name of the main application or entry point module.
        model (str): Name of the module defining core data models or structures.
    """
    fossil: str = 'fossil'
    main: str = 'main'
    model: str = 'model'


MODULE: Module = Module()
"""Global constant for top-level module names."""


class SubPackage(NamedTuple):
    """Defines names for top-level sub-packages.

    These are the directories containing an `__init__.py` file, residing
    directly under the main package directory (e.g., `quarryforge/config/`).

    Attributes:
        config (str): Name of the sub-package for application configurations.
        exception (str): Name of the sub-package for custom exceptions.
        util (str): Name of the sub-package for utility modules.
    """
    config: str = 'config'
    exception: str = 'exception'
    meta: str = 'meta'
    util: str = 'util'


SUB_PACKAGE: SubPackage = SubPackage()
"""Global constant for sub-package name configurations."""


class MetaModule(NamedTuple):
    """Defines names for modules within the utility sub-package (`meta`).

    These strings represent the file names (without the `.py` extension)
    of modules located under the `quarryforge/util/` directory.

    Attributes:
        assembler: The assembler module for package error handling.
        immutable: The immutable module defines the metaclasses for immutable
            class creation.
    """
    assembler: str = 'assembler'
    immutable: str = 'immutable'


META_MODULE: MetaModule = MetaModule()
"""Global constant for meta subpackage modules."""

class Model(NamedTuple):
    """Defines names for quarryforge data models.

    Attributes:
        fossil_commit (str):
            Name of the model representing a Fossil commit.
        fossil_repo (str):
            Name of the model representing a Fossil repository.
        fossil_timeline (str):
            Name of the model representing a Fossil timeline entry.
    """
    fossil_commit: str = 'FossilCommit'
    fossil_repo: str = 'FossilRepo'
    fossil_timeline: str = 'FossilTimeline'


MODEL: Model = Model()
"""Global constant for data model names."""


class FossilCommand(NamedTuple):
    """Defines Fossil SCM commands.

    These are the classes used to provide access to fossil commands via
    subprocess.

    Attributes:
        timeline (str): Identifier for the Fossil 'timeline' command.
        setup (str): Identifier for Fossil repository 'setup' operations.
        info (str): Identifier for the Fossil 'info' command.
        diff (str): Identifier for the Fossil 'diff' command.
        cat (str): Identifier for the Fossil 'cat' command.
        branch (str): Identifier for Fossil 'branch' related commands.
        add (str): Identifier for the Fossil 'add' command.
        commit (str): Identifier for the Fossil 'commit' command.
    """
    timeline: str = 'Timeline'
    setup: str = 'Setup'
    info: str = 'Info'
    diff: str = 'Diff'
    cat: str = 'Cat'
    branch: str = 'Branch'
    add: str = 'Add'
    commit: str = 'Commit'


FOSSIL_COMMAND: FossilCommand = FossilCommand()
"""Global constant for Fossil SCM command names."""


class UtilModule(NamedTuple):
    """Defines names for modules within the utility sub-package (`util`).

    These strings represent the file names (without the `.py` extension)
    of modules located under the `quarryforge/util/` directory.

    Attributes:
        error_data_util (str):
            Name of the utility module for handling error data.
        fossil_util (str):
            Name of the utility module for Fossil-specific helpers.
        main_util (str):
            Name of the utility module for general application utilities.
        model_util (str):
            Name of the utility module for model-related helpers.
    """
    error_data_util: str = 'error_data_util'
    fossil_util: str = 'fossil_util'
    main_util: str = 'main_util'
    model_util: str = 'model_util'


UTIL_MODULE: UtilModule = UtilModule()
"""Global constant for utility module names."""
