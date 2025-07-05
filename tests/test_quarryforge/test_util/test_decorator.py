"""Unit tests for the quarryforge.util.decorator module.

This suite provides comprehensive coverage for the @validate_str_parameters
decorator, ensuring all validation logic paths are tested.
"""

import logging
from typing import Any

import pytest

from quarryforge.util import decorator


@decorator.validate_str_parameters
def _dummy_decorated_function(*args: str) -> str:
    """A simple function to be decorated for testing purposes."""
    return ''.join(args)


class TestValidateStrParameters:
    """Tests for the @validate_str_parameters decorator."""

    def test_success_with_valid_strings(self):
        """Verify the decorator is functional.

        The decorator executes and returns the correct value when all
        arguments are valid, non-empty strings.
        """
        logging.info('Testing @validate_str_parameters: success path.')
        result = _dummy_decorated_function('hello', ' ', 'world')
        assert result == 'hello world'

    def test_failure_on_keyword_arguments(self):
        """MC/DC Test: Verify a TypeError is raised if kwargs are used."""
        logging.info('Testing @validate_str_parameters: failure on kwargs.')
        with pytest.raises(TypeError, match='keyword arguments not supported'):
            _dummy_decorated_function(arg1='a', arg2='b') # type: ignore

    @pytest.mark.parametrize(
        "invalid_arg",
        [
            123,
            None,
            [],
            {},
            ("a", "b"),
        ],
    )
    def test_failure_on_non_string_type(self, invalid_arg: Any):
        """Verify a TypeError is raised for non-string arguments."""
        logging.info(
            'Testing @validate_str_parameters: failure on non-string type "%s".',
            type(invalid_arg).__name__
        )
        with pytest.raises(TypeError, match='must be a valid string'):
            _dummy_decorated_function('good', invalid_arg, 'also_good')

    def test_failure_on_empty_string(self):
        """Verify a ValueError is raised for an empty string argument."""
        logging.info('Testing @validate_str_parameters: failure on empty string.')
        with pytest.raises(ValueError, match='must be a non-empty string'):
            _dummy_decorated_function('good', '', 'this_is_not_reached')
