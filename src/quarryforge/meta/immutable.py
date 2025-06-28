"""Immutable class module."""

from typing import Any

__all__: list[str] = ['Namespace', 'ImmutableInstance']


class ImmutableMetaClass(type):
    """Prevent setting or deleting attributes after class creation."""

    def __setattr__(cls, name: str, value: Any) -> None:
        raise AttributeError('Immutable')

    def __delattr__(cls, name: str) -> None:
        raise AttributeError('Immutable')


class Namespace(ImmutableMetaClass):
    """Provide immutable structures with types and methods.

    Example of a class using this metaclass:
    ```
        class MyNamespace(metaclass=Namespace):
            CONSTANT = "some_value"

            @staticmethod
            def utility_function() -> str:
                ...
    ```
    """

    def __new__(
        mcs: type['Namespace'],
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
    ) -> 'Namespace':
        """Override new constructer with a default exception."""

        def _uninstantiable(
            self: Any, *args: Any, **kwargs: dict[str, Any]
        ) -> None:
            raise TypeError('Class has no instances.')

        attrs['__init__'] = _uninstantiable
        attrs['__slots__'] = ()

        cls = super().__new__(mcs, name, bases, attrs)

        return cls


class ImmutableInstance:
    """Enforce immutability for instances mixin class."""

    def __setattr__(cls, name: str, value: Any) -> None:
        raise TypeError('Immutable')

    def __delattr__(cls, name: str) -> None:
        raise TypeError('Immutable')
