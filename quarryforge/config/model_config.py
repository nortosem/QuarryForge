"""Model-Specific Configuration Module.

This module provides detailed configurations for the classes defined in the
model module.

Attributes:
    BASE_MODEL (BaseModelConfig):
        An instance providing base path utilities for models.
    FOSSIL_REPO_CONFIG (ConfigFossilRepo):
        Configuration specific to the FossilRepo model.
    FOSSIL_COMMIT_CONFIG (ConfigFossilCommit):
        Configuration specific to the FossilCommit model.
"""
from typing import List, NamedTuple, Tuple


__all__: List[str] = ['FOSSIL_REPO','FOSSIL_COMMIT', 'FOSSIL_TIMELINE']


class ConfigFossilRepo(NamedTuple):
    """Configuration for the FossilRepo model.

    Defines the file attribute and provides utility methods related to the
    `FossilRepo` model. Field_name metho provides public name property for a
    Fossil Repository.

    Attributes:
        file (str): Stores the string '_file'. This is the internal attribute
        name for the immutable FossilRepo class.
    """
    file: str = '_file'
    is_new: str = '_is_new'
    workdir: str = '_workdir'

    def slots(self) -> Tuple[str]:
        """Get field values to define FossilRepo slots.

        Returns:
            tuple: Returns the internal field names for FossilRepo class.
        """
        return tuple(getattr(self, field) for field in self._fields)


FOSSIL_REPO: ConfigFossilRepo = ConfigFossilRepo()
"""Global constant for FossilRepo configuration."""


class ConfigFossilCommit(NamedTuple):
    """Configuration for the FossilCommit model.

    Defines attributes (field names) and provides utility methods related to the
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

    def slots(self) -> Tuple[str]:
        """Get field values to define FossilCommit slots.

        Returns:
            tuple: Returns the internal field names for FossilCommit class.
        """
        return tuple(getattr(self, field) for field in self._fields)


FOSSIL_COMMIT: ConfigFossilCommit = ConfigFossilCommit()
"""Global constant for FossilCommit configuration."""


class ConfigFossilTimeline(NamedTuple):
    """Configuration for the FossilTimeline model"""
    commits: str = 'commits'


FOSSIL_TIMELINE: ConfigFossilTimeline = ConfigFossilTimeline()
