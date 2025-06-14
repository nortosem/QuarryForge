"""config.exeption_conf.exception_data test suite"""
import pytest
from quarryforge.config.exception_conf import exception_data as ed
from quarryforge.meta import immutable as _


class TestExceptionData:
    """Tests for the refactored exception_data module."""

    def test_module_dunder_all(self):
        """Test the __all__ variable."""
        expected_all = ['error_data_config', 'builder_config', 'ValidErrorData']
        assert sorted(ed.__all__) == sorted(expected_all)

    def test_error_data_config_factory(self):
        """Test the error_data_config factory and its returned object."""
        cfg = ed.error_data_config()
        assert isinstance(cfg, ed.ConfigErrorData)
        assert cfg.code == 'code'
        assert cfg.details == 'details'
        assert cfg.message == 'message'
        assert cfg.user_message == 'user_message'
        assert cfg.timestamp == 'timestamp'

    def test_builder_config_factory(self):
        """Test the builder_config factory and its returned object."""
        cfg = ed.builder_config()
        assert isinstance(cfg, ed.ConfigBuilder)
        assert cfg.arg == 'arg'
        assert cfg.error_code == 'error_code'
        assert cfg.error_context == 'error_context'
        assert cfg.extra_details == 'extra_details'
        assert cfg.info == 'info'
        assert cfg.field == 'field'
        assert cfg.message == 'message'
        assert cfg.user_message == 'user_message'

    def test_valid_error_data_instantiation_and_slots(self):
        """Test ValidErrorData instantiation and __slots__."""
        data = ed.ValidErrorData(
            code="ERR001",
            message="Test message",
            user_message="User test message",
            details={"key": "value"}
        )
        assert data.code == "ERR001"
        assert data.message == "Test message"
        assert data.user_message == "User test message"
        assert data.details == {"key": "value"}
        cfg = ed.error_data_config()
        expected_slots = cfg._fields[:-1]
        assert ed.ValidErrorData.__slots__ == expected_slots

        default_data = ed.ValidErrorData()
        assert default_data.code is None
        assert default_data.message is None
        assert default_data.user_message is None
        assert default_data.details is None


    def test_valid_error_data_immutability(self):
        """Test immutability of ValidErrorData."""
        data = ed.ValidErrorData(code="ERR001")

        with pytest.raises(TypeError, match='Immutable'):
            data.code = "NEW_CODE"

        with pytest.raises(TypeError, match='Immutable'):
            setattr(data, 'new_attr', "test")

        assert issubclass(ed.ValidErrorData, _.ImmutableInstance)


    def test_valid_error_data_to_exception(self):
        """Test to_exception method of ValidErrorData."""
        details_dict = {"key": "value", "num": 123}
        data = ed.ValidErrorData(
            code="ERR002",
            message="Another message",
            user_message="Another user message",
            details=details_dict
        )
        expected_dict = {
            'code': 'ERR002',
            'message': 'Another message',
            'user_message': 'Another user message',
            'details': details_dict
        }
        assert data.to_exception() == expected_dict

        data_none = ed.ValidErrorData()
        expected_dict_none = {
            'code': None,
            'message': None,
            'user_message': None,
            'details': None
        }
        assert data_none.to_exception() == expected_dict_none
