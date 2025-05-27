"""Decorator module

The decorator utilities or quarryforge.
"""
from functools import wraps
from typing import Callable, List, ParamSpec, TypeVar

from quarryforge.config.exception_conf import exception_config as config


__all__: List = ['validate_str_parameters']


_PARAM = ParamSpec('_PARAM')
_FUNC = TypeVar('_FUNC')


def validate_str_parameters(
    method: Callable[_PARAM, _FUNC]
) -> Callable[_PARAM, _FUNC]:
    """Decorator for staticmethods of namespaces.

    The decorator validates a staticmethod with a string argument.

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
        if len(args) > 10:
            raise TypeError(
                f'This decorator supports a maximum of ten arguments. '
                f'Got {len(args)}.'
            )
        if kwargs:
            raise TypeError(
                f'Function {method.__name__}: keyword arguments not supported.'
            )
        for parameter in args:
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
