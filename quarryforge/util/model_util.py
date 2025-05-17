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

from quarryforge.config.exception_conf import exception_config as msg
from quarryforge.exception import base_exception
from quarryforge.exception import model_exception

_ModelError = TypeVar('_ModelError', bound=base_exception.ModelError)


def is_valid_str_type(
    arg: str,
    field: str,
    exception: type[_ModelError]) -> str:
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


def is_not_empty(
    arg: str,
    exception: type[_ModelError]
) -> str:
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


def resolve_path_arg(arg: Path | str, exception: type[_ModelError]) -> Path:
    """Resolve a path or convert and resolve a string argument

    Args:
        arg: The path argument to check.
        exception: The specific type of exception to raise.

    Returns:
        The validated Path object.

    Raises:
        RuntimeError if the expanduser function fails
        OSError for permission or other os errors.
        exception: if the argument s is not a string or Path object.
    """
    if isinstance(arg, str):
        arg = is_not_empty(arg, )
        return arg.expanduser().resolve()
    elif isinstance(arg, Path):
        try:
            return arg.expanduser().resolve()
        except RuntimeError as run_error:
            raise
        except OSError as os_error:
            raise
    else:
        raise exception


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
        raise exception(message.PathMessage.does_not_exist(str(arg)))
    return arg


def is_file(arg: Path, exception: type[_ModelError]) -> Path:
    """Verify the path is a file

    Assumes Path already is a pathlib.Path.

    Args:
        arg (Path): The repo path argument to check.
        exception (Exception): The specific type of exception to raise.

    Returns:
        A valid path path attribute.
    """
    if not arg.is_file():
        raise exception(message.PathMessage.not_a_file(path))
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
        raise exception(message.PathMessage.not_a_directory(str(arg)))
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
        raise exception(message.PathMessage.no_read_permission(str(arg)))
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
        raise exception(message.PathMessage.no_write_permission(str(arg)))
    return arg


def viable_fossil_repo(
    self,
    file: Path | str,
    is_new: bool,
    exception: type[_ModelError]
) -> Path:
    """Validates if the path points to a viable Fossil repository.

    For an existing repository (is_new=False):
    - Must be a Path or string.
    - Must exist.
    - Must be a file.
    - Must be readable.
    - Must be a Fossil repository

    For a new repository (is_new=True):
    - Must be a Path or string.
    - File itself must NOT exist.
    - Parent directory must exist and be writable.

    Args:
        arg:
            The path (Path object or string) to the Fossil repository.
        is_new:
            If True, validates for creating a new repository.
            If False (default), validates an existing repository.

    Returns:
        The validated and resolved Path object.

    Raises:
        exception: With specific codes and messages for different failures.
    """
    if not isinstance(file, (str, Path)):
        raise exception
    if isinstance(file, str):
        try:
            if file.strip():
                return (file := (file := Path(file)).expanduser().resolve())
            else:
                raise exception("Empty string not a valid Path")
        except Exception as e:
            raise e

    elif isinstance(file, Path):
        try:
            return arg.expanduser().resolve()
        except RuntimeError as run_error:
            raise
        except OSError as os_error:
            raise
    else:
        raise exception


def viable_update_repo() -> Path:
    pass


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
