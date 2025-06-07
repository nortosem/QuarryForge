import pytest
from typing import NamedTuple

from quarryforge.config.exception_conf import exception_config

from tests.test_config.test_root import get_namedtuple_fields


class TestExceptionConfig:
    """Tests for quarryforge.config.exception_conf.exception_config"""

    def test_module_dunder_all(self):
        """Test the __all__ variable."""
        expected_all = [
            'GENERIC_ERROR', 'STRING_ERROR', 'PATH_ERROR', 'DESC_MSG'
        ]
        assert sorted(exception_config.__all__) == sorted(expected_all)

    def test_generic_error_type_attributes(self):
        """Test attributes of GenericErrorType."""
        cfg = exception_config.GENERIC_ERROR
        assert isinstance(cfg, exception_config.GenericErrorType)
        assert cfg.type_error == 'TYPE_ERROR'
        assert cfg.value_error == 'VALUE_ERROR'
        assert cfg.unexpected_error == 'UNEXPECTED_ERROR'
        assert cfg.invalid_state == 'INVALID_STATE_ERROR'
        assert cfg.configuration_error == 'CONFIGURATION_ERROR'
        assert cfg.external_dependency_error == 'EXTERNAL_DEPENDENCY_ERROR'
        assert cfg.not_implemented_error == 'NOT_IMPLEMENTED_ERROR'

        expected_fields = (
            'type_error', 'value_error', 'unexpected_error',
            'invalid_state', 'configuration_error',
            'external_dependency_error', 'not_implemented_error'
        )
        assert get_namedtuple_fields(
            exception_config.GenericErrorType) == expected_fields

    def test_string_error_type_attributes(self):
        """Test attributes of StringErrorType."""
        cfg = exception_config.STRING_ERROR
        assert isinstance(cfg, exception_config.StringErrorType)
        assert cfg.empty == 'EMPTY_STRING_ERROR'
        assert cfg.invalid_chars == 'INVALID_CHARS_ERROR'

        expected_fields = ('empty', 'invalid_chars')
        assert get_namedtuple_fields(
            exception_config.StringErrorType) == expected_fields

    def test_path_error_type_attributes(self):
        """Test attributes of PathErrorType."""
        cfg = exception_config.PATH_ERROR
        assert isinstance(cfg, exception_config.PathErrorType)
        assert cfg.non_path_object == 'NON_PATH_OBJECT_ERROR'
        assert cfg.invalid_path_string == 'INVALID_PATH_STRING_ERROR'
        assert cfg.resolution == 'PATH_RESOLUTION_ERROR'
        assert cfg.existing == 'PATH_EXISTING_ERROR'
        assert cfg.nonexistent == 'PATH_NONEXISTENT_ERROR'
        assert cfg.file_error == 'PATH_NOT_A_FILE_ERROR'
        assert cfg.dir_error == 'PATH_NOT_A_DIRECTORY_ERROR'
        assert cfg.unreadable == 'PATH_NOT_READABLE_ERROR'
        assert cfg.unwritable == 'PATH_NOT_WRITABLE_ERROR'
        assert cfg.unexecutable == 'PATH_NOT_EXECUTABLE_ERROR'
        assert cfg.same_dir == 'SAME_REPO_DIR_AND_WORK_DIR'

        expected_fields = (
            'non_path_object', 'invalid_path_string', 'resolution', 'existing',
            'nonexistent', 'file_error', 'dir_error', 'unreadable',
            'unwritable', 'unexecutable', 'same_dir'
        )
        assert get_namedtuple_fields(exception_config.PathErrorType) == expected_fields

    def test_desc_msg_attributes(self):
        """Test attributes of DescMsg."""
        cfg = exception_config.DESC_MSG
        assert isinstance(cfg, exception_config.DescMsg)
        assert cfg.dependency == 'dependency'
        assert cfg.dictionary == 'a valid dictionary'
        assert cfg.must_be == 'must be'
        assert cfg.none == 'None'
        assert cfg.path == 'a valid path'
        assert cfg.reason == 'reason'
        assert cfg.string == 'a valid string'
        assert cfg.unempty == 'a non-empty string'
        assert cfg.unexpected_error == 'is an unexpected error'
        assert cfg.unknown == 'unknown'

        expected_fields = (
            'dependency', 'dictionary', 'must_be', 'none', 'path', 'reason',
            'string', 'unempty', 'unexpected_error', 'unknown'
        )
        assert get_namedtuple_fields(
            exception_config.DescMsg) == expected_fields


    def test_global_constants_types(self):
        """Test types of global constants."""
        assert isinstance(
            exception_config.GENERIC_ERROR, exception_config.GenericErrorType)
        assert isinstance(
            exception_config.STRING_ERROR, exception_config.StringErrorType)
        assert isinstance(
            exception_config.PATH_ERROR, exception_config.PathErrorType)
        assert isinstance(
            exception_config.DESC_MSG, exception_config.DescMsg)
