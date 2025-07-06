"""Validation Utility module provides a collection of utility functions.

These utilities perform common validation tasks, such as type checking,
string emptiness checks, path validations (existence, type, permissions),
and list content validation. These functions are designed to raise specific,
configurable exceptions from the `quarryforge.exception` hierarchy upon
validation failure, providing detailed error information.
"""

import os
from pathlib import Path
from typing import Any, assert_never

from quarryforge.config import model_config
from quarryforge.exception import base_exception
from quarryforge.meta import assembler


def is_type_str[
    QuarryForgeError: base_exception.QuarryForgeError,
    ErrorBuilder: assembler.ErrorBuilder,
](
    *,
    arg: Any,
    exception: type[QuarryForgeError],
    error_builder: ErrorBuilder,
) -> str:
    """Validate if the given argument is a string.

    Args:
        arg: The argument to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        error_builder: Generate data specific to the possible error
            the given exception.

    Returns:
        The validated string argument if it is a string.

    Raises:
        exception: If the argument `arg` is not a string.

    """
    if not isinstance(arg, str):
        error_data = error_builder.data()
        raise exception(**error_data.to_exception())
    return arg


def is_str_not_empty[
    QuarryForgeError: base_exception.QuarryForgeError,
    ErrorBuilder: assembler.ErrorBuilder,
](
    *,
    arg: str,
    exception: type[QuarryForgeError],
    error_builder: ErrorBuilder,
) -> str:
    """Validate if the given string argument is not empty.

    This function checks if the string is not empty after stripping leading
    and trailing whitespace.

    Args:
        arg: The string argument to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        error_builder: The builder used to assemble data for an exception.

    Returns:
        The validated string argument if it is not empty.

    Raises:
        exception: If the argument `arg` is empty after stripping whitespace.

    """
    if not arg.strip():
        error_data = error_builder.data()
        raise exception(**error_data.to_exception())
    return arg


def is_type_path[
    QuarryForgeError: base_exception.QuarryForgeError,
    ErrorBuilder: assembler.ErrorBuilder,
](
    *,
    arg: Any,
    exception: type[QuarryForgeError],
    error_builder: ErrorBuilder,
) -> Path:
    """Validate if the given argument is a pathlib.Path object.

    Args:
        arg: The argument to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        error_builder: The builder used to assemble data for an exception.

    Returns:
        The validated Path object if `arg` is a `pathlib.Path` or a string
        converted into a path.

    Raises:
        exception:
            If the argument `arg` is not a `pathlib.Path` object or a valid
            string represenatation of a path.

    """
    if not isinstance(arg, (str, Path)):
        error_data = error_builder.data()
        raise exception(**error_data.to_exception())
    if isinstance(arg, str):
        valid_str = is_str_not_empty(
            arg=arg,
            exception=exception,
            error_builder=error_builder,
        )
        return Path(valid_str)
    return arg


def resolve_path_arg[
    QuarryForgeError: base_exception.QuarryForgeError,
    ErrorBuilder: assembler.ErrorBuilder,
](
    *,
    arg: Path,
    exception: type[QuarryForgeError],
    error_builder: ErrorBuilder,
) -> Path:
    """Resolve a path argument to an absolute path, expanding uservars.

    Checks if the argument is a `pathlib.Path` object, then attempts to
    expand the user directory (e.g., '~') and resolve it to an absolute path.

    Args:
        arg: The path argument (expected to be a `pathlib.Path` object).
        exception: The specific type of QuarryForgeError to raise on
            validation or resolution failure.
        error_builder: The builder used to assemble data for an exception.

    Returns:
        The resolved, absolute `pathlib.Path` object.

    Raises:
        exception: If `arg` is not a `pathlib.Path` object, or if path
            resolution fails due to `RuntimeError` (e.g., home directory
            cannot be determined) or `OSError` (e.g., permission issues,
            path does not exist and cannot be resolved).

    """
    try:
        return arg.expanduser().resolve()
    except RuntimeError as run_error:
        error_data = error_builder.data()
        raise exception(**error_data.to_exception()) from run_error
    except OSError as os_error:
        error_data = error_builder.data()
        raise exception(**error_data.to_exception()) from os_error


def exist[
    QuarryForgeError: base_exception.QuarryForgeError,
    ErrorBuilder: assembler.ErrorBuilder,
](
    *,
    arg: Path,
    exception: type[QuarryForgeError],
    error_builder: ErrorBuilder,
) -> Path:
    """Validate if the path specified exists.

    Args:
        arg: The `pathlib.Path` object to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        error_builder: The builder used to assemble data for an exception.

    Returns:
        The validated `pathlib.Path` object if the path exists.

    Raises:
        exception: If the path specified by `arg` does not exist.

    """
    if not arg.exists():
        error_data = error_builder.data()
        raise exception(**error_data.to_exception())
    return arg


def not_exist[
    QuarryForgeError: base_exception.QuarryForgeError,
    ErrorBuilder: assembler.ErrorBuilder,
](
    *,
    arg: Path,
    exception: type[QuarryForgeError],
    error_builder: ErrorBuilder,
) -> Path:
    """Validate if the path specified exists.

    Args:
        arg: The `pathlib.Path` object to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        error_builder: The builder used to assemble data for an exception.

    Returns:
        The validated `pathlib.Path` object if the path exists.

    Raises:
        exception: If the path specified by `arg` does not exist.

    """
    if arg.exists():
        error_data = error_builder.data()
        raise exception(**error_data.to_exception())
    return arg


def is_file[
    QuarryForgeError: base_exception.QuarryForgeError,
    ErrorBuilder: assembler.ErrorBuilder,
](
    *,
    arg: Path,
    exception: type[QuarryForgeError],
    error_builder: ErrorBuilder,
) -> Path:
    """Validate if the path specified is a file.

    Assumes `arg` is already a `pathlib.Path` object and exists.
    It's recommended to call `exists(arg, ...)` before this function.

    Args:
        arg: The `pathlib.Path` object to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        error_builder: The builder used to assemble data for an exception.

    Returns:
        The validated `pathlib.Path` object if it points to a file.

    Raises:
        exception: If the path specified by `arg` is not a file.

    """
    if not arg.is_file():
        error_data = error_builder.data()
        raise exception(**error_data.to_exception())
    return arg


def is_dir[
    QuarryForgeError: base_exception.QuarryForgeError,
    ErrorBuilder: assembler.ErrorBuilder,
](
    *,
    arg: Path,
    exception: type[QuarryForgeError],
    error_builder: ErrorBuilder,
) -> Path:
    """Validate if the path specified is a directory.

    Assumes `arg` is already a `pathlib.Path` object and exists.
    It's recommended to call `exists(arg, ...)` before this function.

    Args:
        arg: The `pathlib.Path` object to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        error_builder: The builder used to assemble data for an exception.

    Returns:
        The validated `pathlib.Path` object if it points to a directory.

    Raises:
        exception: If the path specified by `arg` is not a directory.

    """
    if not arg.is_dir():
        error_data = error_builder.data()
        raise exception(**error_data.to_exception())
    return arg


def is_read_ok[
    QuarryForgeError: base_exception.QuarryForgeError,
    ErrorBuilder: assembler.ErrorBuilder,
](
    *,
    arg: Path,
    exception: type[QuarryForgeError],
    error_builder: ErrorBuilder,
) -> Path:
    """Validate if the path specified has read permissions.

    Args:
        arg: The `pathlib.Path` object to check for read permissions.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        error_builder: The builder used to assemble data for an exception.

    Returns:
        The validated `pathlib.Path` object if it has read permissions.

    Raises:
        exception:
            If the path specified by `arg` does not have read permissions.

    """
    if not os.access(arg, os.R_OK):
        error_data = error_builder.data()
        raise exception(**error_data.to_exception())
    return arg


def is_write_ok[
    QuarryForgeError: base_exception.QuarryForgeError,
    ErrorBuilder: assembler.ErrorBuilder,
](
    *,
    arg: Path,
    exception: type[QuarryForgeError],
    error_builder: ErrorBuilder,
) -> Path:
    """Validate if the path specified has write permissions.

    For directories, this checks if files can be created in them.
    For files, this checks if the file itself can be written to.

    Args:
        arg: The `pathlib.Path` object to check for write permissions.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        error_builder: The builder used to assemble data for an exception.

    Returns:
        The validated `pathlib.Path` object if it has write permissions.

    Raises:
        exception:
            If the path specified by `arg` does not have write permissions.

    """
    if not os.access(arg, os.W_OK):
        error_data = error_builder.data()
        raise exception(**error_data.to_exception())
    return arg


def content_type_error_str_list[
    QuarryForgeError: base_exception.QuarryForgeError,
    ErrorBuilder: assembler.ErrorBuilder,
](
    *,
    arg: list[str] | None,
    exception: type[QuarryForgeError],
    error_builder: ErrorBuilder,
) -> list[str]:
    """Validate if all elements within the given list are strings.

    Args:
        arg: The list of items to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        error_builder: The builder used to assemble data for an exception.

    Returns:
        The validated list, guaranteed to contain only strings if successful.

    Raises:
        exception: If any element in `arg` is not a string.

    """
    valid = arg or []
    if not all(isinstance(item, str) for item in valid):
        error_data = error_builder.data()
        raise exception(**error_data.to_exception())
    return valid


def content_empty_error_str_list[
    QuarryForgeError: base_exception.QuarryForgeError,
    ErrorBuilder: assembler.ErrorBuilder,
](
    *,
    arg: list[str] | None,
    exception: type[QuarryForgeError],
    error_builder: ErrorBuilder,
) -> list[str]:
    """Validate if all string elements within the given list are not empty.

    This function checks if each string in the list is not empty after
    stripping leading and trailing whitespace. Assumes `args_list` contains
    only strings (e.g., after `content_type_error` validation).

    Args:
        arg: The list of strings to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        error_builder: The builder used to assemble data for an exception.

    Returns:
        The validated list of non-empty strings.

    Raises:
        exception: If any string in `args_list` is empty after stripping
            whitespace.

    """
    valid = arg or []
    if not all(item.strip() for item in valid):
        error_data = error_builder.data()
        raise exception(**error_data.to_exception())
    return valid


def content_type_error_str_tuple_list[
    QuarryForgeError: base_exception.QuarryForgeError,
    ErrorBuilder: assembler.ErrorBuilder,
](
    *,
    arg: list[tuple[str, str]] | None,
    exception: type[QuarryForgeError],
    error_builder: ErrorBuilder,
) -> list[tuple[str, str]]:
    """Validate elements within the given list are tuples of two strings.

    Args:
        arg: The list of items to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        error_builder: The builder used to assemble data for an exception.

    Returns:
        The validated list, guaranteed to contain only tuples of two strings.

    Raises:
        exception: If any element in `arg` is not a tuple of two strings.

    """
    valid_config = model_config.validation_config()
    valid = arg or []
    if not all(
        isinstance(item, tuple)
        and len(item) == valid_config.PAIR
        and isinstance(item[valid_config.KEY], str)
        and isinstance(item[valid_config.VALUE], str)
        for item in valid
    ):
        error_data = error_builder.data()
        raise exception(**error_data.to_exception())
    return valid


def content_empty_error_str_tuple_list[
    QuarryForgeError: base_exception.QuarryForgeError,
    ErrorBuilder: assembler.ErrorBuilder,
](
    *,
    arg: list[tuple[str, str]] | None,
    exception: type[QuarryForgeError],
    error_builder: ErrorBuilder,
) -> list[tuple[str, str]]:
    """Validate string elements in the given list of string-tuples.

    This function checks if each string within each tuple in the list is not
    empty after stripping leading and trailing whitespace.

    Args:
        arg:
            The list of string-tuples to check.
        exception:
            The specific type of QuarryForgeError to raise on validation
            failure.
        error_builder:
            The builder used to assemble data for an exception.

    Returns:
        The validated list of non-empty string-tuples.

    Raises:
        exception:
            If any string within any tuple in `arg` is empty after stripping
            whitespace.

    """
    valid = arg or []
    if not all(
        isinstance(element, str) and element.strip()
        for item in valid
        for element in item
    ):
        error_data = error_builder.data()
        raise exception(**error_data.to_exception())
    return valid
