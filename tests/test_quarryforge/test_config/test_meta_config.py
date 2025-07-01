"""Unit tests for the quarryforge.config.meta_config module."""

from quarryforge.config import meta_config
from quarryforge.config.exception_conf import exception_data


class TestMetaConfig:
    """Tests for quarryforge.config.meta_config"""

    def test_module_dunder_all(self):
        """Test the __all__ variable."""
        assert hasattr(meta_config, '__all__')
        assert meta_config.__all__ == []

    def test_attribute_modifier_type_factory(self):
        """Test the attribute_modifier_type factory and its return object."""
        cfg = meta_config.attribute_modifier_type()
        assert isinstance(cfg, meta_config.AttrModTypeConfig)
        assert cfg.set_attribute == 'set attribute'
        assert cfg.delete_attribute == 'delete attribute'

    def test_error_builder_factory(self):
        """Test the error_builder factory and its return object."""
        cfg = meta_config.error_builder()
        assert isinstance(cfg, meta_config.ErrorBuilderConfig)

        builder_fields = exception_data.builder_config()
        assert cfg.error_context == builder_fields.error_context
        assert cfg.error_code == builder_fields.error_code
        assert cfg.arg == builder_fields.arg
        assert cfg.extra_details == builder_fields.extra_details
        assert cfg.info == builder_fields.info
        assert cfg.field == builder_fields.field

        assert cfg.error_context == 'error_context'
        assert cfg.error_code == 'error_code'
        assert cfg.arg == 'arg'
        assert cfg.extra_details == 'extra_details'
        assert cfg.info == 'info'
        assert cfg.field == 'field'

        expected_fields = [
            'error_context',
            'error_code',
            'arg',
            'extra_details',
            'info',
            'field',
        ]
        assert sorted(cfg.slots()) == sorted(expected_fields)
