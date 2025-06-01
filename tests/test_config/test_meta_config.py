import pytest
from typing import NamedTuple

from quarryforge.config import meta_config
from quarryforge.config.exception_conf import exception_data


def get_namedtuple_fields(nt_class):
    """Get all fields from a NamedTuple class"""
    return nt_class._fields

class TestMetaConfig:
    """Tests for quarryforge.config.meta_config"""

    def test_module_dunder_all(self):
        """Test the __all__ variable."""
        assert hasattr(meta_config, '__all__')
        assert meta_config.__all__ == []

    def test_error_builder_config_attributes(self):
        """Test attributes of ErrorBuilderConfig."""
        cfg = meta_config.BUILDER_CONFIG
        assert isinstance(cfg, meta_config.ErrorBuilderConfig)

        assert cfg.error_context == exception_data.BUILDER_FIELD.error_context
        assert cfg.error_code == exception_data.BUILDER_FIELD.error_code
        assert cfg.arg == exception_data.BUILDER_FIELD.arg
        assert cfg.extra_details == exception_data.BUILDER_FIELD.extra_details
        assert cfg.info == exception_data.BUILDER_FIELD.info
        assert cfg.field == exception_data.BUILDER_FIELD.field
        assert cfg.message == exception_data.BUILDER_FIELD.message
        assert cfg.user_message == exception_data.BUILDER_FIELD.user_message

        assert cfg.error_context == 'error_context'
        assert cfg.error_code == 'error_code'
        assert cfg.arg == 'arg'
        assert cfg.extra_details == 'extra_details'
        assert cfg.info == 'info'
        assert cfg.field == 'field'
        assert cfg.message == 'message'
        assert cfg.user_message == 'user_message'

        expected_fields = [
            'error_context', 'error_code', 'arg', 'extra_details',
            'info', 'field', 'message', 'user_message'
        ]
        assert sorted(
            get_namedtuple_fields(
                meta_config.ErrorBuilderConfig)) == sorted(expected_fields)

    def test_global_builder_config_instance(self):
        """Test the global BUILDER_CONFIG instance."""
        assert isinstance(
            meta_config.BUILDER_CONFIG, meta_config.ErrorBuilderConfig)
