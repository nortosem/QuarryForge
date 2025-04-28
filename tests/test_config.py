"""Test Config

Test suite for the quarryforge.config module.

This test suite provides full MC/DC coverage for the quarryforge.config module.
It utilizes pytest for test execution and coverage analysis.
"""
from enum import Enum
from pathlib import Path
import pytest

from quarryforge.config import CatConfig
from quarryforge.config import Command
from quarryforge.config import ConfigArgs
from quarryforge.config import DiffConfig
from quarryforge.config import InfoConfig
from quarryforge.config import InfoData
from quarryforge.config import TimelineConfig
from quarryforge.config import TimelineData
from quarryforge.config import Valid

import re
from typing import Tuple


class TestValidEnum:
    """Test Valid Enum

    Test suite for the Valid Enum class.
    """

    class ExampleEnum(Valid):
        A = 'a'
        B = 'b'
        C = 'c'

    def test_slots(self):
        """Tests the slots class method."""
        slots = self.ExampleEnum.slots()
        assert isinstance(slots, tuple)
        assert slots == ('a', 'b', 'c')


class TestConfigArgs:
    """Tset ConfigArgs

    Test suite for the ConfigArgs Enum.
    """

    def test_config_args_values(self):
        """Tests that all ConfigArgs members have the correct string values."""
        assert ConfigArgs.USER.value == 'user'
        assert ConfigArgs.EMAIL.value == 'email'
        assert ConfigArgs.SRC_REPO.value == 'src_repo'
        assert ConfigArgs.REBUILD_REPO.value == 'rebuild_repo'
        assert ConfigArgs.REBUILD_CHECKOUT_DIR.value == 'rebuild_checkout_dir'
        assert ConfigArgs.TEMPLATE.value == 'template'
        assert ConfigArgs.PROJECT_NAME.value == 'project_name'
        assert ConfigArgs.PROJECT_DESC.value == 'project_desc'

    def test_type_name(self):
        """Tests the type_name class method."""
        assert ConfigArgs.type_name() == 'RepoConfig'

    def test_docs(self):
        """Tests the docs class method."""
        assert ConfigArgs.docs() == 'Repoconfig stores valid toml config.'


class TestTimelineConfig:
    """Test TimelineConfig

    Test suite for the TimelineConfig Enum.
    """

    def test_timeline_config_values(self):
        """
        Tests that all TimelineConfig members have the correct string values.
        """
        assert TimelineConfig.SRC_REPO.value == 'src_repo'

    def test_type_name(self):
        """Tests the type_name class method."""
        assert TimelineConfig.type_name() == 'TimelineArg'

    def test_docs(self):
        """Tests the docs class method."""
        assert TimelineConfig.docs() == '#todo'


class TestInfoConfig:
    """Test InfoConfig

    Test suite for the InfoConfig Enum.
    """

    def test_info_config_values(self):
        """Tests that all InfoConfig members have the correct string values."""
        assert InfoConfig.VERSION.value == 'version'
        assert InfoConfig.SRC_REPO.value == 'src_repo'

    def test_type_name(self):
        """Tests the type_name class method."""
        assert InfoConfig.type_name() == 'InfoArgs'

    def test_docs(self):
        """Tests the docs class method."""
        assert InfoConfig.docs() == \
            'The valid arguments for a fossil info command.'


class TestDiffConfig:
    """Test DiffConfig

    Test suite for the DiffConfig Enum.
    """

    def test_diff_config_values(self):
        """Tests that all DiffConfig members have the correct string values."""
        assert DiffConfig.PARENT.value == 'parent'
        assert DiffConfig.CHILD.value == 'child'
        assert DiffConfig.SRC_REPO.value == 'src_repo'

    def test_type_name(self):
        """Tests the type_name class method."""
        assert DiffConfig.type_name() == 'InfoArgs'

    def test_docs(self):
        """Tests the docs class method."""
        assert DiffConfig.docs() == \
            'The valid arguments for a fossil diff command.'


class TestCatConfig:
    """Test CatConfig
    Test suite for the CatConfig Enum.
    """

    def test_cat_config_values(self):
        """Tests that all CatConfig members have the correct string values."""
        assert CatConfig.FILE.value == 'file'
        assert CatConfig.VERSION.value == 'version'
        assert CatConfig.SRC_REPO.value == 'src_repo'

    def test_type_name(self):
        """Tests the type_name class method."""
        assert CatConfig.type_name() == 'InfoArgs'

    def test_docs(self):
        """Tests the docs class method."""
        assert CatConfig.docs() == \
            'The valid arguments for a fossil cat command.'


class TestCommand:
    """Test Command

    Test suite for the Command Enum.
    """

    def test_command_values(self):
        """Tests that all Command members have the correct string values."""
        assert Command.FOSSIL.value == 'fossil'
        assert Command.REPO.value == '-R'
        assert Command.TIMELINE.value == 'timeline'
        assert Command.VERBOSE.value == '--verbose'
        assert Command.TYPE.value == '--type'
        assert Command.CI.value == 'ci'
        assert Command.LIMIT.value == '--limit'
        assert Command.NO_LIMIT.value == '0'
        assert Command.FULL.value == '--full'
        assert Command.NEW.value == 'new'
        assert Command.USER.value == 'user'
        assert Command.DEFAULT.value == 'default'
        assert Command.CONTACT.value == 'contact'
        assert Command.TEMPLATE.value == '--template'
        assert Command.ADMIN_USER.value == '--admin-user'
        assert Command.PROJECT_NAME.value == '--project-name'
        assert Command.PROJECT_DESC.value == '--project-desc'
        assert Command.BRANCH.value == 'branch'
        assert Command.LIST.value == 'list'
        assert Command.ALL.value == '--all'
        assert Command.CLOSED.value == '--closed'
        assert Command.INFO.value == 'info'
        assert Command.DIFF.value == 'diff'
        assert Command.BRIEF.value == '--brief'
        assert Command.FROM.value == '--from'
        assert Command.TO.value == '--to'
        assert Command.CAT.value == 'cat'
        assert Command.VERSION.value == '-r'


class TestTimelineData:
    """Test TimelineData

    Test suite for the TimelineData Enum.
    """

    def test_timeline_data_values(self):
        """
        Tests that all TimelineData members have the correct string values.
        """
        assert TimelineData.END_MARK.value == '+++ end of timeline'
        assert TimelineData.COMMITS.value == 'commits'
        assert TimelineData.COMMIT_DATA.value == '\\n(?=Commit:\\s+)'
        assert TimelineData.HASH.value == 'uuid'
        assert TimelineData.HASH_DATA.value == \
            '^(?P<label>Commit:\\s+)(?P<uuid>[0-9a-f]+)$'
        assert TimelineData.DATE.value == 'date'
        assert TimelineData.DATE_DATA.value == \
            '^(?P<label>Date):\\s+(?P<date>.+)$'
        assert TimelineData.AUTHOR.value == 'author'
        assert TimelineData.AUTHOR_DATA.value == \
            '^(?P<label>Author):\\s+(?P<author>.+)?'
        assert TimelineData.COMMENT.value == 'comment'
        assert TimelineData.COMMENT_DATA.value == \
            '^(?P<label>Comment):\\s+(?P<comment>.+)$'
        assert TimelineData.BRANCH.value == 'branch'
        assert TimelineData.BRANCH_DATA.value == \
            '^(?P<label>Branch):\\s+(?P<branch>.+)$'
        assert TimelineData.TAGS.value == 'tags'
        assert TimelineData.TAG_DATA.value == \
            '^(?P<label>Tags):\\s+(?P<tags>.+)$'
        assert TimelineData.PHASE.value == 'phase'
        assert TimelineData.PHASE_DATA.value == \
            '^(?P<label>Phase):\\s+\\*?(?P<phase>LEAF|PUBLISHED|FROZEN)?\\*?'
        assert TimelineData.CHANGES.value == 'changes'
        assert TimelineData.CHANGE.value == 'change'
        assert TimelineData.CHANGE_DATA.value == '^\\s+(?P<change>ADDED|EDITED|DELETED)\\s(?P<filename>.+)$'

    def test_commit_slots(self):
        """Tests the commit_slots class method."""
        slots = TimelineData.commit_slots()
        assert isinstance(slots, tuple)
        assert slots == (
            TimelineData.HASH.value,
            TimelineData.DATE.value,
            TimelineData.AUTHOR.value,
            TimelineData.COMMENT.value,
            TimelineData.BRANCH.value,
            TimelineData.TAGS.value,
            TimelineData.PHASE.value,
            TimelineData.CHANGES.value
        )

    def test_commit_pattern(self):
        """Tests the commit_pattern class method."""
        pattern = TimelineData.commit_pattern()
        assert isinstance(pattern, re.Pattern)
        assert pattern.pattern == TimelineData.COMMIT_DATA.value

    def test_hash_pattern(self):
        """Tests the hash_pattern class method."""
        pattern = TimelineData.hash_pattern()
        assert isinstance(pattern, re.Pattern)
        assert pattern.pattern == TimelineData.HASH_DATA.value

    def test_date_pattern(self):
        """Tests the date_pattern class method."""
        pattern = TimelineData.date_pattern()
        assert isinstance(pattern, re.Pattern)
        assert pattern.pattern == TimelineData.DATE_DATA.value

    def test_author_pattern(self):
        """Tests the author_pattern class method."""
        pattern = TimelineData.author_pattern()
        assert isinstance(pattern, re.Pattern)
        assert pattern.pattern == TimelineData.AUTHOR_DATA.value

    def test_comment_pattern(self):
        """Tests the comment_pattern class method."""
        pattern = TimelineData.comment_pattern()
        assert isinstance(pattern, re.Pattern)
        assert pattern.pattern == TimelineData.COMMENT_DATA.value

    def test_branch_pattern(self):
        """Tests the branch_pattern class method."""
        pattern = TimelineData.branch_pattern()
        assert isinstance(pattern, re.Pattern)
        assert pattern.pattern == TimelineData.BRANCH_DATA.value

    def test_tags_pattern(self):
        """Tests the tags_pattern class method."""
        pattern = TimelineData.tags_pattern()
        assert isinstance(pattern, re.Pattern)
        assert pattern.pattern == TimelineData.TAG_DATA.value

    def test_phase_pattern(self):
        """Tests the phase_pattern class method."""
        pattern = TimelineData.phase_pattern()
        assert isinstance(pattern, re.Pattern)
        assert pattern.pattern == TimelineData.PHASE_DATA.value

    def test_change_pattern(self):
        """Tests the change_pattern class method."""
        pattern = TimelineData.change_pattern()
        assert isinstance(pattern, re.Pattern)
        assert pattern.pattern == TimelineData.CHANGE_DATA.value


class TestInfoData:
    """Test InfoData

    Test suite for the InfoData Enum.
    """

    def test_info_data_values(self):
        """Tests that all InfoData members have the correct string values."""
        assert InfoData.INIT_HASH.value == '^comment:\\s+(?P<init>)\\s.+\\n'
        assert InfoData.PARENT.value == 'parent'
        assert InfoData.PARENT_DATA.value == '^parent:\\s+(?P<uuid>.+?)\\s.+\\n'

    def test_init_pattern(self):
         """Tests the init_pattern class method."""
         pattern = InfoData.init_pattern()
         assert isinstance(pattern, re.Pattern)
         assert pattern.pattern == InfoData.INIT_HASH.value

    def test_parent_pattern(self):
        """Tests the parent_pattern class method."""
        pattern = InfoData.parent_pattern()
        assert isinstance(pattern, re.Pattern)
        assert pattern.pattern == InfoData.PARENT_DATA.value
