import pytest
from typing import Any, Dict, Optional

from quarryforge.config.exception_conf import exception_data
from quarryforge.meta import immutable as _ # For checking immutable base

from tests.test_config.test_root import get_namedtuple_fields


class TestExceptionData:
    """Tests for quarryforge.config.exception_conf.exception_data"""

    def test_module_dunder_all(self):
        """Test the __all__ variable."""
        expected_all = ['ERROR_FIELD', 'BUILDER_FIELD', 'ValidErrorData']
        assert sorted(exception_data.__all__) == sorted(expected_all)

    def test_config_error_data_attributes(self):
        """Test attributes of ConfigErrorData."""
        cfg = exception_data.ERROR_FIELD
        assert isinstance(cfg, exception_data.ConfigErrorData)
        assert cfg.code == 'code'
        assert cfg.details == 'details'
        assert cfg.message == 'message'
        assert cfg.user_message == 'user_message'
        assert cfg.timestamp == 'timestamp'

        expected_fields = ('code', 'details', 'message', 'user_message', 'timestamp')
        assert get_namedtuple_fields(
            exception_data.ConfigErrorData) == expected_fields

    def test_config_builder_attributes(self):
        """Test attributes of ConfigBuilder."""
        cfg = exception_data.BUILDER_FIELD
        assert isinstance(cfg, exception_data.ConfigBuilder)
        assert cfg.arg == 'arg'
        assert cfg.error_code == 'error_code'
        assert cfg.error_context == 'error_context'
        assert cfg.extra_details == 'extra_details'
        assert cfg.info == 'info'
        assert cfg.field == 'field'
        assert cfg.message == exception_data.ERROR_FIELD.message
        assert cfg.user_message == exception_data.ERROR_FIELD.user_message

        expected_fields = (
            'arg', 'error_code', 'error_context', 'extra_details',
            'info', 'field', 'message', 'user_message'
        )
        assert get_namedtuple_fields(exception_data.ConfigBuilder) == expected_fields


    def test_valid_error_data_instantiation_and_slots(self):
        """Test ValidErrorData instantiation and __slots__."""
        data = exception_data.ValidErrorData(
            code="ERR001",
            message="Test message",
            user_message="User test message",
            details={"key": "value"}
        )
        assert data.code == "ERR001"
        assert data.message == "Test message"
        assert data.user_message == "User test message"
        assert data.details == {"key": "value"}

        expected_slots = exception_data.ERROR_FIELD._fields[:-1]
        assert exception_data.ValidErrorData.__slots__ == expected_slots

        default_data = exception_data.ValidErrorData()
        assert default_data.code is None
        assert default_data.message is None
        assert default_data.user_message is None
        assert default_data.details is None


    def test_valid_error_data_immutability(self):
        """Test immutability of ValidErrorData."""
        data = exception_data.ValidErrorData(code="ERR001")

        with pytest.raises(TypeError, match='Immutable'):
            data.code = "NEW_CODE"

        with pytest.raises(TypeError, match='Immutable'):
            setattr(data, 'new_attr', "test")

        assert issubclass(exception_data.ValidErrorData, _.ImmutableInstance)


    def test_valid_error_data_to_exception(self):
        """Test to_exception method of ValidErrorData."""
        details_dict = {"key": "value", "num": 123}
        data = exception_data.ValidErrorData(
            code="ERR002",
            message="Another message",
            user_message="Another user message",
            details=details_dict
        )
        expected_dict = {
            exception_data.ERROR_FIELD.code: "ERR002",
            exception_data.ERROR_FIELD.message: "Another message",
            exception_data.ERROR_FIELD.user_message: "Another user message",
            exception_data.ERROR_FIELD.details: details_dict
        }
        assert data.to_exception() == expected_dict

        data_none = exception_data.ValidErrorData()
        expected_dict_none = {
            exception_data.ERROR_FIELD.code: None,
            exception_data.ERROR_FIELD.message: None,
            exception_data.ERROR_FIELD.user_message: None,
            exception_data.ERROR_FIELD.details: None
        }
        assert data_none.to_exception() == expected_dict_none
