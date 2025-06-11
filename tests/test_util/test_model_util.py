"""Test Model Utility module."""
import os
import pytest
from pathlib import Path
import unittest
from unittest.mock import MagicMock

from quarryforge.util import model_util
from quarryforge.exception import base_exception


class ModelTestException(base_exception.ModelError):
    """Custom exception class for testing the model_util module."""
    def __init__(
            self,
            message='Model Test Exception',
            code='TEST_CODE',
            user_message='A test error occurred.',
            details=None
    ):
        if details is None:
            details = {}
        super().__init__(
            message=message,
            code='TEST_CODE',
            user_message='A test error occurred.',
            details={}
        )


@pytest.fixture
def mock_configs(mocker):
    """Mocks configuration objects used in model_util."""
    mock_fossil_repo_config = MagicMock()
    mock_fossil_repo_config._fields = ('repo_file', 'is_new', 'work_dir')
    mocker.patch(
        'quarryforge.util.model_util.model_config.FOSSIL_REPO',
        mock_fossil_repo_config
    )
    mocker.patch('quarryforge.util.model_util.model_ec.FossilRepoErrorBuilder')
    mocker.patch('quarryforge.util.model_util.model_ec.FossilCommitErrorBuilder')


@pytest.fixture
def mock_validation_util(mocker):
    """
    Patches all validation_util functions used by model_util.
    Returns a dictionary of the mock objects for individual configuration.
    By default, mocks are configured to pass validation (return the 'arg').
    """
    validation_functions = [
        'is_type_path', 'resolve_path_arg', 'exist', 'not_exist',
        'is_file', 'is_dir', 'is_read_ok', 'is_write_ok', 'is_type_str',
        'is_str_not_empty', 'content_type_error_str_list',
        'content_empty_error_str_list',
        'content_type_error_str_tuple_list',
        'content_empty_error_str_tuple_list',
    ]

    mocks = {}
    for func_name in validation_functions:
        mock_func = mocker.patch(
            f'quarryforge.util.validation_util.{func_name}'
        )
        # Default behavior: pass-through validation
        mock_func.side_effect = lambda arg, **kwargs: arg
        mocks[func_name] = mock_func

    return mocks


@pytest.mark.usefixtures('mock_configs')
class TestViableFossilRepo:

    def test_pass_existing_repo(self, tmp_path, mock_validation_util):
        """Tests successful validation of an existing repository path."""
        repo_file = tmp_path / 'repo.fossil'
        work_dir = tmp_path / 'work'

        # Simulate path resolution
        mock_validation_util['resolve_path_arg'].side_effect = [
            repo_file, work_dir
        ]

        result_file, result_workdir = model_util.viable_fossil_repo(
            file=str(repo_file),
            workdir=str(work_dir),
            is_new=False,
            exception=ModelTestException
        )

        assert result_file == repo_file
        assert result_workdir == work_dir

        # Verify calls for existing repo validation
        mock_validation_util['exist'].assert_any_call(
            arg=repo_file,
            exception=ModelTestException,
            error_builder=unittest.mock.ANY
        )
        mock_validation_util['is_file'].assert_called_once_with(
            arg=repo_file,
            exception=ModelTestException,
            error_builder=unittest.mock.ANY
        )
        mock_validation_util['is_read_ok'].assert_called_once_with(
            arg=repo_file,
            exception=ModelTestException,
            error_builder=unittest.mock.ANY
        )
        mock_validation_util['not_exist'].assert_not_called()

        # Verify calls for workdir validation
        mock_validation_util['exist'].assert_any_call(
            arg=work_dir,
            exception=ModelTestException,
            error_builder=unittest.mock.ANY
        )
        mock_validation_util['is_dir'].assert_called_once_with(
            arg=work_dir,
            exception=ModelTestException,
            error_builder=unittest.mock.ANY
        )
        mock_validation_util['is_write_ok'].assert_any_call(
            arg=work_dir,
            exception=ModelTestException,
            error_builder=unittest.mock.ANY
        )


    def test_pass_new_repo(self, tmp_path, mock_validation_util):
        """Tests successful validation for creating a new repository."""
        repo_file = tmp_path / 'new_repo.fossil'
        work_dir = tmp_path / 'work'
        parent_dir = repo_file.parent

        # Simulate path resolution
        mock_validation_util['resolve_path_arg'].side_effect = [
            repo_file, work_dir
        ]

        result_file, result_workdir = model_util.viable_fossil_repo(
            file=repo_file,
            workdir=work_dir,
            is_new=True,
            exception=ModelTestException
        )

        assert result_file == repo_file
        assert result_workdir == work_dir

        # Verify calls for new repo validation
        mock_validation_util['not_exist'].assert_called_once_with(
            arg=repo_file,
            exception=ModelTestException,
            error_builder=unittest.mock.ANY
        )
        mock_validation_util['exist'].assert_any_call(
            arg=parent_dir,
            exception=ModelTestException,
            error_builder=unittest.mock.ANY
        )
        mock_validation_util['is_dir'].assert_any_call(
            arg=parent_dir,
            exception=ModelTestException,
            error_builder=unittest.mock.ANY
        )
        mock_validation_util['is_write_ok'].assert_any_call(
            arg=parent_dir,
            exception=ModelTestException,
            error_builder=unittest.mock.ANY
        )

        # Verify workdir validation
        mock_validation_util['exist'].assert_any_call(
            arg=work_dir,
            exception=ModelTestException,
            error_builder=unittest.mock.ANY
        )
        mock_validation_util['is_dir'].assert_any_call(
            arg=work_dir,
            exception=ModelTestException,
            error_builder=unittest.mock.ANY
        )
        mock_validation_util['is_write_ok'].assert_any_call(
            arg=work_dir,
            exception=ModelTestException,
            error_builder=unittest.mock.ANY
        )


    @pytest.mark.parametrize(
        'is_new_flag',
        [True, False], ids=['new', 'existing']
    )
    @pytest.mark.parametrize('failed_validation, arg_name', [
        ('is_type_path', 'file'),
        ('is_type_path', 'workdir'),
        ('resolve_path_arg', 'file'),
        ('resolve_path_arg', 'workdir'),
    ])
    def test_fail_common_validations(
            self,
            tmp_path,
            mock_validation_util,
            is_new_flag,
            failed_validation,
            arg_name
    ):
        """Tests failures in initial validation steps common to new and
        existing repos.
        """
        mock_validation_util[
            failed_validation
        ].side_effect = ModelTestException

        with pytest.raises(ModelTestException):
            model_util.viable_fossil_repo(
                file=tmp_path / 'repo.fossil',
                workdir=tmp_path / 'work',
                is_new=is_new_flag,
                exception=ModelTestException
            )

        assert mock_validation_util[failed_validation].called

    def test_fail_new_repo_already_exists(self, tmp_path, mock_validation_util):
        """Tests failure when creating new repo but the file already exists.
        """
        mock_validation_util['not_exist'].side_effect = ModelTestException

        with pytest.raises(ModelTestException):
            model_util.viable_fossil_repo(
                file=tmp_path / 'repo.fossil',
                workdir=tmp_path / 'work',
                is_new=True,
                exception=ModelTestException
            )
        mock_validation_util['not_exist'].assert_called_once()

    def test_fail_new_repo_parent_dir_nonexistent(self, tmp_path, mock_validation_util):
        """Tests failure when parent dir for a new repo doesn't exist."""
        # The first 'exist' call is for the parent dir
        mock_validation_util['exist'].side_effect = ModelTestException

        with pytest.raises(ModelTestException):
            model_util.viable_fossil_repo(
                file=tmp_path / 'repo.fossil',
                workdir=tmp_path / 'work',
                is_new=True,
                exception=ModelTestException
            )
        mock_validation_util['exist'].assert_called_once()

    def test_fail_new_repo_parent_dir_unwritable(self, tmp_path, mock_validation_util):
        """Tests failure when parent dir for a new repo is not writable."""
        # The first 'is_write_ok' call is for the parent dir
        mock_validation_util['is_write_ok'].side_effect = ModelTestException

        with pytest.raises(ModelTestException):
            model_util.viable_fossil_repo(
                file=tmp_path / 'repo.fossil',
                workdir=tmp_path / 'work',
                is_new=True,
                exception=ModelTestException
            )
        mock_validation_util['is_write_ok'].assert_called_once()

    def test_fail_new_repo_parent_and_workdir_are_same(self, tmp_path, mock_validation_util, mocker):
        """Tests failure when the repo's parent dir is the same as the workdir.
        """
        repo_file = tmp_path / 'repo.fossil'
        work_dir = tmp_path # workdir is parent of repo_file

        mock_validation_util['resolve_path_arg'].side_effect = [
            repo_file, work_dir
        ]

        mock_builder_class = mocker.patch(
            'quarryforge.util.model_util.model_ec.FossilRepoErrorBuilder'
        )
        mock_builder_instance = MagicMock()
        mock_builder_instance.data.return_value.to_exception.return_value = (
            {'message': 'Same dir', 'code': 'E1', 'user_message': 'Err'}
        )
        mocker.patch(
            'quarryforge.util.model_util.model_ec.FossilRepoErrorBuilder',
            return_value=mock_builder_instance
        )

        with pytest.raises(ModelTestException):
            model_util.viable_fossil_repo(
                file=repo_file,
                workdir=work_dir,
                is_new=True,
                exception=ModelTestException
            )

        mock_builder_instance.data.assert_called_once()

    @pytest.mark.parametrize(
        'failed_validation',
        ['exist', 'is_file', 'is_read_ok']
    )
    def test_fail_existing_repo_validations(
            self,
            tmp_path,
            mock_validation_util,
            failed_validation
    ):
        """Tests failures for an existing repo (non-existent, not a file,
        unreadable).
        """
        mock_validation_util[failed_validation].side_effect = ModelTestException

        with pytest.raises(ModelTestException):
             model_util.viable_fossil_repo(
                file=tmp_path / 'repo.fossil',
                workdir=tmp_path / 'work',
                is_new=False,
                exception=ModelTestException
            )
        mock_validation_util[failed_validation].assert_called()


@pytest.mark.usefixtures('mock_configs')
class TestViableFossilCommit:

    def test_pass_with_all_args(self, mock_validation_util):
        """Tests successful validation when all args are provided & valid.
        """
        args = {
            'uuid': 'u1',
            'date': 'd1',
            'author': 'a1',
            'comment': 'c1',
            'branch': 'b1',
            'tags': ['t1'],
            'phase': ['p1'],
            'changes': [('s1', 'f1')]
        }

        result = model_util.viable_fossil_commit(
            exception=ModelTestException, **args
        )

        assert result == (
            'u1', 'd1', 'a1', 'c1', 'b1', ['t1'], ['p1'], [('s1', 'f1')]
        )
        mock_validation_util['is_str_not_empty'].assert_called()
        mock_validation_util['content_empty_error_str_list'].assert_called()
        mock_validation_util[
            'content_empty_error_str_tuple_list'
        ].assert_called()

    def test_pass_with_only_required_args(self, mock_validation_util):
        """Tests successful validation when optional arguments are None."""
        args = {
            'uuid': 'u1', 'date': 'd1', 'author': 'a1', 'comment': 'c1',
            'branch': None, 'tags': None, 'phase': None, 'changes': None
        }

        result = model_util.viable_fossil_commit(
            exception=ModelTestException, **args
        )

        assert result == ('u1', 'd1', 'a1', 'c1', None, None, None, None)
        # Verify optional checks were skipped
        mock_validation_util['content_type_error_str_list'].assert_not_called()
        mock_validation_util[
            'content_type_error_str_tuple_list'
        ].assert_not_called()

    @pytest.mark.parametrize(
        'field',
        ['uuid', 'date', 'author', 'comment', 'branch']
    )
    def test_fail_string_fields_type_error(
            self,
            mock_validation_util,
            field
    ):
        """Tests failure when a string field has the wrong type."""
        args = {
            'uuid': 'u',
            'date': 'd',
            'author': 'a',
            'comment': 'c',
            'branch': 'b'
        }
        args[field] = 123 # Invalid type

        mock_validation_util['is_type_str'].side_effect = ModelTestException

        with pytest.raises(ModelTestException):
            model_util.viable_fossil_commit(
                exception=ModelTestException, **args
            )

        mock_validation_util['is_type_str'].assert_called()

    @pytest.mark.parametrize(
        'field',
        ['uuid', 'date', 'author', 'comment', 'branch']
    )
    def test_fail_string_fields_empty_error(
            self,
            mock_validation_util,
            field
    ):
        """Tests failure when a string field is empty."""
        args = {
            'uuid': 'u',
            'date': 'd',
            'author': 'a',
            'comment': 'c',
            'branch': 'b'
        }
        args[field] = '' # Invalid value

        mock_validation_util[
            'is_str_not_empty'
        ].side_effect = ModelTestException

        with pytest.raises(ModelTestException):
            model_util.viable_fossil_commit(
                exception=ModelTestException, **args
            )

        mock_validation_util['is_str_not_empty'].assert_called()

    @pytest.mark.parametrize('field', ['tags', 'phase'])
    def test_fail_list_fields_type_error(self, mock_validation_util, field):
        """Tests failure when a list field (tags/phase) contains non-strings.
        """
        args = {
            'uuid': 'u',
            'date': 'd',
            'author': 'a',
            'comment': 'c'
        }
        args[field] = ['valid', 123] # Invalid content

        mock_validation_util[
            'content_type_error_str_list'
        ].side_effect = ModelTestException

        with pytest.raises(ModelTestException):
            model_util.viable_fossil_commit(
                exception=ModelTestException, **args
            )

        mock_validation_util[
            'content_type_error_str_list'
        ].assert_called_once()

    @pytest.mark.parametrize('field', ['tags', 'phase'])
    def test_fail_list_fields_empty_error(
            self,
            mock_validation_util,
            field
    ):
        """Tests failure when a list field (tags/phase) contains empty strings.
        """
        args = {
            'uuid': 'u',
            'date': 'd',
            'author': 'a',
            'comment': 'c'
        }
        args[field] = ['valid', ' '] # Invalid content

        mock_validation_util[
            'content_empty_error_str_list'
        ].side_effect = ModelTestException

        with pytest.raises(ModelTestException):
            model_util.viable_fossil_commit(
                exception=ModelTestException, **args
            )

        mock_validation_util[
            'content_empty_error_str_list'
        ].assert_called_once()

    def test_fail_changes_field_type_error(self, mock_validation_util):
        """Tests failure when the changes list contains invalid tuple types.
        """
        args = {
            'uuid': 'u',
            'date': 'd',
            'author': 'a',
            'comment': 'c',
            'changes': [('valid', 'tuple'), 'not a tuple']
        }

        mock_validation_util[
            'content_type_error_str_tuple_list'
        ].side_effect = ModelTestException

        with pytest.raises(ModelTestException):
            model_util.viable_fossil_commit(
                exception=ModelTestException, **args
            )

        mock_validation_util['content_type_error_str_tuple_list'].assert_called_once()

    def test_fail_changes_field_empty_error(self, mock_validation_util):
        """Tests failure when a tuple in the changes list contains an empty
        string.
        """
        args = {
            'uuid': 'u',
            'date': 'd',
            'author': 'a',
            'comment': 'c',
            'changes': [('valid', 'tuple'), ('', 'empty')]
        }

        mock_validation_util[
            'content_empty_error_str_tuple_list'
        ].side_effect = ModelTestException

        with pytest.raises(ModelTestException):
            model_util.viable_fossil_commit(
                exception=ModelTestException, **args
            )

        mock_validation_util[
            'content_empty_error_str_tuple_list'
        ].assert_called_once()
