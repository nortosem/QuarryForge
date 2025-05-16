"""Immutable class Module


"""
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, List, Tuple

from quarryforge.config import root


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

    Prevent function namespace classes from instantiation.
    """
    def __new__(
            mcs,
            name: str,
            bases: Tuple[type, ...],
            attrs: Dict[str, Any]
    ):
        """"""
        def _uninstantiable(self, *args, **kwargs):
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

