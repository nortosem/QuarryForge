"""The decorator utility module."""

from collections.abc import Callable
from functools import wraps

from quarryforge.config.exception_conf import exception_config as config

__all__: list[str] = ['validate_str_parameters']


def validate_str_parameters[**PARAM, FUNC](
    method: Callable[PARAM, FUNC],
) -> Callable[PARAM, FUNC]:
    """Validate that all arguments are non-empty strings.

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
    def wrapper(*args: PARAM.args, **kwargs: PARAM.kwargs) -> FUNC:
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
