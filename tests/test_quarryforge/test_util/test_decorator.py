"""Unit tests for the quarryforge.util.decorator module.

This test suite provides comprehensive, MC/DC (Modified Condition/Decision
Coverage) tests for the `validate_str_parameters` decorator.
"""

import pytest

from quarryforge.config.exception_conf import exception_config as config
from quarryforge.util.decorator import validate_str_parameters


def sample_function_to_decorate(*args: str) -> tuple[str, ...]:
    """This is a sample docstring."""
    return args


decorated_sample_function = validate_str_parameters(sample_function_to_decorate)


class TestValidateStrParameters:
    """Tests for the @validate_str_parameters decorator."""

    def test_preserves_function_metadata(self):
        """Verify that the decorator correctly uses @functools.wraps
        to preserve the original function's name and docstring.
        """
        assert (
            decorated_sample_function.__name__ == 'sample_function_to_decorate'
        )
        assert (
            decorated_sample_function.__doc__ == 'This is a sample docstring.'
        )

    @pytest.mark.parametrize(
        'args, expected_return',
        [
            (('arg1', 'arg2'), ('arg1', 'arg2')),
            (('single_argument',), ('single_argument',)),
            ((), ()),
        ],
    )
    def test_successful_validation(
        self, args: tuple[str, ...], expected_return: tuple[str, ...]
    ):
        """Test the success path where all arguments are valid, non-empty
        strings.

        The decorator should call the original function and return
        its result.
        """
        result = decorated_sample_function(*args)
        assert result == expected_return

    def test_raises_error_on_keyword_arguments(self):
        """Test the first decision point: `if kwargs:`.

        This should immediately raise a TypeError without checking other
        arguments.
        """
        with pytest.raises(TypeError, match='keyword arguments not supported'):
            decorated_sample_function(valid_arg='value', another_kw='value2')

        with pytest.raises(TypeError, match='keyword arguments not supported'):
            decorated_sample_function('valid_positional', kwarg='invalid')

    @pytest.mark.parametrize(
        'invalid_args',
        [
            (123,),
            (None,),
            (True,),
            (['a', 'b'],),
            (('a', 'b'),),
            ({'key': 'val'},),
            ('valid_string', 123),
        ],
    )
    def test_raises_error_on_non_string_argument(self, invalid_args: tuple):
        """Test the second decision point: `if not isinstance(parameter, str)`.

        This should raise a TypeError for any non-string argument.
        """
        expected_msg = f'{config.DESC_MSG.must_be} {config.DESC_MSG.string}'
        with pytest.raises(TypeError, match=expected_msg):
            decorated_sample_function(*invalid_args)

    @pytest.mark.parametrize(
        'invalid_args',
        [
            ('',),
            ('valid_string', ''),
            (' ', ''),
        ],
    )
    def test_raises_error_on_empty_string_argument(
        self, invalid_args: tuple[str, ...]
    ):
        """Test the third decision point: `if not parameter`.

        This should raise a ValueError for an empty string argument.
        """
        expected_msg = f'{config.DESC_MSG.must_be} {config.DESC_MSG.unempty}'
        with pytest.raises(ValueError, match=expected_msg):
            decorated_sample_function(*invalid_args)
