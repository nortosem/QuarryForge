"""Unit tests for the quarryforge.exception.base_exception module.

This suite provides comprehensive coverage for the QuarryForgeError base class
and all its direct subclasses.
"""

import logging
from datetime import UTC, datetime

import pytest
from freezegun import freeze_time

from quarryforge.config.exception_conf import exception_data as _
from quarryforge.exception import base_exception


@freeze_time("2024-01-01 12:00:00 UTC")
class TestQuarryForgeError:
    """Tests for the base QuarryForgeError class."""

    def test_initialization(self):
        """Verify all attributes are set correctly during initialization."""
        logging.info("Testing QuarryForgeError: standard initialization.")
        details = {'extra': 'info', 'value': 123}
        error = base_exception.QuarryForgeError(
            message="Test message",
            code="TEST_CODE",
            user_message="A test error occurred.",
            details=details,
        )

        assert isinstance(error, Exception)
        assert error.code == "TEST_CODE"
        assert error.details == details
        assert error.user_message == "A test error occurred."
        assert error.timestamp == datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        assert str(error.args[0]) == "Test message"

    def test_initialization_with_no_details(self):
        """Test initialization when the details dictionary is not provided."""
        logging.info("Testing QuarryForgeError: initialization with no details.")
        error = base_exception.QuarryForgeError(
            message="No details", code="NO_DETAILS", user_message="User message"
        )
        assert error.details == {}

    def test_to_dict_method(self):
        """Test the to_dict() method for correct dictionary representation."""
        logging.info("Testing QuarryForgeError: to_dict() method.")
        details = {'extra': 'info'}
        error = base_exception.QuarryForgeError(
            message="Dict test",
            code="DICT_CODE",
            user_message="User dict message",
            details=details,
        )

        expected_dict = {
            _.error_data_config().message: '[DICT_CODE] Dict test (extra: info)',
            _.error_data_config().code: "DICT_CODE",
            _.error_data_config().details: details,
            _.error_data_config().timestamp: "2024-01-01T12:00:00+00:00",
            _.error_data_config().user_message: "User dict message",
        }
        assert error.to_dict() == expected_dict

    @pytest.mark.parametrize(
        'code, message, details, expected_str',
        [
            # Case 1: All parts present
            ('CODE_A', 'Message A', {'detail_key': 'detail_value'},
             '[CODE_A] Message A (detail_key: detail_value)'),
            # Case 2: No details
            ('CODE_B', 'Message B', None,
             '[CODE_B] Message B'),
            # Case 3: No code
            (None, 'Message C', {'detail_key': 'detail_value'},
             'Message C (detail_key: detail_value)'),
            # Case 4: Only message
            (None, 'Message D', None,
             'Message D'),
            # Case 5: Details contain keys that should be filtered out
            ('CODE_E', 'Message E',
             {
                 'detail_key': 'value',
                 _.error_data_config().code: 'IGNORED',
                 _.error_data_config().message: 'IGNORED',
                 _.error_data_config().user_message: 'IGNORED',
             },
             '[CODE_E] Message E (detail_key: value)'),
            # Case 6: Details exist but are empty after filtering
            ('CODE_F', 'Message F',
             {
                 _.error_data_config().code: 'IGNORED',
                 _.error_data_config().message: 'IGNORED',
             },
             '[CODE_F] Message F'),
        ]
    )
    def test_str_representation_mcdc(self, code, message, details, expected_str):
        """Test the __str__() method with all combinations of attributes."""
        logging.info(
            "Testing QuarryForgeError: __str__ representation (code=%s).",
            code
        )
        error = base_exception.QuarryForgeError(
            message=message, code=code, user_message="dummy", details=details
        )
        assert str(error) == expected_str


class TestSubclassInheritance:
    """Tests the simple subclasses of QuarryForgeError."""

    @pytest.mark.parametrize(
        "subclass",
        [
            base_exception.ModelError,
            base_exception.FossilError,
            base_exception.MainError,
            base_exception.MetaError,
            base_exception.UtilError,
        ]
    )
    def test_subclasses_inherit_from_quarryforgeerror(self, subclass):
        """Verify that all module-specific base exceptions inherit correctly."""
        logging.info("Testing inheritance for subclass: %s", subclass.__name__)
        instance = subclass(message="test", code="test", user_message="test")
        assert isinstance(instance, base_exception.QuarryForgeError)

    def test_subclasses_are_distinct(self):
        """Verify that the subclasses are distinct types."""
        logging.info("Testing distinctness of exception subclasses.")
        assert base_exception.ModelError is not base_exception.FossilError
