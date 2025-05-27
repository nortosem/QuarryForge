"""Decorator module

The decorator utilities or quarryforge.
"""
from functools import wraps
from typing import Callable, List, ParamSpec, TypeVar

from quarryforge.config.exception_conf import exception_config as config


__all__: List = ['validate_str_parameter']


_PARAM = ParamSpec('_PARAM')
_FUNC = TypeVar('_FUNC')


def validate_str_parameter(
    method: Callable[_PARAM, _FUNC]
) -> Callable[_PARAM, _FUNC]:
    """Decorator for staticmethods of namespaces.

    The decorator validates a staticmethod with a single string argument.

    Args:
        method: The staticmethod being decorated.

    Returns:
        The wrapped method with validation logic.

    Raises:
        TypeError: If more than one argument is provided.
        TypeError: If the argument is not a string.
        ValueError: If the argument is an empty string.
    """
    @wraps(method)
    def wrapper(*args: _PARAM.args, **kwargs: _PARAM.kwargs) -> _FUNC:
        if len(args) != 1:
            raise TypeError(
                f'Function {method.__name__}: Expected exactly '
                f'one positional argument value. Got {len(args)} instead.'
            )

        if kwargs:
            raise TypeError(
                f'Function {method.__name__}: keyword arguments not supported.'
            )

        parameter = args[0]

        if not isinstance(parameter, str):
            raise TypeError(
                f'{parameter!r} {config.DESC_TYPE.must_be}'
                f' {config.DESC_TYPE.string}'
            )
        if not parameter:
            raise ValueError(
                f'{parameter!r} {config.DESC_TYPE.must_be}'
                f' {config.DESC_TYPE.unempty}'
            )
        return method(*args, **kwargs)
    return wrapper
