"""Model Utility Module

This module provides utility functions for validating different types of
arguments used within the data models. It includes functions to check for
valid string types, non-empty strings, valid and existing paths (files and
directories), and readable/writable paths. It also includes functions for
validating list types and the content of lists based on specific error
conditions.

#TODO
# fossil file validation TODO
"""
import os
from pathlib import Path
from typing import List, TypeVar

from quarryforge.config.exception_conf import PathMessage
from quarryforge.exceptions import base_exception
from quarryforge.exceptions.model_exception import commit_exception

_ModelError = TypeVar('_ModelError', bound=base_exception.ModelError)


def is_valid_str_type(arg: str, exception: type[_ModelError]) -> str:
    """Validates if the given argument is a string.

    Args:
        arg: The string argument to check.
        exception: The specific type of exception to raise.

    Returns:
        The validated string argument.

    Raises:
        exception: If the argument is not a string.
    """
    if not isinstance(arg, str):
        raise exception()
    return arg


def is_not_empty(arg: str, exception: type[_ModelError]) -> str:
    """Validates if the given string argument is not empty.

    This function checks if the string is not empty after stripping leading
    and trailing whitespace.

    Args:
        arg: The string argument to check.
        exception: The specific type of exception to raise.

    Returns:
        The validated string argument.

    Raises:
        exception: If the argument is empty after stripping whitespace.
    """
    if not arg.strip():
        raise exception()
    return arg


def is_valid_path_type(arg: Path, exception: type[_ModelError]) -> Path:
    """Validates if the given argument is a pathlib.Path object.

    Args:
        arg: The path argument to check.
        exception: The specific type of exception to raise.

    Returns:
        The validated Path object.

    Raises:
        exception: If the argument is not a Path object.
    """
    if not isinstance(arg, Path):
        raise exception()
    return arg


def exists(arg: Path, exception: type[_ModelError]) -> Path:
    """Validates if the path specified by the pathlib.Path object exists.

    Args:
        arg: The path argument to check.
        exception: The specific type of exception to raise.

    Returns:
        The validated Path object.

    Raises:
        exception: If the path does not exist.
    """
    if not arg.exists():
        raise exception(PathMessage.does_not_exist(str(arg)))
    return arg


def is_file(arg: Path, exception: type[_ModelError]) -> Path:
    """Verify the path is a file

    Assumes Path already is a pathlib.Path.

    Args:
        arg (Path): The repo path argument to check.
        exception (Exception): The specific type of exception to raise.

    Returns:
        path (Path): Returns a valid path path attribute.
    """
    path = arg
    if not path.is_file():
        raise exception(PathMessage.not_a_file(path))
    return path


def is_dir(arg: Path, exception: type[_ModelError]) -> Path:
    """Validates if the path specified by the pathlib.Path object is directory.

    Args:
        arg: The path argument to check.
        exception: The specific type of exception to raise.

    Returns:
        The validated Path object.

    Raises:
        exception: If the path is not a directory.
    """
    if not arg.is_dir():
        raise exception(PathMessage.not_a_directory(str(arg)))
    return arg


def is_read_ok(arg: Path, exception: type[_ModelError]) -> Path:
    """Validates if the path specified by the pathlib.Path object has read
    permissions.

    Args:
        arg: The path argument to check.
        exception: The specific type of exception to raise.

    Returns:
        The validated Path object.

    Raises:
        exception: If the path does not have read permissions.
    """
    if not os.access(arg, os.R_OK):
        raise exception(PathMessage.no_read_permission(str(arg)))
    return arg


def is_write_ok(arg: Path, exception: type[_ModelError]) -> Path:
    """Validates if the path specified by the pathlib.Path object has write
    permissions.

    Args:
        arg: The path argument to check.
        exception: The specific type of exception to raise.

    Returns:
        The validated Path object.

    Raises:
        exception: If the path does not have write permissions.
    """
    if not os.access(arg, os.W_OK):
        raise exception(PathMessage.no_write_permission(str(arg)))
    return arg


def viable_infile(arg: Path, exception: type[_ModelError]) -> Path:
    """Validates if the path is an existing, readable file.

    Args:
        arg: The path argument to check.
        exception: The specific type of exception to raise.

    Returns:
        The validated Path object.

    Raises:
        exception: If the path does not exist, is not a file, or is not
        readable.
    """
    path = exists(arg, exception)
    path = is_file(path, exception)
    path = is_read_ok(path, exception)
    return path


def viable_source(arg: Path, exception: type[_ModelError]) -> Path:
    """Validates if the path is an existing, readable file.

    This is an alias for `viable_infile`.

    Args:
        arg: The path argument to check.
        exception: The specific type of exception to raise.

    Returns:
        The validated Path object.

    Raises:
        exception: If the path does not exist, is not a file, or is not
        readable.
    """
    return viable_infile(arg, exception)


def viable_output(arg: Path, exception: type[_ModelError]) -> Path:
    """Validates if the path is an existing, writable file.

    Args:
        arg: The path argument to check.
        exception: The specific type of exception to raise.

    Returns:
        The validated Path object.

    Raises:
        exception: If the path does not exist, is not a file, or is not
        writable.
    """
    path = exists(arg, exception)
    path = is_file(path, exception)
    path = is_write_ok(path, exception)
    return path


def viable_update_dir(arg: Path, exception: type[_ModelError]) -> Path:
    """Validates if the path is an existing, writable directory.

    Args:
        arg: The path argument to check.
        exception: The specific type of exception to raise.

    Returns:
        The validated Path object.

    Raises:
        exception: If the path does not exist, is not a directory, or is not
        writable.
    """
    path = exists(arg, exception)
    path = is_dir(path, exception)
    path = is_write_ok(path, exception)
    return path

def check_list_type(arg: List, exception: type[_ModelError]) -> List:
    """Validates if the given argument is a list.

    Args:
        arg: The list argument to check.
        exception: The specific type of exception to raise.

    Returns:
        The validated list argument.  Returns an empty list if arg is None.

    Raises:
        exception: If the argument is not a list and not None.
    """
    final_list: List = []
    if arg is not None:
        if not isinstance(arg, list):
            raise exception()
        final_list = arg
    return final_list


def content_type_error(
    args: List[str],
    exception: type[_ModelError]
) -> List[str]:
    """Validates if all elements within the given list are strings.

    Args:
        args: The list of strings to check.
        exception: The specific type of exception to raise.

    Returns:
        The validated list of strings.

    Raises:
        exception: If any element in the list is not a string.
    """
    for item in args:
        if not isinstance(item, str):
            raise exception()
    return args


def content_empty_error(
    args: List[str],
    exception: type[_ModelError]
) -> List[str]:
    """Validates if all string elements within the given list are not empty.

    This function checks if each string in the list is not empty after
    stripping leading and trailing whitespace.

    Args:
        args: The list of strings to check.
        exception: The specific type of exception to raise.

    Returns:
        The validated list of strings.

    Raises:
        exception: If any string in the list is empty after stripping
        whitespace.
    """
    for item in args:
        if not item.strip():
            raise exception()
    return args


def check_list_content(
    arg: List[str],
    exception: type[_ModelError]
) -> List[str]:
    """Validates the content of a list of strings based on the exception type.

    This function provides specific validation for lists of strings used in
    different contexts (e.g., tags or changes in a commit).

    Args:
        arg: The list of strings to check.
        exception: The specific type of exception to raise for content errors.

    Returns:
        The validated list of strings.

    Raises:
        commit_exception.TagTypeError: If any tag is not a string.
        commit_exception.TagValueError: If any tag is empty or contains spaces.
        commit_exception.ChangeTypeError: If any change is not a string.
        commit_exception.ChangeValueError: If any change is empty.
    """
    items = arg
    if exception is commit_exception.TagsCommitError:
        items = content_type_error(items, commit_exception.TagTypeError)
        items = content_empty_error(items, commit_exception.TagValueError)
        for tag in items:
            if ' ' in tag:
                raise commit_exception.TagValueError()

    if exception is commit_exception.ChangesCommitError:
        items = content_type_error(items, commit_exception.ChangeTypeError)
        items = content_empty_error(items, commit_exception.ChangeValueError)

    return items
