"""Unit tests for the quarryforge.util.validation_util module.

This suite provides comprehensive, MC/DC-focused coverage for all validation
utility functions using a hybrid of unit, functional, and mocked tests.
"""

import logging
import os
from pathlib import Path
from typing import Any

import pytest

from quarryforge.exception import base_exception
from quarryforge.meta import assembler
from quarryforge.util import validation_util


class UtilTestException(base_exception.UtilError):
    """Custom exception class for testing the validation_util module."""
    def __init__(self, code, message, user_message, details=None):
        super().__init__(
            code=code, message=message,
            user_message=user_message, details=details or {}
        )


class MockErrorData:
    """Mock of ValidErrorData for testing."""
    def __init__(self, code, message, user_message, details):
        self._data = {
            'code': code, 'message': message,
            'user_message': user_message, 'details': details
        }
    def to_exception(self) -> dict[str, Any]:
        return self._data


class MockErrorBuilder(assembler.ErrorBuilder):
    """Mock implementation of the ErrorBuilder ABC for use in tests."""
    def code(self) -> str:
        return f'{self.error_context.upper()}_{self.error_code.upper()}'
    def message(self) -> str: return f'Technical error for arg {self.arg!r}'
    def user_message(self) -> str: return 'A problem occurred.'
    def data(self) -> MockErrorData:
        return MockErrorData(self.code(), self.message(), self.user_message(), self.details())


@pytest.fixture
def error_builder_factory():
    """Factory fixture to create MockErrorBuilder instances."""
    def _create_builder(
            arg: Any = None,
            context: str = 'test_ctx',
            code: str = 'test_code'
    ):
        return MockErrorBuilder(
            error_context=context, error_code=code, arg=arg
        )
    return _create_builder


class TestStringValidators:
    """Tests for is_type_str and is_str_not_empty."""

    def test_is_type_str_pass(self, error_builder_factory):
        logging.info('Testing is_type_str: success path.')
        assert validation_util.is_type_str(
            arg='valid',
            exception=UtilTestException,
            error_builder=error_builder_factory()) == 'valid'

    @pytest.mark.parametrize('invalid_arg', [123, None, []])
    def test_is_type_str_fail(self, invalid_arg, error_builder_factory):
        logging.info(
            'Testing is_type_str: failure on type %s.',
            type(invalid_arg).__name__
        )
        with pytest.raises(UtilTestException):
            validation_util.is_type_str(
                arg=invalid_arg,
                exception=UtilTestException,
                error_builder=error_builder_factory(arg=invalid_arg)
            )

    def test_is_str_not_empty_pass(self, error_builder_factory):
        logging.info('Testing is_str_not_empty: success path.')
        assert validation_util.is_str_not_empty(
            arg='valid',
            exception=UtilTestException,
            error_builder=error_builder_factory()) == 'valid'

    @pytest.mark.parametrize('invalid_arg', ['', '   ', '\t\n'])
    def test_is_str_not_empty_fail(self, invalid_arg, error_builder_factory):
        logging.info(
            'Testing is_str_not_empty: failure on empty or whitespace string.'
        )
        with pytest.raises(UtilTestException):
            validation_util.is_str_not_empty(
                arg=invalid_arg,
                exception=UtilTestException,
                error_builder=error_builder_factory(arg=invalid_arg)
            )


class TestPathValidators:
    """Tests for path-related validation functions."""

    def test_is_type_path_success(self, error_builder_factory):
        """Test is_type_path correctly handles valid Path and str types."""
        logging.info('Testing is_type_path: success with Path object.')
        path_obj = Path('/tmp/test')
        assert validation_util.is_type_path(
            arg=path_obj,
            exception=UtilTestException,
            error_builder=error_builder_factory()) is path_obj

        logging.info('Testing is_type_path: success with string.')
        path_str = '/tmp/test'
        assert validation_util.is_type_path(
            arg=path_str,
            exception=UtilTestException,
            error_builder=error_builder_factory()) == Path(path_str)

    @pytest.mark.parametrize('invalid_arg', [123, None, [], {}])
    def test_is_type_path_fail_on_invalid_type(self, invalid_arg, error_builder_factory):
        """Test is_type_path raises the correct exception for invalid types."""
        logging.info(
            'Testing is_type_path: failure on invalid type %s.',
             type(invalid_arg).__name__
        )
        with pytest.raises(UtilTestException) as excinfo:
            validation_util.is_type_path(
                arg=invalid_arg,
                exception=UtilTestException,
                error_builder=error_builder_factory(arg=invalid_arg),
            )
        assert f"for arg {invalid_arg!r}" in str(excinfo.value)

    def test_resolve_path_arg_fail_on_runtime_error(
            self, monkeypatch, error_builder_factory):
        """Ensures a RuntimeError from expanduser() is caught and wrapped."""
        logging.info('Testing resolve_path_arg: RuntimeError case.')
        arg = Path('~/fail')
        def mock_expanduser_runtime_error(self):
            raise RuntimeError('Cannot determine home directory')
        monkeypatch.setattr(Path, 'expanduser', mock_expanduser_runtime_error)
        with pytest.raises(UtilTestException) as excinfo:
            validation_util.resolve_path_arg(
                arg=arg,
                exception=UtilTestException,
                error_builder=error_builder_factory(arg=arg),
            )
        assert isinstance(excinfo.value.__cause__, RuntimeError)

    def test_resolve_path_arg_fail_on_os_error(
            self, monkeypatch, error_builder_factory):
        """Ensures an OSError from resolve() is caught and wrapped."""
        logging.info('Testing resolve_path_arg: OSError case.')
        arg = Path('/nonexistent/path')
        def mock_resolve_os_error(self, strict: bool = False):
            raise OSError('test os error')
        monkeypatch.setattr(Path, 'expanduser', lambda self: self)
        monkeypatch.setattr(Path, 'resolve', mock_resolve_os_error)
        with pytest.raises(UtilTestException) as excinfo:
            validation_util.resolve_path_arg(
                arg=arg,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )
        assert isinstance(excinfo.value.__cause__, OSError)

    def test_file_system_checks(self, tmp_path: Path, error_builder_factory):
        """Functional tests for exist, not_exist, is_file, is_dir."""
        logging.info('Testing filesystem validators with tmp_path.')
        existing_file = tmp_path / 'file.txt'
        existing_dir = tmp_path / 'dir'
        non_existent = tmp_path / 'ghost'
        existing_file.touch()
        existing_dir.mkdir()

        # Test exist and not_exist
        assert validation_util.exist(
            arg=existing_file,
            exception=UtilTestException,
            error_builder=error_builder_factory()
        )
        with pytest.raises(UtilTestException):
            validation_util.exist(
                arg=non_existent,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )
        assert validation_util.not_exist(
            arg=non_existent,
            exception=UtilTestException,
            error_builder=error_builder_factory()
        )
        with pytest.raises(UtilTestException):
            validation_util.not_exist(
                arg=existing_file,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )

        # Test is_file and is_dir
        assert validation_util.is_file(
            arg=existing_file,
            exception=UtilTestException,
            error_builder=error_builder_factory()
        )
        with pytest.raises(UtilTestException):
            validation_util.is_file(
                arg=existing_dir,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )
        assert validation_util.is_dir(
            arg=existing_dir,
            exception=UtilTestException,
            error_builder=error_builder_factory()
        )
        with pytest.raises(UtilTestException):
            validation_util.is_dir(
                arg=existing_file,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )

    def test_permission_checks(self, tmp_path: Path, monkeypatch, error_builder_factory):
        """Unit tests for permission checks using monkeypatch."""
        logging.info('Testing permission validators with monkeypatch.')
        path = tmp_path / 'test.file'

        monkeypatch.setattr(os, 'access', lambda p, m: False)
        with pytest.raises(UtilTestException):
            validation_util.is_read_ok(
                arg=path,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )
        with pytest.raises(UtilTestException):
            validation_util.is_write_ok(
                arg=path,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )

        monkeypatch.setattr(os, 'access', lambda p, m: True)
        assert validation_util.is_read_ok(
            arg=path,
            exception=UtilTestException,
            error_builder=error_builder_factory()
        )
        assert validation_util.is_write_ok(
            arg=path,
            exception=UtilTestException,
            error_builder=error_builder_factory()
        )


class TestListValidators:
    """Tests for list content validation functions."""

    @pytest.mark.parametrize('valid_list', [None, [], ['a', 'b'], ['']])
    def test_content_type_error_str_list_pass(
            self, valid_list, error_builder_factory):
        logging.info('Testing content_type_error_str_list: success path.')
        expected = [] if valid_list is None else valid_list
        assert validation_util.content_type_error_str_list(
            arg=valid_list,
            exception=UtilTestException,
            error_builder=error_builder_factory()) == expected

    def test_content_type_error_str_list_fail(self, error_builder_factory):
        logging.info('Testing content_type_error_str_list: failure path.')
        with pytest.raises(UtilTestException):
            validation_util.content_type_error_str_list(
                arg=['a', 1],
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )

    @pytest.mark.parametrize('valid_list', [None, [], [('a', 'b')]])
    def test_content_type_error_str_tuple_list_pass(
            self, valid_list, error_builder_factory):
        logging.info(
            'Testing content_type_error_str_tuple_list: success path.'
        )
        expected = [] if valid_list is None else valid_list
        assert validation_util.content_type_error_str_tuple_list(
            arg=valid_list,
            exception=UtilTestException,
            error_builder=error_builder_factory()) == expected

    @pytest.mark.parametrize(
        'invalid_list',
        [[('a', 1)], [('a', 'b', 'c')], [('a')]]
    )
    def test_content_type_error_str_tuple_list_fail(
            self, invalid_list, error_builder_factory):
        logging.info('Testing content_type_error_str_tuple_list: failure path.')
        with pytest.raises(UtilTestException):
            validation_util.content_type_error_str_tuple_list(
                arg=invalid_list,
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )

    def test_content_empty_error_str_tuple_list_fail(
            self, error_builder_factory):
        logging.info(
            'Testing content_empty_error_str_tuple_list: failure path.'
        )
        with pytest.raises(UtilTestException):
            validation_util.content_empty_error_str_tuple_list(
                arg=[('a', '')],
                exception=UtilTestException,
                error_builder=error_builder_factory()
            )
