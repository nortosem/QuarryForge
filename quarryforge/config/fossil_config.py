"""Fossil Configuration

This module defines configurations specific to Fossil SCM operations,
including default timeouts, command structures, and output parsing patterns.
It centralizes all Fossil-related constant definitions.
"""
from enum import StrEnum
from typing import List, NamedTuple
import re


__all__: List[str] = [
    'Command',
    'timeline_data',
    'info_data',
    'Fossil'
]


class Command(StrEnum):
    """The permitted fossil commands and options."""
    FOSSIL = 'fossil'
    REPO = '-R'
    TIMELINE = 'timeline'
    VERBOSE = '--verbose'
    TYPE = '--type'
    CI = 'ci'
    LIMIT = '--limit'
    NO_LIMIT = '0'
    FULL = '--full'
    NEW = 'new'
    USER = 'user'
    DEFAULT = 'default'
    CONTACT = 'contact'
    TEMPLATE = '--template'
    ADMIN_USER = '--admin-user'
    DATE_OVERRIDE = '--date-override'
    PROJECT_NAME = '--project-name'
    PROJECT_DESC = '--project-desc'
    BRANCH = 'branch'
    LIST = 'list'
    ALL = '--all'
    OPEN = 'open'
    CLOSE = 'close'
    WORKDIR = '--workdir'
    CLOSED = '--closed'
    INFO = 'info'
    DIFF = 'diff'
    BRIEF = '--brief'
    FROM = '--from'
    TO = '--to'
    OUTFILE = '--out'
    CAT = 'cat'
    VERSION = '-r'
    ADD = 'add'
    COMMENT = '--comment'
    TAG = '--tag'
    USER_OVERRIDE = '--user-override'
    HASH = '--hash'
    COMMIT = 'commit'


class TimelineDataConfig(NamedTuple):
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

    def commit_pattern(self) -> re.Pattern[str]:
        """Regex pattern to split timeline output into individual commits."""
        return re.compile(f'{self.COMMIT_SEP}')

    def hash_pattern(self) -> re.Pattern[str]:
        """Regex pattern for extracting commit hash (UUID)."""
        return re.compile(f'{self.HASH_PATTERN}')

    def date_pattern(self) -> re.Pattern[str]:
        """Regex pattern for extracting commit date."""
        return re.compile(f'{self.DATE_PATTERN}')

    def author_pattern(self) -> re.Pattern[str]:
        """Regex pattern for extracting commit author."""
        return re.compile(f'{self.AUTHOR_PATTERN}')

    def comment_pattern(self) -> re.Pattern[str]:
        """Regex pattern for extracting commit comment."""
        return re.compile(f'{self.COMMENT_PATTERN}')

    def branch_pattern(self) -> re.Pattern[str]:
        """Regex pattern for extracting commit branch."""
        return re.compile(f'{self.BRANCH_PATTERN}')

    def tags_pattern(self) -> re.Pattern[str]:
        """Regex pattern for extracting commit tags."""
        return re.compile(f'{self.TAGS_PATTERN}')

    def phase_pattern(self) -> re.Pattern[str]:
        """Regex pattern for extracting commit phase."""
        return re.compile(f'{self.PHASE_PATTERN}')

    def change_pattern(self) -> re.Pattern[str]:
        """Regex pattern for extracting file changes."""
        return re.compile(f'{self.CHANGE_PATTERN}')


def timeline_data() -> TimelineDataConfig:
    """Provides the configuration for the Timeline data."""
    return TimelineDataConfig()


class InfoDataConfig(NamedTuple):
    """Parser for Fossil Info output."""
    INIT_HASH: str = '^comment:\\s+(?P<init>)\\s.+\\n'
    PARENT_KEY: str = 'parent'
    PARENT_DATA_PATTERN: str = '^parent:\\s+(?P<uuid>.+?)\\s.+\\n'

    def init_pattern(self) -> re.Pattern[str]:
        """Regex pattern for identifying initial commit info output."""
        return re.compile(self.INIT_HASH)

    def parent_pattern(self) -> re.Pattern[str]:
        """Regex pattern for extracting parent commit hash from info output."""
        return re.compile(self.PARENT_DATA_PATTERN)


def info_data() -> InfoDataConfig:
    """Provides the configuration for the Info data."""
    return InfoDataConfig()


class Fossil(StrEnum):
    """Config Fossil

    Define the constants used with fossil commands and exceptions.
    """
    DEFAULT_TIMEOUT = 180 #seconds
    PROCESS_ERROR = 'FOSSIL_PROCESS_ERROR'
    TIMEOUT_ERROR = 'FOSSIL_TIMEOUT_ERROR'
    ARGS = 'args'
    CMD = 'cmd'
    OUTPUT = 'output'
    RETURN_CODE = 'return_code'
    DEFAULT_RETURN_CODE = 1
    STDERR = 'stderr'
    TIMEOUT = 'timeout'
    STEP = 'step'
    INIT = 'New repository initialization'
    USERNAME_SETUP = 'username_setup'
    USER_CONTACT = 'user_contact'
