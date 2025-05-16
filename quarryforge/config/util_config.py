"""Utility Configuration

#TODO
"""
from typing import NamedTuple

import re


__all__ = ['COMMAND', 'TIMELINE_DATA', '']


class Command(NamedTuple):
    """The permitted fossil commands and options"""
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
    PROJECT_NAME = '--project-name'
    PROJECT_DESC = '--project-desc'
    BRANCH = 'branch'
    LIST = 'list'
    ALL = '--all'
    CLOSED = '--closed'
    INFO = 'info'
    DIFF = 'diff'
    BRIEF = '--brief'
    FROM = '--from'
    TO = '--to'
    CAT = 'cat'
    VERSION = '-r'


COMMAND: Command = Command()
"""Global constant for fossil command arguments."""


class TimelineData(NamedTuple):
    """Timeline Data

    The fields and patterns used to parse commits from the timeline output.
    """
    INIT_CHECKIN = 'initial empty check-in'
    END_MARK = '+++ end of timeline'
    COMMITS = 'commits'
    COMMIT = '\\n(?=Commit:\\s+)'
    HASH = '^(?P<label>Commit:\\s+)(?P<uuid>[0-9a-f]+)$'
    DATE = '^(?P<label>Date):\\s+(?P<date>.+)$'
    AUTHOR = '^(?P<label>Author):\\s+(?P<author>.+)?'
    COMMENT = '^(?P<label>Comment):\\s+(?P<comment>.+)$'
    BRANCH = '^(?P<label>Branch):\\s+(?P<branch>.+)$'
    TAGS = '^(?P<label>Tags):\\s+(?P<tags>.+)$'
    TAG = '?P<tag>[\\w-]+'
    PHASE = \
        '^(?P<label>Phase):\\s+\\*?(?P<phase>LEAF|PUBLISHED|FROZEN)?\\*?'
    CHANGE = '^\\s+(?P<change>ADDED|EDITED|DELETED)\\s(?P<filename>.+)$'
    PATH = '^(?P<path>.*[\\/])?(?P<file>[^/\\\\]+$)'

    @classmethod
    def commit_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.COMMIT}')
        return pattern

    @classmethod
    def hash_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.HASH}')
        return pattern

    @classmethod
    def date_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.DATE}')
        return pattern

    @classmethod
    def author_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.AUTHOR}')
        return pattern

    @classmethod
    def comment_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.COMMENT}')
        return pattern

    @classmethod
    def branch_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.BRANCH}')
        return pattern

    @classmethod
    def tags_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.TAGS}')
        return pattern

    @classmethod
    def phase_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.PHASE}')
        return pattern

    @classmethod
    def change_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.CHANGE}')
        return pattern


TIMELINE_DATA: TimelineData = TimelineData()
"""Global constant for timeline data configuration."""


class InfoData(NamedTuple):
    """Parser for Fossil Info output."""
    INIT_HASH = '^comment:\\s+(?P<init>)\\s.+\\n'
    PARENT = 'parent'
    PARENT_DATA = '^parent:\\s+(?P<uuid>.+?)\\s.+\\n'

    @classmethod
    def init_pattern(cls) -> re.Pattern:
        pattern = re.compile(cls.INIT_HASH)
        return pattern

    @classmethod
    def parent_pattern(cls) -> re.Pattern:
        pattern = re.compile(cls.PARENT_DATA)
        return pattern


INFO_DATA: InfoData = InfoData()
"""Global constant for info data patterns."""
