"""Immutable class Module


"""
from typing import Any, Dict, List, Tuple


__all__: List[str] = ['Namespace', 'ImmutableInstance']


class ImmutableMetaClass(type):
    """Immutable MetaClass

    Metaclass to prevent setting or deleting attributes on the class itself
    after initial class creation.
    """
    def __setattr__(cls, name: str, value: Any) -> None:
        raise AttributeError('Immutable')

    def __delattr__(cls, name: str) -> None:
        raise AttributeError('Immutable')


class Namespace(ImmutableMetaClass):
    """Namespace

    Namespaces provide immutable structures with types and methods.

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
        bases: Tuple[type, ...],
        attrs: Dict[str, Any]
    ) -> 'Namespace':
        """"""
        def _uninstantiable(
            self: Any,
            *args: Any,
            **kwargs: Dict[str,Any]
        ) -> None:
            raise TypeError('Class has no instances.')

        attrs['__init__'] = _uninstantiable
        attrs['__slots__'] = ()

        cls = super().__new__(mcs, name, bases, attrs)

        return cls


class ImmutableInstance:
    """ImmutableInstance

    A mixin class to enforce immutability for instances.
    """
    def __setattr__(cls, name: str, value: Any) -> None:
        raise TypeError('Immutable')

    def __delattr__(cls, name: str) -> None:
        raise TypeError('Immutable')

