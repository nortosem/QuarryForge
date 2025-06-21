"""Decorator module

The decorator utilities or quarryforge.
"""

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from quarryforge.config.exception_conf import exception_config as config

__all__: list[str] = ['validate_str_parameters']


_PARAM = ParamSpec('_PARAM')
_FUNC = TypeVar('_FUNC')


def validate_str_parameters(
    method: Callable[_PARAM, _FUNC],
) -> Callable[_PARAM, _FUNC]:
    """Decorator for functions with all string arguments.

    The decorator validates all arguments are non-empty strings.

    Args:
        method: The method being decorated.

    Returns:
        The wrapped method with validation logic.

    Raises:
        TypeError: If a keyword argument is provided.
        TypeError: If the argument is not a string.
        ValueError: If the argument is an empty string.
    """

    @wraps(method)
    def wrapper(*args: _PARAM.args, **kwargs: _PARAM.kwargs) -> _FUNC:
        if kwargs:
            raise TypeError(
                f'Function {method.__name__}: keyword arguments not supported.'
            )
        for parameter in args:
            if not isinstance(parameter, str):
                raise TypeError(
                    f'{parameter!r} {config.DescMsg.MUST_BE}'
                    f' {config.DescMsg.A_VALID_STRING}'
                )
            if not parameter:
                raise ValueError(
                    f'{parameter!r} {config.DescMsg.MUST_BE}'
                    f' {config.DescMsg.A_NON_EMPTY_STRING}'
                )
        return method(*args, **kwargs)

    return wrapper
