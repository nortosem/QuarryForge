"""Model-Specific Configuration Module.

This module Provide detailed configurations for the classes defined in the
model module.
"""

from typing import NamedTuple

__all__: list[str] = [
    'fossil_repo_config',
    'fossil_commit_config',
    'fossil_timeline_config',
]


class ConfigFossilRepo(NamedTuple):
    """Configuration for the FossilRepo model.

    Defines the file attribute and Provide utility methods related to the
    `FossilRepo` model. Field_name metho Provide public name property for a
    Fossil Repository.

    Attributes:
        file (str): Stores the string '_file'. This is the internal attribute
        name for the immutable FossilRepo class.

    """

    file: str = '_file'
    is_new: str = '_is_new'
    workdir: str = '_workdir'

    def slots(self) -> tuple[str]:
        """Get field values to define FossilRepo slots.

        Returns:
            tuple: Returns the internal field names for FossilRepo class.

        """
        return tuple(getattr(self, field) for field in self._fields)


def fossil_repo_config() -> ConfigFossilRepo:
    """Provide the configuration for the FossilRepo model."""
    return ConfigFossilRepo()


class ConfigFossilCommit(NamedTuple):
    """Configuration for the FossilCommit model.

    Defines attributes (field names) and Provide utility methods related to the
    `FossilCommit` model.

    Attributes:
        uuid (str): Field name for the commit's unique identifier (hash).
        date (str): Field name for the commit's date.
        author (str): Field name for the commit's author.
        comment (str): Field name for the commit's comment/message.
        branch (str): Field name for the commit's branch.
        tags (str): Field name for the commit's tags.
        phase (str): Field name for the commit's phase
        changes (str): Field name for the summary of changes in the commit.

    """

    uuid: str = '_uuid'
    date: str = '_date'
    author: str = '_author'
    comment: str = '_comment'
    branch: str = '_branch'
    tags: str = '_tags'
    phase: str = '_phase'
    changes: str = '_changes'

    def slots(self) -> tuple[str]:
        """Get field values to define FossilCommit slots.

        Returns:
            tuple: Returns the internal field names for FossilCommit class.

        """
        return tuple(getattr(self, field) for field in self._fields)


def fossil_commit_config() -> ConfigFossilCommit:
    """Provide the configuration for the FossilCommit model."""
    return ConfigFossilCommit()


class ConfigFossilTimeline(NamedTuple):
    """Configuration for the FossilTimeline model."""

    commits: str = 'commits'


def fossil_timeline_config() -> ConfigFossilTimeline:
    """Provide the configuration for the FossilTimeline model."""
    return ConfigFossilTimeline()


class ConfigValidation(NamedTuple):
    """Defined constants for model validation."""

    PAIR = 2
    KEY = 0
    VALUE = 1


def validation_config() -> ConfigValidation:
    """Provide an instance for validation constants."""
    return ConfigValidation()
