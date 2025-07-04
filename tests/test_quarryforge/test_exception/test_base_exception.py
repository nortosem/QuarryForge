"""Unit tests for the quarryforge.exception.base_exception module.

This suite provides comprehensive, MC/DC-focused coverage for the
QuarryForgeError base class and verifies the inheritance of its subclasses.
"""

import datetime
from unittest.mock import patch

import pytest

from quarryforge.config.exception_conf import exception_data as ed
from quarryforge.exception import base_exception as be

FIXED_DATETIME = datetime.datetime(2023, 10, 27, 10, 0, 0, tzinfo=datetime.UTC)
FIXED_ISO_FORMAT = FIXED_DATETIME.isoformat()


@pytest.fixture
def mock_datetime_now():
    """Fixture to patch datetime.datetime.now to return a fixed time."""
    with patch('datetime.datetime') as mock_dt:
        mock_dt.now.return_value = FIXED_DATETIME
        mock_dt.UTC = datetime.UTC
        yield mock_dt


class TestQuarryForgeError:
    """Tests for the QuarryForgeError base class."""

    def test_inheritance(self):
        """Verify that QuarryForgeError is a subclass of Exception."""
        assert issubclass(be.QuarryForgeError, Exception)

    def test_initialization_full(self, mock_datetime_now):
        """Test initialization with all arguments provided."""
        details = {'extra': 'info', 'arg': 123}
        err = be.QuarryForgeError(
            message='Technical message',
            code='E1001',
            user_message='User-friendly message',
            details=details,
        )
        assert err.code == 'E1001'
        assert err.details == details
        assert err.user_message == 'User-friendly message'
        assert str(err.args[0]) == 'Technical message'
        assert err.timestamp == FIXED_DATETIME

    def test_initialization_minimal(self, mock_datetime_now):
        """Test initialization with only required arguments, verifying
        defaults.
        """
        err = be.QuarryForgeError(
            message='Minimal message',
            code='E1002',
            user_message='Minimal user message',
        )
        assert err.code == 'E1002'
        assert err.details == {}
        assert err.user_message == 'Minimal user message'
        assert err.timestamp == FIXED_DATETIME

    @pytest.mark.parametrize(
        'init_kwargs, expected_str',
        [
            (
                {
                    'code': 'C1',
                    'message': 'Msg1',
                    'user_message': 'UM1',
                    'details': {'extra': 'info'},
                },
                '[C1] Msg1 (extra: info)',
            ),
            (
                {
                    'code': '',
                    'message': 'Msg2',
                    'user_message': 'UM2',
                    'details': {'arg': 42},
                },
                'Msg2 (arg: 42)',
            ),
            (
                {
                    'code': 'C3',
                    'message': '',
                    'user_message': 'UM3',
                    'details': {'extra': 'info'},
                },
                '[C3] (extra: info)',
            ),
            (
                {
                    'code': 'C4',
                    'message': 'Msg4',
                    'user_message': 'UM4',
                    'details': None,
                },
                '[C4] Msg4',
            ),
            (
                {
                    'code': 'C5',
                    'message': 'Msg5',
                    'user_message': 'UM5',
                    'details': {'code': 'C5', 'message': 'Msg5'},
                },
                '[C5] Msg5',
            ),
            (
                {
                    'code': 'C6',
                    'message': '',
                    'user_message': 'UM6',
                    'details': None,
                },
                '[C6]',
            ),
            (
                {
                    'code': '',
                    'message': 'Msg7',
                    'user_message': 'UM7',
                    'details': None,
                },
                'Msg7',
            ),
            (
                {
                    'code': '',
                    'message': '',
                    'user_message': 'UM8',
                    'details': None,
                },
                '',
            ),
        ],
    )
    def test_str_representation_mcdc(self, init_kwargs, expected_str):
        """Test __str__ method with various combinations of arguments for
        MC/DC.
        """
        err = be.QuarryForgeError(**init_kwargs)
        assert str(err) == expected_str

    def test_to_dict_conversion(self, mock_datetime_now):
        """Test the to_dict method for correct dictionary representation."""
        details = {'extra': 'info', 'arg': 123}
        err = be.QuarryForgeError(
            message='Technical message',
            code='E1001',
            user_message='User-friendly message',
            details=details.copy(),
        )

        expected_dict = {
            ed.error_data_config().message: str(err),
            ed.error_data_config().code: 'E1001',
            ed.error_data_config().details: details,
            ed.error_data_config().timestamp: FIXED_ISO_FORMAT,
            ed.error_data_config().user_message: 'User-friendly message',
        }

        assert err.to_dict() == expected_dict


@pytest.mark.parametrize(
    'subclass',
    [
        be.ModelError,
        be.FossilError,
        be.MainError,
        be.MetaError,
        be.UtilError,
    ],
)
class TestSubclassInheritance:
    """Tests to ensure all specific error classes inherit from QuarryForgeError."""

    def test_inheritance(self, subclass):
        """Verify that the given subclass inherits from QuarryForgeError."""
        assert issubclass(subclass, be.QuarryForgeError)

    def test_instantiation(self, subclass):
        """Verify that subclasses can be instantiated with the same signature."""
        instance = subclass(message='test', code='test', user_message='test')
        assert isinstance(instance, be.QuarryForgeError)
        assert str(instance) == '[test] test'
