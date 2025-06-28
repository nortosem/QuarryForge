"""Unit tests for the quarryforge.util.fossil_util module.

This test suite provides comprehensive, MC/DC-focused coverage for all
command-generation utility functions. It uses mocking to isolate the functions
from the model layer and verifies that command lists are correctly assembled
based on both required and optional arguments.
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from quarryforge.config import fossil_config as fc
from quarryforge.model import FossilRepo
from quarryforge.util import fossil_util


@pytest.fixture
def mock_repo() -> MagicMock:
    """Fixture to create a mock FossilRepo object."""
    repo = MagicMock(spec=FossilRepo)
    repo.__str__.return_value = '/mock/repo.fossil'
    return repo


class TestFossilUtilCommands:
    """Tests for each command-generating function in fossil_util."""

    def test_get_raw_timeline(self, mock_repo: MagicMock):
        """Verify the command to get the full, verbose timeline."""
        expected_cmd = [
            fc.COMMAND.FOSSIL,
            fc.COMMAND.TIMELINE,
            fc.COMMAND.VERBOSE,
            fc.COMMAND.FULL,
            fc.COMMAND.LIMIT,
            fc.COMMAND.NO_LIMIT,
            fc.COMMAND.TYPE,
            fc.COMMAND.CI,
            fc.COMMAND.REPO,
            str(mock_repo),
        ]
        assert fossil_util.get_raw_timeline(mock_repo) == expected_cmd

    @pytest.mark.parametrize(
        'template, project_name, project_desc, expected_extras',
        [
            (
                MagicMock(__str__=lambda s: '/template.fossil'),
                'QF',
                'Desc',
                [
                    fc.COMMAND.TEMPLATE,
                    '/template.fossil',
                    fc.COMMAND.PROJECT_NAME,
                    'QF',
                    fc.COMMAND.PROJECT_DESC,
                    'Desc',
                ],
            ),
            (None, None, None, []),
            (
                MagicMock(__str__=lambda s: '/template.fossil'),
                None,
                None,
                [fc.COMMAND.TEMPLATE, '/template.fossil'],
            ),
            (None, 'QF', None, [fc.COMMAND.PROJECT_NAME, 'QF']),
            (None, None, 'Desc', [fc.COMMAND.PROJECT_DESC, 'Desc']),
        ],
    )
    def test_rebuild_init_mcdc(
        self,
        mock_repo: MagicMock,
        template,
        project_name,
        project_desc,
        expected_extras,
    ):
        """Test `rebuild_init` with all combinations of optional arguments."""
        base_cmd = [
            fc.COMMAND.FOSSIL,
            fc.COMMAND.NEW,
            fc.COMMAND.ADMIN_USER,
            'user1',
            fc.COMMAND.DATE_OVERRIDE,
            '2023-01-01',
        ]
        final_cmd = [str(mock_repo)]
        expected_cmd = base_cmd + expected_extras + final_cmd

        cmd = fossil_util.rebuild_init(
            username='user1',
            date_override='2023-01-01',
            new_repo=mock_repo,
            template=template,
            project_name=project_name,
            project_desc=project_desc,
        )
        assert cmd == expected_cmd

    def test_set_default_user(self, mock_repo: MagicMock):
        """Verify the command to set the default user."""
        expected_cmd = [
            fc.COMMAND.FOSSIL,
            fc.COMMAND.USER,
            fc.COMMAND.DEFAULT,
            'user1',
            fc.COMMAND.REPO,
            str(mock_repo),
        ]
        assert fossil_util.set_default_user('user1', mock_repo) == expected_cmd

    def test_set_user_contact(self, mock_repo: MagicMock):
        """Verify the command to set a user's contact email."""
        expected_cmd = [
            fc.COMMAND.FOSSIL,
            fc.COMMAND.USER,
            fc.COMMAND.CONTACT,
            'user1',
            'user@example.com',
            fc.COMMAND.REPO,
            str(mock_repo),
        ]
        cmd = fossil_util.set_user_contact(
            'user1', 'user@example.com', mock_repo
        )
        assert cmd == expected_cmd

    def test_open_rebuild(self, mock_repo: MagicMock):
        """Verify the command to open a repository checkout."""
        workdir = Path('/tmp/workdir')
        expected_cmd = [
            fc.COMMAND.FOSSIL,
            fc.COMMAND.OPEN,
            str(mock_repo),
            fc.COMMAND.WORKDIR,
            str(workdir),
        ]
        assert fossil_util.open_rebuild(mock_repo, workdir) == expected_cmd

    def test_close_rebuild(self):
        """Verify the command to close a repository checkout."""
        expected_cmd = [fc.COMMAND.FOSSIL, fc.COMMAND.CLOSE]
        assert fossil_util.close_rebuild() == expected_cmd

    def test_get_parent_hash(self, mock_repo: MagicMock):
        """Verify the command to get info for a specific version."""
        version = 'a1b2c3d4'
        expected_cmd = [
            fc.COMMAND.FOSSIL,
            fc.COMMAND.INFO,
            version,
            fc.COMMAND.REPO,
            str(mock_repo),
        ]
        assert fossil_util.get_parent_hash(version, mock_repo) == expected_cmd

    def test_get_file_changes(self, mock_repo: MagicMock):
        """Verify the command to get a brief diff between two versions."""
        from_v = 'a1b2c3d4'
        to_v = 'e5f6a7b8'
        expected_cmd = [
            fc.COMMAND.FOSSIL,
            fc.COMMAND.DIFF,
            fc.COMMAND.BRIEF,
            fc.COMMAND.FROM,
            from_v,
            fc.COMMAND.TO,
            to_v,
            fc.COMMAND.REPO,
            str(mock_repo),
        ]
        cmd = fossil_util.get_file_changes(from_v, to_v, mock_repo)
        assert cmd == expected_cmd

    def test_get_file_content(self, mock_repo: MagicMock):
        """Verify the command to cat a file's content to an outfile."""
        expected_cmd = [
            fc.COMMAND.FOSSIL,
            fc.COMMAND.CAT,
            'src/main.c',
            fc.COMMAND.OUTFILE,
            '/tmp/main.c.out',
            fc.COMMAND.VERSION,
            'a1b2c3d4',
            fc.COMMAND.REPO,
            str(mock_repo),
        ]
        cmd = fossil_util.get_file_content(
            'src/main.c', '/tmp/main.c.out', 'a1b2c3d4', mock_repo
        )
        assert cmd == expected_cmd

    def test_ls_branches(self, mock_repo: MagicMock):
        """Verify the command to list all branches."""
        expected_cmd = [
            fc.COMMAND.FOSSIL,
            fc.COMMAND.BRANCH,
            fc.COMMAND.LIST,
            fc.COMMAND.ALL,
            fc.COMMAND.REPO,
            str(mock_repo),
        ]
        assert fossil_util.ls_branches(mock_repo) == expected_cmd

    def test_closed_branches(self, mock_repo: MagicMock):
        """Verify the command to list closed branches."""
        expected_cmd = [
            fc.COMMAND.FOSSIL,
            fc.COMMAND.BRANCH,
            fc.COMMAND.LIST,
            fc.COMMAND.CLOSED,
            fc.COMMAND.REPO,
            str(mock_repo),
        ]
        assert fossil_util.closed_branches(mock_repo) == expected_cmd

    def test_add_files(self):
        """Verify the command to add multiple files."""
        files = [Path('file1.txt'), Path('dir/file2.py')]
        expected_cmd = [
            fc.COMMAND.FOSSIL,
            fc.COMMAND.ADD,
            'file1.txt',
            'dir/file2.py',
        ]
        assert fossil_util.add_files(files) == expected_cmd

    @pytest.mark.parametrize(
        'branch, tag, expected_extras',
        [
            # MC/DC: Both branch and tag provided
            (
                'feature-x',
                'v1.1',
                ['--branch', 'feature-x', fc.COMMAND.TAG, 'v1.1'],
            ),
            # MC/DC: Neither provided
            (None, None, []),
            # MC/DC: Only branch provided
            ('feature-x', None, ['--branch', 'feature-x']),
            # MC/DC: Only tag provided
            (None, 'v1.1', [fc.COMMAND.TAG, 'v1.1']),
        ],
    )
    def test_commit_mcdc(self, branch, tag, expected_extras):
        """Test the commit command with all combinations of optional arguments."""
        files = [Path('file1.txt')]
        base_cmd = [
            fc.COMMAND.FOSSIL,
            fc.COMMAND.COMMIT,
            fc.COMMAND.HASH,
            fc.COMMAND.DATE_OVERRIDE,
            '2023-01-01',
            fc.COMMAND.USER_OVERRIDE,
            'user1',
            fc.COMMAND.COMMENT,
            'Commit message',
        ]
        final_cmd = ['file1.txt']
        expected_cmd = base_cmd + expected_extras + final_cmd

        cmd = fossil_util.commit(
            date_override='2023-01-01',
            user_override='user1',
            comment='Commit message',
            branch=branch,
            tag=tag,
            files=files,
        )
        assert cmd == expected_cmd
