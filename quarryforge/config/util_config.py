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

    def commit_pattern(self) -> re.Pattern:
        pattern = re.compile(f'{self.COMMIT}')
        return pattern

    def hash_pattern(self) -> re.Pattern:
        pattern = re.compile(f'{self.HASH}')
        return pattern

    def date_pattern(self) -> re.Pattern:
        pattern = re.compile(f'{self.DATE}')
        return pattern

    def author_pattern(self) -> re.Pattern:
        pattern = re.compile(f'{self.AUTHOR}')
        return pattern

    def comment_pattern(self) -> re.Pattern:
        pattern = re.compile(f'{self.COMMENT}')
        return pattern

    def branch_pattern(self) -> re.Pattern:
        pattern = re.compile(f'{self.BRANCH}')
        return pattern

    def tags_pattern(self) -> re.Pattern:
        pattern = re.compile(f'{self.TAGS}')
        return pattern

    def phase_pattern(self) -> re.Pattern:
        pattern = re.compile(f'{self.PHASE}')
        return pattern

    def change_pattern(self) -> re.Pattern:
        pattern = re.compile(f'{self.CHANGE}')
        return pattern


TIMELINE_DATA: TimelineData = TimelineData()
"""Global constant for timeline data configuration."""


class InfoData(NamedTuple):
    """Parser for Fossil Info output."""
    INIT_HASH = '^comment:\\s+(?P<init>)\\s.+\\n'
    PARENT = 'parent'
    PARENT_DATA = '^parent:\\s+(?P<uuid>.+?)\\s.+\\n'

    def init_pattern(self) -> re.Pattern:
        pattern = re.compile(self.INIT_HASH)
        return pattern

    def parent_pattern(self) -> re.Pattern:
        pattern = re.compile(self.PARENT_DATA)
        return pattern


INFO_DATA: InfoData = InfoData()
"""Global constant for info data patterns."""
