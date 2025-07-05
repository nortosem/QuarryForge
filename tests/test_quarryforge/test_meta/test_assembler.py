"""Unit tests for the quarryforge.meta.assembler module.

This suite provides comprehensive coverage for the ErrorBuilder ABC and its
private helper functions, ensuring all validation and data assembly logic
is correct.
"""

import logging
from typing import Any

import pytest

from quarryforge.config.exception_conf import exception_data as error
from quarryforge.meta import assembler


class TestAssemblerHelpers:
    """Test the private validation helper functions in the assembler module."""

    @pytest.mark.parametrize("value", ["test", " a "])
    def test_valid_str_type_success(self, value: str):
        """Test _valid_str_type with valid string inputs."""
        logging.info(
            'Testing _valid_str_type: success case with value "%s".',
            value
        )
        assert assembler._valid_str_type(value) == value

    @pytest.mark.parametrize("value", [123, None, []])
    def test_valid_str_type_failure(self, value: Any):
        """Test _valid_str_type with non-string inputs."""
        logging.info(
            'Testing _valid_str_type: failure case with type %s.',
            type(value).__name__
        )
        with pytest.raises(TypeError, match='must be a valid string'):
            assembler._valid_str_type(value)

    def test_valid_str_value_success(self):
        """Test _valid_str_value with a valid non-empty string."""
        logging.info("Testing _valid_str_value: success case.")
        assert assembler._valid_str_value('test') == 'test'

    @pytest.mark.parametrize('value', ['', '  '])
    def test_valid_str_value_failure(self, value: str):
        """Test _valid_str_value with empty or whitespace-only strings."""
        logging.info(
            'Testing _valid_str_value: failure case with value "%s".',
            value
        )
        with pytest.raises(ValueError, match='a non-empty string'):
            assembler._valid_str_value(value)

    @pytest.mark.parametrize(
        'field_value, info_value',
        [
            ('field', 'info'),
            (None, 'info'),
            ('field', None),
            (None, None),
        ]
    )
    def test_validate_init_mcdc(self, field_value, info_value):
        """Test _validate_init with all combinations of optional arguments."""
        logging.info(
            'Testing _validate_init: field=%s, info=%s.',
            field_value, info_value
        )
        context, code, field, info = assembler._validate_init(
            'ctx', 'code', field_value, info_value
        )
        assert context == 'ctx'
        assert code == 'code'
        assert field == field_value
        assert info == info_value

    def test_validate_init_failure(self):
        """Test _validate_init with invalid required arguments."""
        logging.info('Testing _validate_init: failure cases.')
        with pytest.raises(TypeError):
            assembler._validate_init(None, 'code')
        with pytest.raises(ValueError):
            assembler._validate_init('', 'code')


class ConcreteErrorBuilder(assembler.ErrorBuilder):
    """A minimal, concrete implementation of ErrorBuilder for testing."""
    def code(self) -> str:
        return f'{self.error_context}.{self.error_code}'
    def message(self) -> str:
        return f'Message: {self.info}'
    def user_message(self) -> str:
        return 'User message.'


class TestErrorBuilder:
    """Tests for the ErrorBuilder abstract base class."""

    def test_init_success(self):
        """Verify all attributes are set correctly during initialization."""
        logging.info('Testing ErrorBuilder.__init__: success path.')
        details = {'extra': 'data'}
        builder = ConcreteErrorBuilder(
            error_context='ctx.test',
            error_code='TEST_CODE',
            arg='arg_val',
            field='field_name',
            info='info_str',
            extra_details=details
        )
        assert builder.error_context == 'ctx.test'
        assert builder.error_code == 'TEST_CODE'
        assert builder.arg == 'arg_val'
        assert builder.field == 'field_name'
        assert builder.info == 'info_str'
        assert builder.extra_details == details

    def test_init_invalid_extra_details_type(self):
        """Test that __init__ raises TypeError if extra_details is not a dict."""
        logging.info(
            'Testing ErrorBuilder.__init__: invalid extra_details type.'
        )
        with pytest.raises(TypeError, match='a valid dictionary'):
            ConcreteErrorBuilder(
                error_context='ctx',
                error_code='code',
                extra_details='not a dict'
            )

    def test_base_message_method(self):
        """Test the _base_message helper method."""
        logging.info('Testing ErrorBuilder._base_message.')
        builder = ConcreteErrorBuilder(
            error_context='ctx.test',
            error_code='CODE'
        )
        expected = 'Error in `ctx.test` (Code: CODE).'
        assert builder._base_message() == expected

    def test_details_method_mcdc(self):
        """Test details() method with all combinations of optional attributes."""
        logging.info('Testing ErrorBuilder.details(): full data case.')
        # Case 1: All optional attributes are provided
        full_builder = ConcreteErrorBuilder(
            error_context='ctx', error_code='code',
            arg='arg_val', field='field_name', info='info_str',
            extra_details={'extra': 'data'}
        )
        details = full_builder.details()
        assert details[error.builder_config().arg] == "arg_val"
        assert details[error.builder_config().field] == "field_name"
        assert details[error.builder_config().info] == "info_str"
        assert details['extra'] == 'data'

        logging.info('Testing ErrorBuilder.details(): minimal data case.')
        # Case 2: No optional attributes are provided
        minimal_builder = ConcreteErrorBuilder(
            error_context='ctx',
            error_code='code'
        )
        details = minimal_builder.details()
        assert error.builder_config().arg not in details
        assert error.builder_config().field not in details
        assert error.builder_config().info not in details

    def test_data_method(self):
        """Test the data() method for correct ValidErrorData construction."""
        logging.info('Testing ErrorBuilder.data().')
        builder = ConcreteErrorBuilder(
            error_context='ctx', error_code='code', info='info_str'
        )
        error_data = builder.data()

        assert isinstance(error_data, error.ValidErrorData)
        assert error_data.code == 'ctx.code'
        assert error_data.message == 'Message: info_str'
        assert error_data.user_message == 'User message.'
        assert isinstance(error_data.details, dict)
        assert error_data.details[error.builder_config().error_context] == 'ctx'
