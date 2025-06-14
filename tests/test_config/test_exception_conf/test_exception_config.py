"""Exception Config Module Test Suite"""
import pytest
from enum import StrEnum
from quarryforge.config.exception_conf import exception_config as ec


class TestExceptionConfig:
    """Tests for quarryforge.config.exception_conf.exception_config"""

    def test_module_dunder_all(self):
        """Test the __all__ variable."""
        expected_all = ['GenericError', 'StringError', 'PathError', 'DescMsg']
        assert sorted(ec.__all__) == sorted(expected_all)

    def test_generic_error_type_attributes(self):
        """Verify members and values of the GenericError StrEnum."""
        assert issubclass(ec.GenericError, ec.ValidName)
        assert ec.GenericError.TYPE_ERROR == 'TYPE_ERROR'

        assert ec.GenericError.VALUE_ERROR == 'VALUE_ERROR'
        assert ec.GenericError.UNEXPECTED_ERROR == 'UNEXPECTED_ERROR'
        assert ec.GenericError.INVALID_STATE_ERROR == 'INVALID_STATE_ERROR'
        assert ec.GenericError.CONFIGURATION_ERROR == 'CONFIGURATION_ERROR'
        assert ec.GenericError.EXTERNAL_DEPENDENCY_ERROR == 'EXTERNAL_DEPENDENCY_ERROR'
        assert ec.GenericError.NOT_IMPLEMENTED_ERROR == 'NOT_IMPLEMENTED_ERROR'
        assert len(list(ec.GenericError)) == 7

    def test_string_error_type_attributes(self):
        """Verify members and values of the StringError StrEnum."""
        assert issubclass(ec.StringError, ec.ValidName)
        assert ec.StringError.EMPTY_STRING_ERROR == 'EMPTY_STRING_ERROR'
        assert ec.StringError.INVALID_CHARS_ERROR == 'INVALID_CHARS_ERROR'

    def test_path_error_type_attributes(self):
        """Verify members and values of the PathError StrEnum."""
        assert issubclass(ec.PathError, ec.ValidName)
        assert ec.PathError.NON_PATH_OBJECT_ERROR == 'NON_PATH_OBJECT_ERROR'
        assert ec.PathError.INVALID_PATH_STRING_ERROR == 'INVALID_PATH_STRING_ERROR'
        assert ec.PathError.PATH_RESOLUTION_ERROR == 'PATH_RESOLUTION_ERROR'
        assert ec.PathError.PATH_EXISTING_ERROR == 'PATH_EXISTING_ERROR'
        assert ec.PathError.PATH_NONEXISTENT_ERROR == 'PATH_NONEXISTENT_ERROR'
        assert ec.PathError.PATH_NOT_A_FILE_ERROR == 'PATH_NOT_A_FILE_ERROR'
        assert ec.PathError.PATH_NOT_A_DIRECTORY_ERROR == 'PATH_NOT_A_DIRECTORY_ERROR'
        assert ec.PathError.PATH_NOT_READABLE_ERROR == 'PATH_NOT_READABLE_ERROR'
        assert ec.PathError.PATH_NOT_WRITABLE_ERROR == 'PATH_NOT_WRITABLE_ERROR'
        assert ec.PathError.PATH_NOT_EXECUTABLE_ERROR == 'PATH_NOT_EXECUTABLE_ERROR'
        assert ec.PathError.SAME_REPO_DIR_AND_WORK_DIR == 'SAME_REPO_DIR_AND_WORK_DIR'
        assert len(list(ec.PathError)) == 11

    def test_desc_msg_attributes(self):
        """Verify members and manually assigned values of the DescMsg StrEnum."""
        assert issubclass(ec.DescMsg, StrEnum)
        assert not issubclass(ec.DescMsg, ec.ValidName)
        assert ec.DescMsg.DEPENDENCY == 'dependency'
        assert ec.DescMsg.A_VALID_DICTIONARY == 'a valid dictionary'
        assert ec.DescMsg.MUST_BE == 'must be'
        assert ec.DescMsg.NONE == 'None'
        assert ec.DescMsg.A_VALID_PATH == 'a valid path'
        assert ec.DescMsg.REASON == 'reason'
        assert ec.DescMsg.A_VALID_STRING == 'a valid string'
        assert ec.DescMsg.A_NON_EMPTY_STRING == 'a non-empty string'
        assert ec.DescMsg.IS_AN_UNEXPECTED_ERROR == 'is an unexpected error'
        assert ec.DescMsg.UNKNOWN == 'unknown'
