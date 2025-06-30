"""The configuration module for the main module of quarryforge."""

from enum import StrEnum, auto


class ConfigKeys(StrEnum):
    """All of the keys that can be set via CLI or TOML."""

    SOURCE_REPO = auto()
    SOURCE_WORKDIR = auto()
    UPDATED_REPO = auto()
    UPDATED_WORKDIR = auto()
    NEW_USERNAME = auto()
    NEW_EMAIL = auto()
    PROJECT_NAME = auto()
    PROJECT_DESC = auto()


class RequiredKeys(StrEnum):
    """The required keys for any repository update."""

    SOURCE_REPO = ConfigKeys.SOURCE_REPO
    SOURCE_WORKDIR = ConfigKeys.SOURCE_WORKDIR
    UPDATED_REPO = ConfigKeys.UPDATED_REPO
    UPDATED_WORKDIR = ConfigKeys.UPDATED_WORKDIR
    NEW_USERNAME = ConfigKeys.NEW_USERNAME
    NEW_EMAIL = ConfigKeys.NEW_EMAIL
