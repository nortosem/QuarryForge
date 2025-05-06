"""Protocol Module

Define protocols used.
"""
from pathlib import Path
from typing import Protocol


class FossilRepoFile(Protocol):
    """Protocol for an immutable object reference for a fossil repository"""
    @property
    def file(self) -> Path:
        ...

    def __setattr__(self, name: str, value: Path) -> None:
        ...

    def __delattr__(self, name: str) -> None:
        ...


class Argument(Protocol):
    """Protocol for an immutable string reference to command line argument."""
    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> str:
        ...

    def __setattr__(self, name: str, value: str) -> None:
        ...

    def __delattr__(self, name: str) -> None:
        ...
