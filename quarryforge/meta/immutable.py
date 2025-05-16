"""Immutable Metaclass Module


"""
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, List, Tuple

from quarryforge.config import root


class Immutable(type):
    """Immutable MetaClass

    Metaclass to prevent setting or deleting attributes on the class itself.
    This allows utility classes with no attributes and ensure that immutable
    class instances remain immutable on the class itself prior to
    instantiation.
    """
    def __setattr__(cls, name: str, value: Any) -> None:
        raise Exception('Immutable')

    def __delattr__(cls, name: str) -> None:
        raise Exception('Immutable')
