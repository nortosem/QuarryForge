"""Unit tests for the quarryforge.util.fossil_util module.

This suite provides comprehensive, MC/DC-focused coverage for all
command-generation utility functions.
"""

import logging
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from quarryforge.config import fossil_config as fc
from quarryforge.util import fossil_util


class TestFossilUtilCommands:
    """Tests for each command-generating function in fossil_util."""

    def test_get_raw_timeline(self, mock_repo: MagicMock):
        """Verify the command to get the full, verbose timeline."""
        logging.info('Testing fossil_util.get_raw_timeline.')
        expected_cmd = [
            fc.Command.FOSSIL, fc.Command.TIMELINE, fc.Command.VERBOSE,
            fc.Command.FULL, fc.Command.LIMIT, fc.Command.NO_LIMIT,
            fc.Command.TYPE, fc.Command.CI, fc.Command.REPO, str(mock_repo),
        ]
        assert fossil_util.get_raw_timeline(mock_repo) == expected_cmd

    @pytest.mark.parametrize(
        'template, project_name, project_desc, expected_extras',
        [
            (MagicMock(spec=Path, __str__=lambda s: '/tmpl'), 'QF', 'Desc',
             [fc.Command.TEMPLATE, '/tmpl', fc.Command.PROJECT_NAME,
              'QF', fc.Command.PROJECT_DESC, 'Desc']
             ),
            (None, None, None, []),
            (MagicMock(spec=Path, __str__=lambda s: '/tmpl'), None, None,
             [fc.Command.TEMPLATE, '/tmpl']
             ),
            (None, 'QF', None, [fc.Command.PROJECT_NAME, 'QF']),
            (None, None, 'Desc', [fc.Command.PROJECT_DESC, 'Desc']),
        ]
    )
    def test_rebuild_init_mcdc(self, mock_repo: MagicMock, template, project_name, project_desc, expected_extras):
        """Test `rebuild_init` with all combinations of optional arguments."""
        logging.info(
            'Testing fossil_util.rebuild_init: template=%s, name=%s, desc=%s',
            bool(template), bool(project_name), bool(project_desc)
        )
        base_cmd = [
            fc.Command.FOSSIL, fc.Command.NEW, fc.Command.ADMIN_USER, 'user1',
            fc.Command.DATE_OVERRIDE, '2023-01-01',
        ]
        final_cmd = [str(mock_repo)]
        expected_cmd = base_cmd + expected_extras + final_cmd
        cmd = fossil_util.rebuild_init(
            'user1', '2023-01-01', mock_repo, template,
            project_name, project_desc
        )
        assert cmd == expected_cmd

    def test_set_default_user(self, mock_repo: MagicMock):
        """Verify command to set the default user."""
        logging.info('Testing fossil_util.set_default_user.')
        expected_cmd = [
            fc.Command.FOSSIL, fc.Command.USER,
            fc.Command.DEFAULT, 'test_user',
            fc.Command.REPO, str(mock_repo)
        ]
        assert fossil_util.set_default_user(
            'test_user', mock_repo) == expected_cmd

    def test_set_user_contact(self, mock_repo: MagicMock):
        """Verify command to set user contact info."""
        logging.info('Testing fossil_util.set_user_contact.')
        expected_cmd = [
            fc.Command.FOSSIL, fc.Command.USER, fc.Command.CONTACT, 'test_user',
            'user@example.com', fc.Command.REPO, str(mock_repo)
        ]
        assert fossil_util.set_user_contact('test_user', 'user@example.com', mock_repo) == expected_cmd

    def test_open_repo(self, mock_repo: MagicMock):
        """Verify command to open a repository."""
        logging.info('Testing fossil_util.open_repo.')
        workdir = Path('/tmp/workdir')
        expected_cmd = [
            fc.Command.FOSSIL, fc.Command.OPEN, str(mock_repo),
            fc.Command.WORKDIR, str(workdir)
        ]
        assert fossil_util.open_repo(mock_repo, workdir) == expected_cmd

    def test_close_repo(self):
        """Verify command to close a repository."""
        logging.info("Testing fossil_util.close_repo.")
        assert fossil_util.close_repo() == [fc.Command.FOSSIL, fc.Command.CLOSE]

    def test_get_parent_hash(self, mock_repo: MagicMock):
        """Verify command to get info for a specific version."""
        logging.info('Testing fossil_util.get_parent_hash.')
        version = 'a1b2c3d4e5f6'
        expected_cmd = [
            fc.Command.FOSSIL, fc.Command.INFO,
            version, fc.Command.REPO, str(mock_repo)
        ]
        assert fossil_util.get_parent_hash(version, mock_repo) == expected_cmd

    def test_get_file_changes(self, mock_repo: MagicMock):
        """Verify command to diff between two versions."""
        logging.info('Testing fossil_util.get_file_changes.')
        expected_cmd = [
            fc.Command.FOSSIL, fc.Command.DIFF, fc.Command.BRIEF,
            fc.Command.FROM, 'from_ver', fc.Command.TO, 'to_ver',
            fc.Command.REPO, str(mock_repo)
        ]
        assert fossil_util.get_file_changes('from_ver', 'to_ver', mock_repo) == expected_cmd

    def test_get_file_content(self, mock_repo: MagicMock):
        """Verify command to cat a file at a specific version."""
        logging.info('Testing fossil_util.get_file_content.')
        expected_cmd = [
            fc.Command.FOSSIL, fc.Command.CAT, 'file.txt',
            fc.Command.OUTFILE, '/tmp/out.txt', fc.Command.VERSION, 'a1b2c3',
            fc.Command.REPO, str(mock_repo)
        ]
        cmd = fossil_util.get_file_content('file.txt', '/tmp/out.txt', 'a1b2c3', mock_repo)
        assert cmd == expected_cmd

    def test_ls_branches(self, mock_repo: MagicMock):
        """Verify command to list all branches."""
        logging.info('Testing fossil_util.ls_branches.')
        expected_cmd = [
            fc.Command.FOSSIL, fc.Command.BRANCH, fc.Command.LIST,
            fc.Command.ALL, fc.Command.REPO, str(mock_repo)
        ]
        assert fossil_util.ls_branches(mock_repo) == expected_cmd

    def test_closed_branches(self, mock_repo: MagicMock):
        """Verify command to list closed branches."""
        logging.info('Testing fossil_util.closed_branches.')
        expected_cmd = [
            fc.Command.FOSSIL, fc.Command.BRANCH, fc.Command.LIST,
            fc.Command.CLOSED, fc.Command.REPO, str(mock_repo)
        ]
        assert fossil_util.closed_branches(mock_repo) == expected_cmd

    def test_add_files(self):
        """Verify command to add a list of files."""
        logging.info('Testing fossil_util.add_files.')
        files = [Path('file1.txt'), Path('dir/file2.py')]
        expected_cmd = [fc.Command.FOSSIL, fc.Command.ADD, 'file1.txt', 'dir/file2.py']
        assert fossil_util.add_files(files) == expected_cmd

    @pytest.mark.parametrize(
        'branch, tag, expected_extras',
        [
            ('feature', 'v1.0',
             ['--branch', 'feature', fc.Command.TAG, 'v1.0']
             ),
            (None, None, []),
            ('feature', None, ['--branch', 'feature']),
            (None, 'v1.0', [fc.Command.TAG, 'v1.0']),
        ]
    )
    def test_commit_mcdc(self, branch, tag, expected_extras):
        """Test commit command with all combinations of optional arguments."""
        logging.info(
            'Testing fossil_util.commit: branch=%s, tag=%s.'
            , bool(branch), bool(tag)
        )
        files = [Path('a.txt')]
        base_cmd = [
            fc.Command.FOSSIL, fc.Command.COMMIT, fc.Command.HASH,
            fc.Command.DATE_OVERRIDE, 'date', fc.Command.USER_OVERRIDE, 'user',
            fc.Command.COMMENT, 'comment'
        ]
        final_cmd = [str(f) for f in files]
        expected_cmd = base_cmd + expected_extras + final_cmd
        cmd = fossil_util.commit('date', 'user', 'comment', branch, tag, files)
        assert cmd == expected_cmd
