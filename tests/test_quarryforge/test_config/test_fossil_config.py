"""Tests for quarryforge.config.exception_conf.fossil_exception_config module."""

import re

import pytest

from quarryforge.config import fossil_config


class TestFossilConfig:
    """Tests for quarryforge.config.fossil_config"""

    def test_module_dunder_all(self):
        """Test the __all__ variable for completeness."""
        expected_all = ['Command', 'timeline_data', 'info_data', 'Fossil']
        assert sorted(fossil_config.__all__) == sorted(expected_all)

    def test_config_command_attributes(self):
        """Test attributes of Command."""
        assert fossil_config.Command.FOSSIL == 'fossil'
        assert fossil_config.Command.REPO == '-R'
        assert fossil_config.Command.TIMELINE == 'timeline'
        assert fossil_config.Command.VERBOSE == '--verbose'
        assert fossil_config.Command.TYPE == '--type'
        assert fossil_config.Command.CI == 'ci'
        assert fossil_config.Command.LIMIT == '--limit'
        assert fossil_config.Command.NO_LIMIT == '0'
        assert fossil_config.Command.FULL == '--full'
        assert fossil_config.Command.NEW == 'new'
        assert fossil_config.Command.USER == 'user'
        assert fossil_config.Command.DEFAULT == 'default'
        assert fossil_config.Command.CONTACT == 'contact'
        assert fossil_config.Command.TEMPLATE == '--template'
        assert fossil_config.Command.ADMIN_USER == '--admin-user'
        assert fossil_config.Command.DATE_OVERRIDE == '--date-override'
        assert fossil_config.Command.PROJECT_NAME == '--project-name'
        assert fossil_config.Command.PROJECT_DESC == '--project-desc'
        assert fossil_config.Command.BRANCH == 'branch'
        assert fossil_config.Command.LIST == 'list'
        assert fossil_config.Command.ALL == '--all'
        assert fossil_config.Command.OPEN == 'open'
        assert fossil_config.Command.CLOSE == 'close'
        assert fossil_config.Command.WORKDIR == '--workdir'
        assert fossil_config.Command.CLOSED == '--closed'
        assert fossil_config.Command.INFO == 'info'
        assert fossil_config.Command.DIFF == 'diff'
        assert fossil_config.Command.BRIEF == '--brief'
        assert fossil_config.Command.FROM == '--from'
        assert fossil_config.Command.TO == '--to'
        assert fossil_config.Command.OUTFILE == '--out'
        assert fossil_config.Command.CAT == 'cat'
        assert fossil_config.Command.VERSION == '-r'
        assert fossil_config.Command.ADD == 'add'
        assert fossil_config.Command.COMMENT == '--comment'
        assert fossil_config.Command.TAG == '--tag'
        assert fossil_config.Command.USER_OVERRIDE == '--user-override'
        assert fossil_config.Command.HASH == '--hash'
        assert fossil_config.Command.COMMIT == 'commit'

        assert isinstance(fossil_config.Command.FOSSIL, fossil_config.Command)
        assert len(fossil_config.Command) == 39

    def test_timeline_data_factory_and_patterns(self):
        """Verify the timeline_data factory and its pattern methods."""
        td = fossil_config.timeline_data()
        assert isinstance(td, fossil_config.TimelineDataConfig)
        assert td.INIT_CHECKIN == 'initial empty check-in'
        assert td.END_MARK == '+++ end of timeline'
        assert td.COMMITS_KEY == 'commits'
        assert td.COMMIT_SEP == '\\n(?=Commit:\\s+)'
        assert td.HASH_KEY == 'uuid'
        assert td.DATE_KEY == 'date'
        assert td.AUTHOR_KEY == 'author'
        assert td.COMMENT_KEY == 'comment'
        assert td.BRANCH_KEY == 'branch'
        assert td.TAGS_KEY == 'tags'
        assert td.PHASE_KEY == 'phase'
        assert td.CHANGES_KEY == 'changes'
        assert (
            td.HASH_PATTERN
            == '^(?P<label>Commit:\\s+)(?P<uuid>[0-9a-f]+)$'
        )
        assert td.DATE_PATTERN == '^(?P<label>Date):\\s+(?P<date>.+)$'
        assert (
            td.AUTHOR_PATTERN == '^(?P<label>Author):\\s+(?P<author>.+)?'
        )
        assert (
            td.COMMENT_PATTERN
            == '^(?P<label>Comment):\\s+(?P<comment>.+)$'
        )
        assert (
            td.BRANCH_PATTERN == '^(?P<label>Branch):\\s+(?P<branch>.+)$'
        )
        assert td.TAGS_PATTERN == '^(?P<label>Tags):\\s+(?P<tags>.+)$'
        assert td.TAG_REGEX == '?P<tag>[\\w-]+'
        assert (
            td.PHASE_PATTERN
            == '^(?P<label>Phase):\\s+\\*?(?P<phase>LEAF|PUBLISHED|FROZEN)?\\*?'
        )
        assert (
            td.CHANGE_PATTERN
            == '^\\s+(?P<change>ADDED|EDITED|DELETED)\\s(?P<filename>.+)$'
        )
        assert (
            td.PATH_PATTERN == '^(?P<path>.*[\\/])?(?P<file>[^/\\\\]+$)'
        )

        assert len(td) == 22

        for method_name in [
                m for m in dir(td) if m.endswith('_pattern')]:
            pattern_method = getattr(td, method_name)
            pattern_obj = pattern_method()
            assert isinstance(pattern_obj, re.Pattern)

    def test_info_data_factory_and_patterns(self):
        """Verify the info_data factory and its pattern methods."""
        id_config = fossil_config.info_data()
        assert isinstance(id_config, fossil_config.InfoDataConfig)
        assert id_config.INIT_HASH == '^comment:\\s+(?P<init>)\\s.+\\n'
        assert id_config.PARENT_KEY == 'parent'
        assert (
            id_config.PARENT_DATA_PATTERN
            == '^parent:\\s+(?P<uuid>.+?)\\s.+\\n'
        )
        assert isinstance(id_config.init_pattern(), re.Pattern)
        assert isinstance(id_config.parent_pattern(), re.Pattern)

    def test_config_fossil_attributes(self):
        """Test member values of the Fossil enum."""
        fossil = fossil_config.Fossil
        assert fossil.DEFAULT_TIMEOUT == '180'
        assert fossil.PROCESS_ERROR == 'FOSSIL_PROCESS_ERROR'
        assert fossil.TIMEOUT_ERROR == 'FOSSIL_TIMEOUT_ERROR'
        assert fossil.ARGS == 'args'
        assert fossil.CMD == 'cmd'
        assert fossil.OUTPUT == 'output'
        assert fossil.RETURN_CODE == 'returncode'
        assert fossil.DEFAULT_RETURN_CODE == '1'
        assert fossil.STDERR == 'stderr'
        assert fossil.TIMEOUT == 'timeout'
        assert fossil.STEP == 'step'
        assert fossil.INIT == 'New repository initialization'
        assert fossil.USERNAME_SETUP == 'username_setup'
        assert fossil.USER_CONTACT == 'user_contact'

        assert len(fossil) == 14
