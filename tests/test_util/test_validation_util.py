"""Unit tests for the quarryforge.util.validation_util module.

This suite provides comprehensive, MC/DC-focused coverage for all validation
utility functions.
"""
import os
import pytest
from pathlib import Path
from typing import Any, Dict

from quarryforge.util import validation_util
from quarryforge.exception import base_exception
from quarryforge.meta import assembler


class UtilTestException(base_exception.UtilError):
    """Custom exception class for testing the validation_util module."""
    pass


class MockErrorData:
    """Mock of quarryforge.config.exception_conf.exception_data.ValidErrorData.
    """
    def __init__(self, code: str, message: str, user_message: str, details: Dict[str, Any]):
        self._data = {
            'code': code,
            'message': message,
            'user_message': user_message,
            'details': details,
        }

    def to_exception(self) -> Dict[str, Any]:
        """Returns the dictionary needed to instantiate a QuarryForgeError."""
        return self._data


class MockErrorBuilder(assembler.ErrorBuilder):
    """A mock implementation of the ErrorBuilder ABC for use in tests."""
    def code(self) -> str:
        """Generates a mock error code."""
        return f'{self.error_context.upper()}_{self.error_code.upper()}'

    def message(self) -> str:
        """Generates a mock technical error message."""
        return (
            f'Technical error in {self.error_context}: {self.error_code} for '
            f'arg \'{self.arg}\''
        )

    def user_message(self) -> str:
        """Generates a mock user-friendly error message."""
        return f'A problem occurred with code: {self.error_code}'

    def data(self) -> MockErrorData:
        """Constructs a MockErrorData object with the generated error info."""
        return MockErrorData(
            code=self.code(),
            message=self.message(),
            user_message=self.user_message(),
            details=self.details(),
        )


@pytest.fixture
def error_builder_factory():
    """Factory fixture to create MockErrorBuilder instances."""
    def _create_builder(
        arg: Any = None,
        context: str = 'test_context',
        code: str = 'test_code',
    ):
        return MockErrorBuilder(error_context=context, error_code=code, arg=arg)
    return _create_builder


class TestIsTypeStr:
    """Tests for validation_util.is_type_str."""

    def test_pass_with_str(self, error_builder_factory):
        """Test a valid string passes validation and is returned."""
        arg = 'hello world'
        result = validation_util.is_type_str(
            arg=arg,
            exception=UtilTestException,
            error_builder=error_builder_factory(arg=arg)
        )
        assert result == arg

    @pytest.mark.parametrize(
        'invalid_arg',
        [123, 12.3, None, True, [], {}, Path()]
    )
    def test_fail_with_non_str(self, invalid_arg, error_builder_factory):
        """Test non-string fail validation and raise the correct exception."""
        with pytest.raises(UtilTestException) as excinfo:
            validation_util.is_type_str(
                arg=invalid_arg,
                exception=UtilTestException,
                error_builder=error_builder_factory(arg=invalid_arg)
            )
        assert 'TEST_CONTEXT_TEST_CODE' in str(excinfo.value)


class TestIsStrNotEmpty:
    """Tests for validation_util.is_str_not_empty."""

    @pytest.mark.parametrize('valid_arg', ['hello', '  hello  ', ' a '])
    def test_pass_with_non_empty_str(self, valid_arg, error_builder_factory):
        """Test non-empty or whitespace-padded strings pass validation."""
        result = validation_util.is_str_not_empty(
            arg=valid_arg,
            exception=UtilTestException,
            error_builder=error_builder_factory(arg=valid_arg)
        )
        assert result == valid_arg

    @pytest.mark.parametrize('invalid_arg', ['', '   ', '\t\n'])
    def test_fail_with_empty_str(self, invalid_arg, error_builder_factory):
        """Test empty or whitespace-only strings fail validation."""
        with pytest.raises(UtilTestException):
            validation_util.is_str_not_empty(
                arg=invalid_arg,
                exception=UtilTestException,
                error_builder=error_builder_factory(arg=invalid_arg)
            )


class TestIsTypePath:
    """Tests for validation_util.is_type_path."""

    def test_pass_with_path_object(self, error_builder_factory):
        """Test a pathlib.Path object passes validation."""
        arg = Path('/tmp/test')
        result = validation_util.is_type_path(
            arg=arg,
            exception=UtilTestException,
            error_builder=error_builder_factory(arg=arg)
        )
        assert result == arg
        assert isinstance(result, Path)

    def test_pass_with_valid_string(self, error_builder_factory):
        """Test a valid string is correctly converted to a Path object."""
        arg = '/tmp/test'
        result = validation_util.is_type_path(
            arg=arg,
            exception=UtilTestException,
            error_builder=error_builder_factory(arg=arg)
        )
        assert result == Path(arg)
        assert isinstance(result, Path)

    def test_fail_with_empty_string(self, error_builder_factory):
        """Test an empty or whitespace-only string fails validation."""
        arg = '   '
        with pytest.raises(UtilTestException):
            validation_util.is_type_path(
                arg=arg,
                exception=UtilTestException,
                error_builder=error_builder_factory(arg=arg)
            )

    @pytest.mark.parametrize('invalid_arg', [123, 12.3, None, True, [], {}])
    def test_fail_with_invalid_type(self, invalid_arg, error_builder_factory):
        """Test non-str/non-Path types fail, covering the final 'else' block."""
        with pytest.raises(UtilTestException):
            validation_util.is_type_path(
                arg=invalid_arg,
                exception=UtilTestException,
                error_builder=error_builder_factory(arg=invalid_arg)
            )


class TestResolvePathArg:
    """Tests for validation_util.resolve_path_arg."""

    def test_pass_with_simple_path(self, error_builder_factory):
        """Tests successful resolution of a simple relative path."""
        arg = Path('.')
        expected = Path.cwd()
        result = validation_util.resolve_path_arg(
            arg=arg,
            exception=UtilTestException,
            error_builder=error_builder_factory(arg=arg)
        )
        assert result == expected

    def test_fail_on_runtime_error(self, monkeypatch, error_builder_factory):
        """Ensures a RuntimeError from expanduser() is caught and wrapped."""
        arg = Path('~/fail')
        def mock_expanduser(self):
            raise RuntimeError('Cannot determine home directory')

        monkeypatch.setattr(Path, 'expanduser', mock_expanduser)

        with pytest.raises(UtilTestException) as excinfo:
            validation_util.resolve_path_arg(
                arg=arg,
                exception=UtilTestException,
                error_builder=error_builder_factory(arg=arg)
            )
        assert isinstance(excinfo.value.__cause__, RuntimeError)

    def test_fail_on_os_error(self, monkeypatch, error_builder_factory):
        """Ensures an OSError from resolve() is caught and wrapped."""
        arg = Path('/nonexistent/path')
        def mock_resolve(self, strict: bool = False):
            raise OSError('Path does not exist')

        monkeypatch.setattr(Path, 'expanduser', lambda self: self)
        monkeypatch.setattr(Path, 'resolve', mock_resolve)

        with pytest.raises(UtilTestException) as excinfo:
            validation_util.resolve_path_arg(
                arg=arg,
                exception=UtilTestException,
                error_builder=error_builder_factory(arg=arg)
            )
        assert isinstance(excinfo.value.__cause__, OSError)


class TestFileSystemChecks:
    """Tests for exist, not_exist, is_file, is_dir using the tmp_path fixture."""

    def test_exist_pass(self, tmp_path, error_builder_factory):
        """Tests exist() passes for an existing file."""
        file_path = tmp_path / 'test.txt'
        file_path.touch()
        assert validation_util.exist(
            arg=file_path,
            exception=UtilTestException,
            error_builder=error_builder_factory()
        ) == file_path

    def test_exist_fail(self, tmp_path, error_builder_factory):
        """Tests exist() fails for a non-existent file."""
        with pytest.raises(UtilTestException):
            validation_util.exist(
                arg=tmp_path / 'ghost.txt',
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )

    def test_not_exist_pass(self, tmp_path, error_builder_factory):
        """Tests not_exist() passes for a non-existent file."""
        path = tmp_path / 'ghost.txt'
        assert validation_util.not_exist(
            arg=path,
            exception=UtilTestException,
            error_builder=error_builder_factory()
        ) == path

    def test_not_exist_fail(self, tmp_path, error_builder_factory):
        """Tests not_exist() fails for an existing file."""
        file_path = tmp_path / 'test.txt'
        file_path.touch()
        with pytest.raises(UtilTestException):
            validation_util.not_exist(
                arg=file_path,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )

    def test_is_file_pass(self, tmp_path, error_builder_factory):
        """Tests is_file() passes for a file."""
        file_path = tmp_path / 'test.txt'
        file_path.touch()
        assert validation_util.is_file(
            arg=file_path,
            exception=UtilTestException,
            error_builder=error_builder_factory()
        ) == file_path

    def test_is_file_fail(self, tmp_path, error_builder_factory):
        """Tests is_file() fails for a directory."""
        dir_path = tmp_path / 'test_dir'
        dir_path.mkdir()
        with pytest.raises(UtilTestException):
            validation_util.is_file(
                arg=dir_path,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )

    def test_is_dir_pass(self, tmp_path, error_builder_factory):
        """Tests is_dir() passes for a directory."""
        dir_path = tmp_path / 'test_dir'
        dir_path.mkdir()
        assert validation_util.is_dir(
            arg=dir_path,
            exception=UtilTestException,
            error_builder=error_builder_factory()
        ) == dir_path

    def test_is_dir_fail(self, tmp_path, error_builder_factory):
        """Tests is_dir() fails for a file."""
        file_path = tmp_path / 'test.txt'
        file_path.touch()
        with pytest.raises(UtilTestException):
            validation_util.is_dir(
                arg=file_path,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )


class TestPermissionChecks:
    """Tests for is_read_ok and is_write_ok using monkeypatching."""

    def test_is_read_ok_pass(
            self,
            tmp_path,
            monkeypatch,
            error_builder_factory
    ):
        """Tests is_read_ok() passes when os.access returns True."""
        path = tmp_path / 'readable.txt'
        monkeypatch.setattr(os, 'access', lambda p, m: True)
        assert validation_util.is_read_ok(
            arg=path,
            exception=UtilTestException,
            error_builder=error_builder_factory()
        ) == path

    def test_is_read_ok_fail(
            self,
            tmp_path,
            monkeypatch,
            error_builder_factory
    ):
        """Tests is_read_ok() fails when os.access returns False for R_OK."""
        path = tmp_path / 'unreadable.txt'
        monkeypatch.setattr(os, 'access', lambda p, mode: mode != os.R_OK)
        with pytest.raises(UtilTestException):
            validation_util.is_read_ok(
                arg=path,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )

    def test_is_write_ok_pass(
            self,
            tmp_path,
            monkeypatch,
            error_builder_factory
    ):
        """Tests is_write_ok() passes when os.access returns True."""
        path = tmp_path / 'writable.txt'
        monkeypatch.setattr(os, 'access', lambda p, m: True)
        assert validation_util.is_write_ok(
            arg=path,
            exception=UtilTestException,
            error_builder=error_builder_factory()
        ) == path

    def test_is_write_ok_fail(
            self,
            tmp_path,
            monkeypatch,
            error_builder_factory
    ):
        """Tests is_write_ok() fails when os.access returns False for W_OK."""
        path = tmp_path / 'unwritable.txt'
        monkeypatch.setattr(os, 'access', lambda p, mode: mode != os.W_OK)
        with pytest.raises(UtilTestException):
            validation_util.is_write_ok(
                arg=path,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )


class TestContentTypeErrorStrList:
    """Tests for validation_util.content_type_error_str_list."""

    @pytest.mark.parametrize('valid_list', [None, [], ['a', 'b', 'c'], ['']])
    def test_pass_with_valid_list(self, valid_list, error_builder_factory):
        """Ensures valid lists (including None and empty) pass."""
        expected = [] if valid_list is None else valid_list
        result = validation_util.content_type_error_str_list(
            arg=valid_list,
            exception=UtilTestException,
            error_builder=error_builder_factory()
        )
        assert result == expected

    @pytest.mark.parametrize(
        'invalid_list',
        [['a', 1, 'c'], [None, 'b'], [('tuple',)]]
    )
    def test_fail_with_mixed_types(self, invalid_list, error_builder_factory):
        """Ensures lists with non-string elements fail."""
        with pytest.raises(UtilTestException):
            validation_util.content_type_error_str_list(
                arg=invalid_list,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )


class TestContentEmptyErrorStrList:
    """Tests for validation_util.content_empty_error_str_list."""

    @pytest.mark.parametrize('valid_list', [None, [], ['a', 'b', ' c ']])
    def test_pass_with_valid_list(self, valid_list, error_builder_factory):
        """Ensures lists with non-empty strings pass."""
        expected = [] if valid_list is None else valid_list
        result = validation_util.content_empty_error_str_list(
            arg=valid_list,
            exception=UtilTestException,
            error_builder=error_builder_factory()
        )
        assert result == expected

    @pytest.mark.parametrize('invalid_list', [['a', '', 'c'], ['a', '   ', 'c']])
    def test_fail_with_empty_strings(self, invalid_list, error_builder_factory):
        """Ensures lists with empty or whitespace-only strings fail."""
        with pytest.raises(UtilTestException):
            validation_util.content_empty_error_str_list(
                arg=invalid_list,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )


class TestContentTypeErrorStrTupleList:
    """Tests for validation_util.content_type_error_str_tuple_list."""

    @pytest.mark.parametrize(
        'valid_list',
        [None, [], [('a', 'b'), ('c', 'd')], [('', '')]]
    )
    def test_pass_with_valid_list(self, valid_list, error_builder_factory):
        """Ensures valid lists of (str, str) tuples pass."""
        expected = [] if valid_list is None else valid_list
        result = validation_util.content_type_error_str_tuple_list(
            arg=valid_list,
            exception=UtilTestException,
            error_builder=error_builder_factory()
            )
        assert result == expected

    @pytest.mark.parametrize('invalid_list, desc', [
        ([('a', 'b'), ['c', 'd']], 'item is not a tuple'),
        ([('a', 'b'), ('c',)], 'tuple length is not 2'),
        ([('a', 'b'), ('c', 'd', 'e')], 'tuple length is not 2'),
        ([('a', 'b'), (1, 'd')], 'first element is not a string'),
        ([('a', 'b'), ('c', 2)], 'second element is not a string'),
    ])
    def test_fail_with_invalid_items_for_mcdc(self, invalid_list, desc, error_builder_factory):
        """Tests failure modes for MC/DC of the item validation condition."""
        with pytest.raises(UtilTestException):
             validation_util.content_type_error_str_tuple_list(
                 arg=invalid_list,
                 exception=UtilTestException,
                 error_builder=error_builder_factory()
             )


class TestContentEmptyErrorStrTupleList:
    """Tests for validation_util.content_empty_error_str_tuple_list."""

    @pytest.mark.parametrize('valid_list', [[], [('a', 'b'), (' c ', 'd')]])
    def test_pass_with_valid_list(self, valid_list, error_builder_factory):
        """Ensures lists with non-empty string tuples pass."""
        result = validation_util.content_empty_error_str_tuple_list(
            arg=valid_list,
            exception=UtilTestException,
            error_builder=error_builder_factory()
        )
        assert result == valid_list

    @pytest.mark.parametrize('invalid_list, desc', [
        ([('a', 'b'), ('', 'd')], 'first element is empty'),
        ([('a', 'b'), ('c', '   ')], 'second element is whitespace'),
        ([('a', 1)], 'element is not a string, causing failure'),
    ])
    def test_fail_with_invalid_content_for_mcdc(self, invalid_list, desc, error_builder_factory):
        """Tests failure modes for MC/DC of the tuple element validation."""
        with pytest.raises(UtilTestException):
            validation_util.content_empty_error_str_tuple_list(
                arg=invalid_list,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )
