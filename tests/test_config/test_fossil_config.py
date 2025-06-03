import pytest
import re
from typing import NamedTuple

from quarryforge.config import fossil_config

from tests.test_config.test_root import get_namedtuple_fields


class TestFossilConfig:
    """Tests for quarryforge.config.fossil_config"""

    def test_module_dunder_all(self):
        """Test the __all__ variable for completeness."""
        expected_all = [
            'COMMAND',
            'TIMELINE_DATA',
            'INFO_DATA',
            'FOSSIL'
        ]
        assert sorted(fossil_config.__all__) == sorted(expected_all)

    def test_config_command_attributes(self):
        """Test attributes of ConfigCommand."""
        cmd = fossil_config.COMMAND
        assert isinstance(cmd, fossil_config.ConfigCommand)
        assert cmd.FOSSIL == 'fossil'
        assert cmd.REPO == '-R'
        assert cmd.TIMELINE == 'timeline'
        assert cmd.VERBOSE == '--verbose'
        assert cmd.TYPE == '--type'
        assert cmd.CI == 'ci'
        assert cmd.LIMIT == '--limit'
        assert cmd.NO_LIMIT == '0'
        assert cmd.FULL == '--full'
        assert cmd.NEW == 'new'
        assert cmd.USER == 'user'
        assert cmd.DEFAULT == 'default'
        assert cmd.CONTACT == 'contact'
        assert cmd.TEMPLATE == '--template'
        assert cmd.ADMIN_USER == '--admin-user'
        assert cmd.PROJECT_NAME == '--project-name'
        assert cmd.PROJECT_DESC == '--project-desc'
        assert cmd.BRANCH == 'branch'
        assert cmd.LIST == 'list'
        assert cmd.ALL == '--all'
        assert cmd.CLOSED == '--closed'
        assert cmd.INFO == 'info'
        assert cmd.DIFF == 'diff'
        assert cmd.BRIEF == '--brief'
        assert cmd.FROM == '--from'
        assert cmd.TO == '--to'
        assert cmd.CAT == 'cat'
        assert cmd.VERSION == '-r'
        assert cmd.ADD == 'add'
        assert cmd.COMMIT == 'commit'

        assert len(get_namedtuple_fields(fossil_config.ConfigCommand)) == 30

    def test_config_timeline_data_attributes(self):
        """Test attributes of ConfigTimelineData."""
        td = fossil_config.TIMELINE_DATA
        assert isinstance(td, fossil_config.ConfigTimelineData)
        assert td.INIT_CHECKIN == 'initial empty check-in'
        assert td.END_MARK == '+++ end of timeline'
        assert td.COMMITS_KEY == 'commits'
        assert td.HASH_KEY == 'uuid'
        assert td.DATE_KEY == 'date'
        assert td.AUTHOR_KEY == 'author'
        assert td.COMMENT_KEY == 'comment'
        assert td.BRANCH_KEY == 'branch'
        assert td.TAGS_KEY == 'tags'
        assert td.PHASE_KEY == 'phase'
        assert td.CHANGES_KEY == 'changes'

        assert td.HASH_PATTERN == '^(?P<label>Commit:\\s+)(?P<uuid>[0-9a-f]+)$'
        assert td.DATE_PATTERN == '^(?P<label>Date):\\s+(?P<date>.+)$'
        assert td.AUTHOR_PATTERN == '^(?P<label>Author):\\s+(?P<author>.+)?'
        assert td.COMMENT_PATTERN == '^(?P<label>Comment):\\s+(?P<comment>.+)$'
        assert td.BRANCH_PATTERN == '^(?P<label>Branch):\\s+(?P<branch>.+)$'
        assert td.TAGS_PATTERN == '^(?P<label>Tags):\\s+(?P<tags>.+)$'
        assert td.TAG_REGEX == '?P<tag>[\\w-]+'
        assert td.PHASE_PATTERN == (
            '^(?P<label>Phase):\\s+\\*?(?P<phase>LEAF|PUBLISHED|FROZEN)?\\*?'
        )
        assert td.CHANGE_PATTERN == (
            '^\\s+(?P<change>ADDED|EDITED|DELETED)\\s(?P<filename>.+)$'
        )
        assert td.PATH_PATTERN == '^(?P<path>.*[\\/])?(?P<file>[^/\\\\]+$)'

        expected_fields = [
            'INIT_CHECKIN', 'END_MARK', 'COMMITS_KEY', 'COMMIT_SEP',
            'HASH_KEY', 'HASH_PATTERN', 'DATE_KEY', 'DATE_PATTERN',
            'AUTHOR_KEY', 'AUTHOR_PATTERN', 'COMMENT_KEY', 'COMMENT_PATTERN',
            'BRANCH_KEY', 'BRANCH_PATTERN', 'TAGS_KEY', 'TAGS_PATTERN',
            'TAG_REGEX', 'PHASE_KEY', 'PHASE_PATTERN', 'CHANGES_KEY',
            'CHANGE_PATTERN', 'PATH_PATTERN'
        ]
        assert sorted(get_namedtuple_fields(fossil_config.ConfigTimelineData)) == sorted(expected_fields)


    @pytest.mark.parametrize(
        "method_name, expected_pattern_attr",
        [
            ("commit_pattern", "COMMIT_SEP"),
            ("hash_pattern", "HASH_PATTERN"),
            ("date_pattern", "DATE_PATTERN"),
            ("author_pattern", "AUTHOR_PATTERN"),
            ("comment_pattern", "COMMENT_PATTERN"),
            ("branch_pattern", "BRANCH_PATTERN"),
            ("tags_pattern", "TAGS_PATTERN"),
            ("phase_pattern", "PHASE_PATTERN"),
            ("change_pattern", "CHANGE_PATTERN"),
        ]
    )
    def test_config_timeline_data_pattern_methods(
            self, method_name, expected_pattern_attr):
        """Test pattern compilation methods of ConfigTimelineData."""
        td = fossil_config.TIMELINE_DATA
        method = getattr(td, method_name)
        pattern_obj = method()
        assert isinstance(pattern_obj, re.Pattern)

        expected_source_pattern = getattr(td, expected_pattern_attr)
        assert pattern_obj.pattern == expected_source_pattern

    def test_config_info_data_attributes(self):
        """Test attributes of ConfigInfoData."""
        info_data = fossil_config.INFO_DATA
        assert isinstance(info_data, fossil_config.ConfigInfoData)
        assert info_data.INIT_HASH == '^comment:\\s+(?P<init>)\\s.+\\n'
        assert info_data.PARENT_KEY == 'parent'
        assert info_data.PARENT_DATA_PATTERN == (
            '^parent:\\s+(?P<uuid>.+?)\\s.+\\n'
        )

        expected_fields = ['INIT_HASH', 'PARENT_KEY', 'PARENT_DATA_PATTERN']
        assert sorted(
            get_namedtuple_fields(
                fossil_config.ConfigInfoData)) == sorted(expected_fields)


    @pytest.mark.parametrize(
        "method_name, expected_pattern_attr",
        [
            ("init_pattern", "INIT_HASH"),
            ("parent_pattern", "PARENT_DATA_PATTERN"),
        ]
    )
    def test_config_info_data_pattern_methods(self, method_name, expected_pattern_attr):
        """Test pattern compilation methods of ConfigInfoData."""
        info_data = fossil_config.INFO_DATA
        method = getattr(info_data, method_name)
        pattern_obj = method()
        assert isinstance(pattern_obj, re.Pattern)
        expected_source_pattern = getattr(info_data, expected_pattern_attr)
        assert pattern_obj.pattern == expected_source_pattern

    def test_config_fossil_attributes(self):
        """Test attributes of ConfigFossil."""
        fossil_conf = fossil_config.FOSSIL
        assert isinstance(fossil_conf, fossil_config.ConfigFossil)
        assert fossil_conf.default_timeout == 180
        assert fossil_conf.process_error == 'FOSSIL_PROCESS_ERROR'
        assert fossil_conf.timeout_error == 'FOSSIL_TIMEOUT_ERROR'
        assert fossil_conf.args == 'args'
        assert fossil_conf.cmd == 'cmd'
        assert fossil_conf.output == 'output'
        assert fossil_conf.return_code == 'return_code'
        assert fossil_conf.default_return_code == 1
        assert fossil_conf.stderr == 'stderr'
        assert fossil_conf.timeout == 'timeout'

        expected_attrs = [
            'default_timeout', 'process_error', 'timeout_error',
            'args', 'cmd', 'output', 'return_code',
            'default_return_code', 'stderr', 'timeout'
        ]

        for attr_name in expected_attrs:
            assert hasattr(fossil_conf, attr_name)
            assert getattr(fossil_conf, attr_name) == (
                getattr(fossil_config.FOSSIL, attr_name)
            )


    def test_global_constants_types(self):
        """Test types of global constants."""
        assert isinstance(fossil_config.COMMAND, fossil_config.ConfigCommand)
        assert isinstance(
            fossil_config.TIMELINE_DATA, fossil_config.ConfigTimelineData)
        assert isinstance(fossil_config.INFO_DATA, fossil_config.ConfigInfoData)
        assert isinstance(fossil_config.FOSSIL, fossil_config.ConfigFossil)
