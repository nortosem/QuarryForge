"""Unit tests for the meta-exception framework.

This suite provides comprehensive coverage for the classes and functions in
quarryforge.exception.meta_exception and
quarryforge.config.exception_conf.meta_exception_config.
"""

import logging

from quarryforge.exception import base_exception, meta_exception


class DummyTestInstance:
    pass

BASE_ERROR_ARGS = {
    "code": "META_TEST_CODE",
    "message": "Test meta message",
    "user_message": "Test meta user message",
}


class TestImmutableError:
    """Tests for the ImmutableError exception class."""

    def test_inheritance(self):
        """Verify correct inheritance from MetaError and AttributeError."""
        logging.info("Testing ImmutableError: inheritance.")
        assert issubclass(meta_exception.ImmutableError, base_exception.MetaError)
        assert issubclass(meta_exception.ImmutableError, AttributeError)

    def test_init_with_full_details(self):
        """Test initialization when name and obj details are provided."""
        logging.info("Testing ImmutableError: initialization with full details.")
        dummy = DummyTestInstance()
        details = {'field': 'test_attr', 'arg': dummy}
        error = meta_exception.ImmutableError(**BASE_ERROR_ARGS, details=details)

        assert error.name == 'test_attr'
        assert error.obj is dummy
        assert error.code == "META_TEST_CODE"

    def test_init_with_no_details(self):
        """Test initialization when the details dictionary is not provided."""
        logging.info("Testing ImmutableError: initialization without details.")
        error = meta_exception.ImmutableError(**BASE_ERROR_ARGS, details=None)

        assert error.name is None
        assert error.obj is None
        assert str(error.args[0]) == "Test meta message"
