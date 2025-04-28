"""config

#todo
"""
from enum import Enum

#from pathlib import Path

import re

#from typing import List
from typing import Text
from typing import Tuple


class Valid(Enum):
    """Package Enum Validator

    Define class method to return member values as a tuple.
    """
    @classmethod
    def slots(cls) -> Tuple[str]:
        return tuple(slot.value for slot in cls)


class ConfigArgs(Valid):
    """Configuration Arguments

    This class holds settings for rebuilding a fossil repository with updated
    user information, repository paths, and project details.

    Args:
        user (str): Username.
        emai (str)l: User email.
        src_repo (Path): Path to the source repository.
        rebuild_repo (Path): Path to the rebuild repository.
        template (Path): Path to the template directory.
        project_name (str): Name of the project.
        project_desc (str): Description of the project.
    """
    USER = 'user'
    EMAIL = 'email'
    SRC_REPO = 'src_repo'
    REBUILD_REPO = 'rebuild_repo'
    TEMPLATE = 'template'
    PROJECT_NAME = 'project_name'
    PROJECT_DESC = 'project_desc'

    @classmethod
    def type_name(cls) -> str:
        return 'RepoConfig'

    @classmethod
    def docs(cls) -> Text:
        return 'Repoconfig stores valid toml config.'


class TimelineConfig(Valid):
    """Timeline Config

    Defines the slots for a TimelineArg

    Attributes:
        src: (Path): pathlib.Path location of the fossil repo to reconstruct.
    """
    SRC_REPO = 'src_repo'

    @classmethod
    def type_name(cls) -> str:
        return 'TimelineArg'

    @classmethod
    def docs(cls) -> Text:
        return '#todo'


class InfoConfig(Valid):
    """Info Config

    The slots for a valid args to a fossil info command.
    """
    VERSION = 'version'
    SRC_REPO = 'src_repo'

    @classmethod
    def type_name(cls) -> str:
        return 'InfoArgs'

    @classmethod
    def docs(cls) -> Text:
        return 'The valid arguments for a fossil info command.'


class DiffConfig(Valid):
    """Diff Config

    The slots for a valid args to a fossil diff command.
    """
    PARENT = 'parent'
    CHILD = 'child'
    SRC_REPO = 'src_repo'

    @classmethod
    def type_name(cls) -> str:
        return 'InfoArgs'

    @classmethod
    def docs(cls) -> Text:
        return 'The valid arguments for a fossil diff command.'


class CatConfig(Valid):
    """Cat Config

    The slots for a valid args to a fossil cat command.
    """
    FILE = 'file'
    VERSION = 'version'
    SRC_REPO = 'src_repo'


    @classmethod
    def type_name(cls) -> str:
        return 'InfoArgs'

    @classmethod
    def docs(cls) -> Text:
        return 'The valid arguments for a fossil cat command.'


class Command(Valid):
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


class TimelineData(Valid):
    """Timeline Data

    The fields and patterns used to parse commits from the timeline output.
    """
    END_MARK = '+++ end of timeline'
    COMMITS = 'commits'
    COMMIT_DATA = '\\n(?=Commit:\\s+)'
    HASH = 'uuid'
    HASH_DATA = '^(?P<label>Commit:\\s+)(?P<uuid>[0-9a-f]+)$'
    DATE = 'date'
    DATE_DATA = '^(?P<label>Date):\\s+(?P<date>.+)$'
    AUTHOR = 'author'
    AUTHOR_DATA = '^(?P<label>Author):\\s+(?P<author>.+)?'
    COMMENT = 'comment'
    COMMENT_DATA = '^(?P<label>Comment):\\s+(?P<comment>.+)$'
    BRANCH = 'branch'
    BRANCH_DATA = '^(?P<label>Branch):\\s+(?P<branch>.+)$'
    TAGS = 'tags'
    TAG_DATA = '^(?P<label>Tags):\\s+(?P<tags>.+)$'
    PHASE = 'phase'
    PHASE_DATA = \
        '^(?P<label>Phase):\\s+\\*?(?P<phase>LEAF|PUBLISHED|FROZEN)?\\*?'
    CHANGES = 'changes'
    CHANGE = 'change'
    CHANGE_DATA = '^\\s+(?P<change>ADDED|EDITED|DELETED)\\s(?P<filename>.+)$'

    @classmethod
    def commit_slots(cls) -> Tuple[str]:
        return (cls.HASH.value, cls.DATE.value, cls.AUTHOR.value,
                cls.COMMENT.value, cls.BRANCH.value, cls.TAGS.value,
                cls.PHASE.value, cls.CHANGES.value)

    @classmethod
    def commit_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.COMMIT_DATA.value}')
        return pattern

    @classmethod
    def hash_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.HASH_DATA.value}')
        return pattern

    @classmethod
    def date_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.DATE_DATA.value}')
        return pattern

    @classmethod
    def author_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.AUTHOR_DATA.value}')
        return pattern

    @classmethod
    def comment_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.COMMENT_DATA.value}')
        return pattern

    @classmethod
    def branch_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.BRANCH_DATA.value}')
        return pattern

    @classmethod
    def tags_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.TAG_DATA.value}')
        return pattern

    @classmethod
    def phase_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.PHASE_DATA.value}')
        return pattern

    @classmethod
    def change_pattern(cls) -> re.Pattern:
        pattern = re.compile(f'{cls.CHANGE_DATA.value}')
        return pattern


class InfoData(Valid):
    """Parser for Fossil Info output."""
    INIT_HASH = '^comment:\\s+(?P<init>)\\s.+\\n'
    PARENT = 'parent'
    PARENT_DATA = '^parent:\\s+(?P<uuid>.+?)\\s.+\\n'

    @classmethod
    def init_pattern(cls) -> re.Pattern:
        pattern = re.compile(cls.INIT_HASH.vallue)
        return pattern

    @classmethod
    def parent_pattern(cls) -> re.Pattern:
        pattern = re.compile(cls.PARENT_DATA.value)
        return pattern
