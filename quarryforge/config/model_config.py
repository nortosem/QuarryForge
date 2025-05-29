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
from typing import List, NamedTuple


__all__: List = ['FOSSIL_REPO','FOSSIL_COMMIT', 'FOSSIL_TIMELINE']


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

    def field_name(self) -> str:
        """Get public property field name.

        Returns:
            str: The public field name 'file' from the internal '_file' slot.
        """
        return str(self.file)[1:]


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
    uuid: str = 'uuid'
    date: str = 'date'
    author: str = 'author'
    comment: str = 'comment'
    branch: str = 'branch'
    tags: str = 'tags'
    phase: str = 'phase'
    changes: str = 'changes'


FOSSIL_COMMIT: ConfigFossilCommit = ConfigFossilCommit()
"""Global constant for FossilCommit configuration."""


class ConfigFossilTimeline(NamedTuple):
    """Configuration for the FossilTimeline model"""
    commits: str = 'commits'


FOSSIL_TIMELINE: ConfigFossilTimeline = ConfigFossilTimeline()
