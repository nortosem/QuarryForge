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
from typing import NamedTuple, Tuple

from quarryforge.config import root


__all__ = ['FOSSIL_REPO','FOSSIL_COMMIT']


class BaseModelConfig(NamedTuple):
    """Base configuration for model module paths.

    This class defines a standard base path for all model modules within the
    application and provides a utility method to construct full Python
    dot-paths to specific model modules.

    Class Attributes:
        PATH (str): The base Python module path for all models, constructed from
            `root.PACKAGE.name` and `root.MODULE.model`. For example,
            'quarryforge.model'.
    """
    PATH: str = f'{root.PACKAGE.name}.{root.MODULE.model}'

    @classmethod
    def path(cls, sub_path: str) -> str:
        """Constructs the full Python path to a model module.

        Appends a given model's name to the base `cls.PATH`.

        Args:
            sub_path (str): The specific model module name or sub-path
                (e.g., 'FossilRepo').

        Returns:
            str: The full Python dot-path to the model module
                 (e.g., 'quarryforge.model.FossilRepo').
        """
        return f'{cls.PATH}.{sub_path}'

BASE_MODEL: BaseModelConfig = BaseModelConfig()
"""Instance of ModelConfig, providing access to model path utilities."""


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

    def slots(self) -> Tuple[str, ...]:
        """Returns the field names defined in this NamedTuple.

        Returns:
            Tuple[str, ...]:
            A tuple containing the names of the fields
        """
        tuple(getattr(self, field) for field in self._fields)

    def field_name(self) -> str:
        """Get public property field name.

        Returns:
            str: The public field name 'file' from the internal '_file' slot.
        """
        return str(self.file)[1:]


    @classmethod
    def path(cls) -> str:
        """Returns the full Python module path for the FossilRepo model.

        Returns:
            str: The full Python dot-path 'quarryforge.model.FossilRepo'.
        """
        return BASE_MODEL.path(root.MODEL.fossil_repo)


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
    uuid = 'uuid'
    date = 'date'
    author = 'author'
    comment = 'comment'
    branch = 'branch'
    tags = 'tags'
    phase = 'phase'
    changes = 'changes'

    def slots(self) -> Tuple[str, ...]:
        """Returns the field names defined in this NamedTuple.

        Returns:
            Tuple[str, ...]:
                A tuple containing the names of all fields
        """
        return tuple(
            getattr(
                self,
                self._fields[field]
            ) for field in range(len(self._fields))
        )

    @classmethod
    def path(cls):
        """Returns the full Python module path for the FossilCommit model.

        Returns:
            str: The full Python dot-path 'quarryforge.model.FossilCommit'.
        """
        return BASE_MODEL.path(root.MODEL.fossil_commit)


FOSSIL_COMMIT: ConfigFossilCommit = ConfigFossilCommit()
"""Global constant for FossilCommit configuration."""
