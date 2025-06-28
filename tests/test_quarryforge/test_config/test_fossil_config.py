import re

import pytest

from quarryforge.config import fossil_config


class TestFossilConfig:
    """Tests for quarryforge.config.fossil_config"""

    def test_module_dunder_all(self):
        """Test the __all__ variable for completeness."""
        expected_all = ['Command', 'TimelineData', 'InfoData', 'Fossil']
        assert sorted(fossil_config.__all__) == sorted(expected_all)

    def test_config_command_attributes(self):
        """Test attributes of Command."""
        assert fossil_config.Command.FOSSIL.value == 'fossil'
        assert fossil_config.Command.REPO.value == '-R'
        assert fossil_config.Command.TIMELINE.value == 'timeline'
        assert fossil_config.Command.VERBOSE.value == '--verbose'
        assert fossil_config.Command.TYPE.value == '--type'
        assert fossil_config.Command.CI.value == 'ci'
        assert fossil_config.Command.LIMIT.value == '--limit'
        assert fossil_config.Command.NO_LIMIT.value == '0'
        assert fossil_config.Command.FULL.value == '--full'
        assert fossil_config.Command.NEW.value == 'new'
        assert fossil_config.Command.USER.value == 'user'
        assert fossil_config.Command.DEFAULT.value == 'default'
        assert fossil_config.Command.CONTACT.value == 'contact'
        assert fossil_config.Command.TEMPLATE.value == '--template'
        assert fossil_config.Command.ADMIN_USER.value == '--admin-user'
        assert fossil_config.Command.DATE_OVERRIDE.value == '--date-override'
        assert fossil_config.Command.PROJECT_NAME.value == '--project-name'
        assert fossil_config.Command.PROJECT_DESC.value == '--project-desc'
        assert fossil_config.Command.BRANCH.value == 'branch'
        assert fossil_config.Command.LIST.value == 'list'
        assert fossil_config.Command.ALL.value == '--all'
        assert fossil_config.Command.OPEN.value == 'open'
        assert fossil_config.Command.CLOSE.value == 'close'
        assert fossil_config.Command.WORKDIR.value == '--workdir'
        assert fossil_config.Command.CLOSED.value == '--closed'
        assert fossil_config.Command.INFO.value == 'info'
        assert fossil_config.Command.DIFF.value == 'diff'
        assert fossil_config.Command.BRIEF.value == '--brief'
        assert fossil_config.Command.FROM.value == '--from'
        assert fossil_config.Command.TO.value == '--to'
        assert fossil_config.Command.OUTFILE.value == '--out'
        assert fossil_config.Command.CAT.value == 'cat'
        assert fossil_config.Command.VERSION.value == '-r'
        assert fossil_config.Command.ADD.value == 'add'
        assert fossil_config.Command.COMMENT.value == '--comment'
        assert fossil_config.Command.TAG.value == '--tag'
        assert fossil_config.Command.USER_OVERRIDE.value == '--user-override'
        assert fossil_config.Command.HASH.value == '--hash'
        assert fossil_config.Command.COMMIT.value == 'commit'

        assert isinstance(fossil_config.Command.FOSSIL, fossil_config.Command)
        assert len(fossil_config.Command) == 39

    def test_config_timeline_data_attributes(self):
        """Test attributes of TimelineData enum."""
        td = fossil_config.TimelineData
        assert td.INIT_CHECKIN.value == 'initial empty check-in'
        assert td.END_MARK.value == '+++ end of timeline'
        assert td.COMMITS_KEY.value == 'commits'
        assert td.COMMIT_SEP.value == '\\n(?=Commit:\\s+)'
        assert td.HASH_KEY.value == 'uuid'
        assert td.DATE_KEY.value == 'date'
        assert td.AUTHOR_KEY.value == 'author'
        assert td.COMMENT_KEY.value == 'comment'
        assert td.BRANCH_KEY.value == 'branch'
        assert td.TAGS_KEY.value == 'tags'
        assert td.PHASE_KEY.value == 'phase'
        assert td.CHANGES_KEY.value == 'changes'
        assert (
            td.HASH_PATTERN.value
            == '^(?P<label>Commit:\\s+)(?P<uuid>[0-9a-f]+)$'
        )
        assert td.DATE_PATTERN.value == '^(?P<label>Date):\\s+(?P<date>.+)$'
        assert (
            td.AUTHOR_PATTERN.value == '^(?P<label>Author):\\s+(?P<author>.+)?'
        )
        assert (
            td.COMMENT_PATTERN.value
            == '^(?P<label>Comment):\\s+(?P<comment>.+)$'
        )
        assert (
            td.BRANCH_PATTERN.value == '^(?P<label>Branch):\\s+(?P<branch>.+)$'
        )
        assert td.TAGS_PATTERN.value == '^(?P<label>Tags):\\s+(?P<tags>.+)$'
        assert td.TAG_REGEX.value == '?P<tag>[\\w-]+'
        assert (
            td.PHASE_PATTERN.value
            == '^(?P<label>Phase):\\s+\\*?(?P<phase>LEAF|PUBLISHED|FROZEN)?\\*?'
        )
        assert (
            td.CHANGE_PATTERN.value
            == '^\\s+(?P<change>ADDED|EDITED|DELETED)\\s(?P<filename>.+)$'
        )
        assert (
            td.PATH_PATTERN.value == '^(?P<path>.*[\\/])?(?P<file>[^/\\\\]+$)'
        )

        assert isinstance(td.HASH_KEY, fossil_config.TimelineData)
        assert len(td) == 22

    @pytest.mark.parametrize(
        'method_name, enum_member',
        [
            ('commit_pattern', 'COMMIT_SEP'),
            ('hash_pattern', 'HASH_PATTERN'),
            ('date_pattern', 'DATE_PATTERN'),
            ('author_pattern', 'AUTHOR_PATTERN'),
            ('comment_pattern', 'COMMENT_PATTERN'),
            ('branch_pattern', 'BRANCH_PATTERN'),
            ('tags_pattern', 'TAGS_PATTERN'),
            ('phase_pattern', 'PHASE_PATTERN'),
            ('change_pattern', 'CHANGE_PATTERN'),
        ],
    )
    def test_config_timeline_data_pattern_methods(
        self, method_name, enum_member
    ):
        """Test pattern compilation methods of TimelineData."""
        member_instance = getattr(fossil_config.TimelineData, enum_member)
        method = getattr(member_instance, method_name)
        pattern_obj = method()
        assert isinstance(pattern_obj, re.Pattern)
        assert pattern_obj.pattern == member_instance.value

    def test_config_info_data_attributes(self):
        """Test member values of the InfoData enum."""
        info_data = fossil_config.InfoData
        assert info_data.INIT_HASH.value == '^comment:\\s+(?P<init>)\\s.+\\n'
        assert info_data.PARENT_KEY.value == 'parent'
        assert (
            info_data.PARENT_DATA_PATTERN.value
            == '^parent:\\s+(?P<uuid>.+?)\\s.+\\n'
        )

        assert isinstance(info_data.PARENT_KEY, fossil_config.InfoData)
        assert len(info_data) == 3

    @pytest.mark.parametrize(
        'method_name, enum_member',
        [
            ('init_pattern', 'INIT_HASH'),
            ('parent_pattern', 'PARENT_DATA_PATTERN'),
        ],
    )
    def test_info_data_pattern_methods(self, method_name, enum_member):
        """Test pattern compilation methods of InfoData."""
        member_instance = getattr(fossil_config.InfoData, enum_member)
        method = getattr(member_instance, method_name)
        pattern_obj = method()
        assert isinstance(pattern_obj, re.Pattern)
        assert pattern_obj.pattern == member_instance.value

    def test_config_fossil_attributes(self):
        """Test member values of the Fossil enum."""
        f = fossil_config.Fossil
        assert f.default_timeout.value == 180
        assert f.process_error.value == 'FOSSIL_PROCESS_ERROR'
        assert f.timeout_error.value == 'FOSSIL_TIMEOUT_ERROR'
        assert f.args.value == 'args'
        assert f.cmd.value == 'cmd'
        assert f.output.value == 'output'
        assert f.return_code.value == 'return_code'
        assert f.default_return_code.value == 1
        assert f.stderr.value == 'stderr'
        assert f.timeout.value == 'timeout'
        assert f.step.value == 'step'
        assert f.init.value == 'New repository initialization'
        assert f.username_setup.value == 'username_setup'
        assert f.user_contact.value == 'user_contact'

        assert isinstance(f.step, fossil_config.Fossil)
        assert len(f) == 14
