import pytest
from typing import NamedTuple

from quarryforge.config import meta_config
from quarryforge.config.exception_conf import exception_data

from tests.test_config.test_root import get_namedtuple_fields


class TestMetaConfig:
    """Tests for quarryforge.config.meta_config"""

    def test_module_dunder_all(self):
        """Test the __all__ variable."""
        assert hasattr(meta_config, '__all__')
        assert meta_config.__all__ == []

    def test_attr_mod_type_config_attributes(self):
        """Test attributes of AttrModTypeConfig."""
        cfg = meta_config.MOD_TYPE
        assert isinstance(cfg, meta_config.AttrModTypeConfig)

        assert cfg.set_attribute == 'set attribute'
        assert cfg.delete_attribute == 'delete attribute'

        expected_fields = ['set_attribute', 'delete_attribute']
        assert sorted(get_namedtuple_fields(meta_config.AttrModTypeConfig)) == sorted(expected_fields)

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

        assert cfg.error_context == 'error_context'
        assert cfg.error_code == 'error_code'
        assert cfg.arg == 'arg'
        assert cfg.extra_details == 'extra_details'
        assert cfg.info == 'info'
        assert cfg.field == 'field'

        expected_fields = [
            'error_context', 'error_code', 'arg', 'extra_details',
            'info', 'field'
        ]
        assert sorted(
            get_namedtuple_fields(
                meta_config.ErrorBuilderConfig)) == sorted(expected_fields)

    def test_global_constants_instances(self):
        """Test the global config instances."""
        assert isinstance(meta_config.MOD_TYPE, meta_config.AttrModTypeConfig)
        assert isinstance(meta_config.BUILDER_CONFIG, meta_config.ErrorBuilderConfig)
