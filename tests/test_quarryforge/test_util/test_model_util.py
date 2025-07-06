"""Unit tests for the quarryforge.util.model_util module.

This suite provides comprehensive coverage for the validation orchestrator
functions, `viable_fossil_repo` and `viable_fossil_commit`.
"""

import logging
from pathlib import Path
from unittest.mock import ANY, MagicMock, patch

import pytest

from quarryforge.exception import model_exception
from quarryforge.util import model_util

DUMMY_EXCEPTION_TYPE = model_exception.FossilRepoError


@pytest.fixture
def mock_validation_util(mocker: MagicMock) -> MagicMock:
    """Mock the entire validation_util module.

    This is the core fixture for isolating model_util from its dependencies.
    """
    validation_functions_to_mock = [
        'is_type_str',
        'is_str_not_empty',
        'is_type_path',
        'resolve_path_arg',
        'exist',
        'not_exist',
        'is_file',
        'is_dir',
        'is_read_ok',
        'is_write_ok',
        'content_type_error_str_list',
        'content_empty_error_str_list',
        'content_type_error_str_tuple_list',
        'content_empty_error_str_tuple_list',
    ]
    mock_module = mocker.patch('quarryforge.util.model_util.validation_util')
    for func_name in validation_functions_to_mock:
        mock_func = mocker.Mock(side_effect=lambda arg, **kwargs: arg)
        setattr(mock_module, func_name, mock_func)

    return mock_module


class TestViableFossilRepo:
    """Test for the viable_fossil_repo validation function."""

    def test_success_existing_repo(
            self, mock_validation_util: MagicMock, tmp_path: Path):
        """Test success path for an existing repo (is_new=False)."""
        logging.info('Testing viable_fossil_repo: success path for existing repo.')
        repo_file = tmp_path / 'repo.fossil'
        workdir = tmp_path / 'work'

        file_out, workdir_out = model_util.viable_fossil_repo(
            file=repo_file, workdir=workdir, is_new=False,
            exception=DUMMY_EXCEPTION_TYPE
        )
        assert file_out is repo_file
        assert workdir_out is workdir

        # Assert the correct validation chain was called
        mock_validation_util.exist.assert_any_call(
            arg=repo_file,
            exception=DUMMY_EXCEPTION_TYPE,
            error_builder=ANY
        )
        mock_validation_util.is_file.assert_called_once_with(
            arg=repo_file,
            exception=DUMMY_EXCEPTION_TYPE,
            error_builder=ANY
        )
        mock_validation_util.is_read_ok.assert_called_once_with(
            arg=repo_file,
            exception=DUMMY_EXCEPTION_TYPE,
            error_builder=ANY
        )
        assert mock_validation_util.not_exist.call_count == 0

    def test_success_new_repo(
            self, mock_validation_util: MagicMock, tmp_path: Path):
        """Test success path for a new repo (is_new=True)."""
        logging.info('Testing viable_fossil_repo: success path for new repo.')
        repo_file = tmp_path / 'new_repo.fossil'
        workdir = tmp_path / 'work'

        model_util.viable_fossil_repo(
            file=repo_file, workdir=workdir,
            is_new=True, exception=DUMMY_EXCEPTION_TYPE
        )
        mock_validation_util.not_exist.assert_called_once_with(
            arg=repo_file,
            exception=DUMMY_EXCEPTION_TYPE,
            error_builder=ANY
        )
        mock_validation_util.exist.assert_any_call(
            arg=repo_file.parent,
            exception=DUMMY_EXCEPTION_TYPE,
            error_builder=ANY
        )
        mock_validation_util.is_dir.assert_any_call(
            arg=repo_file.parent,
            exception=DUMMY_EXCEPTION_TYPE,
            error_builder=ANY
        )
        mock_validation_util.is_write_ok.assert_any_call(
            arg=repo_file.parent,
            exception=DUMMY_EXCEPTION_TYPE,
            error_builder=ANY
        )

    def test_failure_same_directory(
            self, mock_validation_util: MagicMock, tmp_path: Path):
        """Test failure when repo parent directory and workdir are the same."""
        logging.info('Testing viable_fossil_repo: failure on same directory.')
        workdir = tmp_path
        repo_file = workdir / "repo.fossil"

        with pytest.raises(DUMMY_EXCEPTION_TYPE):
            model_util.viable_fossil_repo(
                file=repo_file,
                workdir=workdir,
                is_new=True,
                exception=DUMMY_EXCEPTION_TYPE
            )

    def test_failure_on_validation_step(
            self, mock_validation_util: MagicMock, tmp_path: Path):
        """Test that an exception from validation_util is propagated correctly."""
        logging.info('Testing viable_fossil_repo: exception propagation.')
        mock_validation_util.exist.side_effect = DUMMY_EXCEPTION_TYPE(
            code="FAIL",
            message="Path does not exist",
            user_message="user fail",
            details={}
        )
        with pytest.raises(DUMMY_EXCEPTION_TYPE, match='Path does not exist'):
            model_util.viable_fossil_repo(
                file=tmp_path / 'f.fossil',
                workdir=tmp_path / 'w',
                is_new=False,
                exception=DUMMY_EXCEPTION_TYPE
            )


class TestViableFossilCommit:
    """Tests for the viable_fossil_commit validation function."""

    @pytest.fixture
    def sample_valid_args(self, sample_commit_data):
        """Provide a valid dictionary of all arguments for the function."""
        args = sample_commit_data.copy()
        args['exception'] = DUMMY_EXCEPTION_TYPE
        return args

    @pytest.mark.parametrize(
        'branch, tags, phase, changes',
        [
            ('trunk', ['v1'], ['phase1'], [('A', 'f1')]), # All optional args
            (None, None, None, None),                    # No optional args present
            ('trunk', None, None, None),                 # Only branch
            (None, ['v1'], None, None),                  # Only tags
            (None, None, None, [('A', 'f1')]),           # Only changes
        ]
    )
    def test_success_paths_mcdc(
        self, mock_validation_util: MagicMock,
        sample_valid_args, branch, tags, phase, changes
    ):
        """Test success paths with all combinations of optional arguments."""
        logging.info(
            (
                'Testing viable_fossil_commit: success path with branch=%s,'
                ' tags=%s, phase=%s, changes=%s'
            ),
            bool(branch), bool(tags), bool(phase), bool(changes)
        )
        # Update args for the current parameterized test case
        sample_valid_args.update({
            'branch': branch, 'tags': tags, 'phase': phase, 'changes': changes
        })

        result = model_util.viable_fossil_commit(**sample_valid_args)

        # Assert required fields were validated
        assert mock_validation_util.is_str_not_empty.call_count >= 4

        # Assert optional fields were validated ONLY if they were provided
        assert (mock_validation_util.is_str_not_empty.call_count == 5) == bool(branch)
        assert (mock_validation_util.content_type_error_str_list.call_count >= 1) == bool(tags or phase)

        # Verify the returned tuple has the correct values
        assert result[0] == sample_valid_args['uuid']
        assert result[4] == branch
        assert result[5] == tags

    def test_failure_on_required_field(self, mock_validation_util: MagicMock, sample_valid_args):
        """Test that an exception is raised if a required field is invalid."""
        logging.info('Testing viable_fossil_commit: failure on required field.')
        mock_validation_util.is_str_not_empty.side_effect = (
            DUMMY_EXCEPTION_TYPE(
                code='FAIL',
                message='Empty string',
                user_message='user fail',
                details={}
            )
        )
        with pytest.raises(DUMMY_EXCEPTION_TYPE, match='Empty string'):
            model_util.viable_fossil_commit(**sample_valid_args)
