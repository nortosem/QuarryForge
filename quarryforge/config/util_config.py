"""Utility Configuration

#TODO
"""
from typing import NamedTuple

import re


__all__: list = ['COMMAND', 'TIMELINE_DATA', 'INFO_DATA']


class Command(NamedTuple):
    """The permitted fossil commands and options"""
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


COMMAND: Command = Command()
"""Global constant for fossil command arguments."""


class TimelineData(NamedTuple):
    """Timeline Data

    The fields and patterns used to parse commits from the timeline output.
    """
    INIT_CHECKIN: str = 'initial empty check-in'
    END_MARK: str = '+++ end of timeline'
    COMMITS: str = 'commits'
    COMMIT: str = '\\n(?=Commit:\\s+)'
    HASH: str = '^(?P<label>Commit:\\s+)(?P<uuid>[0-9a-f]+)$'
    DATE: str = '^(?P<label>Date):\\s+(?P<date>.+)$'
    AUTHOR: str = '^(?P<label>Author):\\s+(?P<author>.+)?'
    COMMENT: str = '^(?P<label>Comment):\\s+(?P<comment>.+)$'
    BRANCH: str = '^(?P<label>Branch):\\s+(?P<branch>.+)$'
    TAGS: str = '^(?P<label>Tags):\\s+(?P<tags>.+)$'
    TAG: str = '?P<tag>[\\w-]+'
    PHASE: str = (
        '^(?P<label>Phase):\\s+\\*?(?P<phase>LEAF|PUBLISHED|FROZEN)?\\*?'
    )
    CHANGE: str = '^\\s+(?P<change>ADDED|EDITED|DELETED)\\s(?P<filename>.+)$'
    PATH: str = '^(?P<path>.*[\\/])?(?P<file>[^/\\\\]+$)'

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
    INIT_HASH: str = '^comment:\\s+(?P<init>)\\s.+\\n'
    PARENT: str = 'parent'
    PARENT_DATA: str = '^parent:\\s+(?P<uuid>.+?)\\s.+\\n'

    def init_pattern(self) -> re.Pattern:
        pattern = re.compile(self.INIT_HASH)
        return pattern

    def parent_pattern(self) -> re.Pattern:
        pattern = re.compile(self.PARENT_DATA)
        return pattern


INFO_DATA: InfoData = InfoData()
"""Global constant for info data patterns."""
