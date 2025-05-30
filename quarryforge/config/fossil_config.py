"""Fossil Configuration

This module defines configurations specific to Fossil SCM operations,
including default timeouts, command structures, and output parsing patterns.
It centralizes all Fossil-related constant definitions.
"""
from typing import NamedTuple
import re

from quarryforge.meta import immutable


__all__: list = [
    'COMMAND',
    'TIMELINE_DATA',
    'INFO_DATA',
    'FOSSIL'
]


class ConfigCommand(NamedTuple):
    """The permitted fossil commands and options."""
    FOSSIL: str = 'fossil'
    REPO: str = '-R'
    TIMELINE: str = 'timeline'
    VERBOSE: str = '--verbose'
    TYPE: str = '--type'
    CI: str = 'ci'
    LIMIT: str = '--limit'
    NO_LIMIT: str = '0'
    FULL: str = '--full'
    NEW: str = 'new'
    USER: str = 'user'
    DEFAULT: str = 'default'
    CONTACT: str = 'contact'
    TEMPLATE: str = '--template'
    ADMIN_USER: str = '--admin-user'
    PROJECT_NAME: str = '--project-name'
    PROJECT_DESC: str = '--project-desc'
    BRANCH: str = 'branch'
    LIST: str = 'list'
    ALL: str = '--all'
    CLOSED: str = '--closed'
    INFO: str = 'info'
    DIFF: str = 'diff'
    BRIEF: str = '--brief'
    FROM: str = '--from'
    TO: str = '--to'
    CAT: str = 'cat'
    VERSION: str = '-r'
    ADD: str = 'add'
    COMMIT: str = 'commit'


COMMAND: ConfigCommand = ConfigCommand()
"""Global constant for fossil command arguments."""


class ConfigTimelineData(NamedTuple):
    """Timeline Data

    The fields and patterns used to parse commits from the timeline output.
    """
    INIT_CHECKIN: str = 'initial empty check-in'
    END_MARK: str = '+++ end of timeline'
    COMMITS_KEY: str = 'commits'
    COMMIT_SEP: str = '\\n(?=Commit:\\s+)'
    HASH_KEY: str = 'uuid'
    HASH_PATTERN: str = '^(?P<label>Commit:\\s+)(?P<uuid>[0-9a-f]+)$'
    DATE_KEY: str = 'date'
    DATE_PATTERN: str = '^(?P<label>Date):\\s+(?P<date>.+)$'
    AUTHOR_KEY: str = 'author'
    AUTHOR_PATTERN: str = '^(?P<label>Author):\\s+(?P<author>.+)?'
    COMMENT_KEY: str = 'comment'
    COMMENT_PATTERN: str = '^(?P<label>Comment):\\s+(?P<comment>.+)$'
    BRANCH_KEY: str = 'branch'
    BRANCH_PATTERN: str = '^(?P<label>Branch):\\s+(?P<branch>.+)$'
    TAGS_KEY: str = 'tags'
    TAGS_PATTERN: str = '^(?P<label>Tags):\\s+(?P<tags>.+)$'
    TAG_REGEX: str = '?P<tag>[\\w-]+'
    PHASE_KEY: str = 'phase'
    PHASE_PATTERN: str = (
        '^(?P<label>Phase):\\s+\\*?(?P<phase>LEAF|PUBLISHED|FROZEN)?\\*?'
    )
    CHANGES_KEY: str = 'changes'
    CHANGE_PATTERN: str = (
        '^\\s+(?P<change>ADDED|EDITED|DELETED)\\s(?P<filename>.+)$'
    )
    PATH_PATTERN: str = '^(?P<path>.*[\\/])?(?P<file>[^/\\\\]+$)'

    def commit_pattern(self) -> re.Pattern:
        """Regex pattern to split timeline output into individual commits."""
        return re.compile(f'{self.COMMIT_SEP}')

    def hash_pattern(self) -> re.Pattern:
        """Regex pattern for extracting commit hash (UUID)."""
        return re.compile(f'{self.HASH_PATTERN}')

    def date_pattern(self) -> re.Pattern:
        """Regex pattern for extracting commit date."""
        return re.compile(f'{self.DATE_PATTERN}')

    def author_pattern(self) -> re.Pattern:
        """Regex pattern for extracting commit author."""
        return re.compile(f'{self.AUTHOR_PATTERN}')

    def comment_pattern(self) -> re.Pattern:
        """Regex pattern for extracting commit comment."""
        return re.compile(f'{self.COMMENT_PATTERN}')

    def branch_pattern(self) -> re.Pattern:
        """Regex pattern for extracting commit branch."""
        return re.compile(f'{self.BRANCH_PATTERN}')

    def tags_pattern(self) -> re.Pattern:
        """Regex pattern for extracting commit tags."""
        return re.compile(f'{self.TAGS_PATTERN}')

    def phase_pattern(self) -> re.Pattern:
        """Regex pattern for extracting commit phase."""
        return re.compile(f'{self.PHASE_PATTERN}')

    def change_pattern(self) -> re.Pattern:
        """Regex pattern for extracting file changes."""
        return re.compile(f'{self.CHANGE_PATTERN}')


TIMELINE_DATA: ConfigTimelineData = ConfigTimelineData()
"""Global constant for timeline data parsing configuration."""


class ConfigInfoData(NamedTuple):
    """Parser for Fossil Info output."""
    INIT_HASH: str = '^comment:\\s+(?P<init>)\\s.+\\n'
    PARENT_KEY: str = 'parent'
    PARENT_DATA_PATTERN: str = '^parent:\\s+(?P<uuid>.+?)\\s.+\\n'

    def init_pattern(self) -> re.Pattern:
        """Regex pattern for identifying initial commit info output."""
        return re.compile(self.INIT_HASH)

    def parent_pattern(self) -> re.Pattern:
        """Regex pattern for extracting parent commit hash from info output."""
        return re.compile(self.PARENT_DATA_PATTERN)


INFO_DATA: ConfigInfoData = ConfigInfoData()
"""Global constant for info data parsing patterns."""


class ConfigFossil(metaclass=immutable.Namespace):
    """Config Fossil

    Define the constants used with fossil commands and exceptions.
    """
    default_timeout: int = 180 #seconds
    process_error: str = 'FOSSIL_PROCESS_ERROR'
    timeout_error: str = 'FOSSIL_TIMEOUT_ERROR'
    args: str = 'args'
    cmd: str = 'cmd'
    output: str = 'output'
    return_code: str = 'return_code'
    default_return_code: int = 1
    stderr: str = 'stderr'
    timeout: str = 'timeout'

FOSSIL: ConfigFossil = ConfigFossil()
"""Global instance of the default fossil configuration."""
