"""Validation Utility

This module provides a collection of utility functions for performing common
validation tasks, such as type checking, string emptiness checks, path
validations (existence, type, permissions), and list content validation.
These functions are designed to raise specific, configurable exceptions from
the `quarryforge.exception` hierarchy upon validation failure, providing
detailed error information.
"""
import os
from pathlib import Path
from typing import Any, List, Optional, Type, TypeVar

from quarryforge.config.exception_conf import exception_config as msg
from quarryforge.config.exception_conf import exception_data
#from quarryforge.config.exception_conf import model_exception_config
from quarryforge.exception import base_exception
from quarryforge.meta import assembler

_QFE = TypeVar('_QFE', bound=base_exception.QuarryForgeError)
_ERROR_BUILDER = TypeVar('_ERROR_BUILDER', bound=assembler.BuildError)


def is_type_str(
    *,
    arg: Any,
    exception: Type[_QFE],
    error_builder: Type[_ERROR_BUILDER]
) -> str:
    """Validates if the given argument is a string.

    Args:
        arg: The argument to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        context: Contextual information (e.g., 'ClassName.method_name')
            where the validation is performed.
        field: The name of the field or argument being validated.
        error_code: A specific error code for this validation failure.
        message: A developer-facing message for the exception.
        user_message (Optional[str]): A user-friendly message for the
            exception. Defaults to None.
        exception_code (Optional[str]): An optional code to associate with the
            exception. Defaults to None.

    Returns:
        The validated string argument if it is a string.

    Raises:
        exception: If the argument `arg` is not a string.
    """
    if not isinstance(arg, str):
        error_data = error_builder.data(
            input_value=arg,
            context=context,
            field=field,
            error_code=error_code,
            message=message,
            user_message=user_message,
            expected_desc=msg.DESC_TYPE.string,
            exception_code=exception_code
        )
        raise exception(**error_data.to_exception())
    return arg


def is_str_not_empty(
    *,
    arg: str,
    exception: Type[_QFE],
    context: str,
) -> str:
    """Validates if the given string argument is not empty.

    This function checks if the string is not empty after stripping leading
    and trailing whitespace.

    Args:
        arg: The string argument to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        context: Contextual information (e.g., 'ClassName.method_name')
            where the validation is performed.
        field: The name of the field or argument being validated.
        error_code: A specific error code for this validation failure.
        message: A developer-facing message for the exception.
        user_message (Optional[str]): A user-friendly message for the
            exception. Defaults to None.
        exception_code (Optional[str]): An optional code to associate with the
            exception. Defaults to None.

    Returns:
        The validated string argument if it is not empty.

    Raises:
        exception: If the argument `arg` is empty after stripping whitespace.
    """
    if not arg.strip():
        error_data = exception_data.error_builder(
            input_value=arg,
            context=context,
            field=field,
            error_code=error_code,
            message=message,
            user_message=user_message,
            expected_desc=msg.DESC_TYPE.empty,
            exception_code=exception_code
        )
        raise exception(**error_data.to_exception())
    return arg


def is_type_path(
    *,
    arg: Any,
    exception: Type[_QFE],
    context: str,
    field: str,
    error_code: str,
    message: str,
    user_message: Optional[str] = None,
    exception_code: Optional[str] = None
) -> Path:
    """Validates if the given argument is a pathlib.Path object.

    Args:
        arg: The argument to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        context: Contextual information (e.g., 'ClassName.method_name')
            where the validation is performed.
        field: The name of the field or argument being validated.
        error_code: A specific error code for this validation failure.
        message: A developer-facing message for the exception.
        user_message (Optional[str]): A user-friendly message for the
            exception. Defaults to None.
        exception_code (Optional[str]): An optional code to associate with the
            exception. Defaults to None.

    Returns:
        The validated Path object if `arg` is a `pathlib.Path`.

    Raises:
        exception: If the argument `arg` is not a `pathlib.Path` object.
    """
    if not isinstance(arg, Path):
        error_data = exception_data.error_builder(
            input_value=arg,
                context=context,
                field=field,
                error_code=error_code,
                message=message,
                user_message=user_message,
                expected_desc=msg.DESC_TYPE.path,
                exception_code=exception_code
            )
        raise exception(**error_data.to_exception())
    return arg


def resolve_path_arg(
    *,
    arg: Path,
    exception: Type[_QFE],
    context: str,
    field: str,
    error_code: str,
    message: str,
    user_message: Optional[str] = None,
    exception_code: Optional[str] = None
) -> Path:
    """Resolves a path argument to an absolute path, expanding uservars.

    Checks if the argument is a `pathlib.Path` object, then attempts to
    expand the user directory (e.g., '~') and resolve it to an absolute path.

    Args:
        arg: The path argument (expected to be a `pathlib.Path` object).
        exception: The specific type of QuarryForgeError to raise on
            validation or resolution failure.
        context: Contextual information (e.g., 'ClassName.method_name')
            where the validation is performed.
        field: The name of the field or argument being validated.
        error_code: A specific error code for this validation failure.
        message: A developer-facing message for the exception.
        user_message (Optional[str]): A user-friendly message for the
            exception. Defaults to None.
        exception_code (Optional[str]): An optional code to associate with the
            exception. Defaults to None.

    Returns:
        The resolved, absolute `pathlib.Path` object.

    Raises:
        exception: If `arg` is not a `pathlib.Path` object, or if path
            resolution fails due to `RuntimeError` (e.g., home directory
            cannot be determined) or `OSError` (e.g., permission issues,
            path does not exist and cannot be resolved).
    """
    if isinstance(arg, Path):
        try:
            return arg.expanduser().resolve()
        except RuntimeError as run_error:
            raise exception(exception_data.error_builder(
                input_value=arg,
                context=context,
                field=field,
                error_code=error_code,
                message=message,
                user_message=user_message,
                expected_desc=msg.DESC_TYPE.path,
                exception_code=exception_code
            ).to_exception()) from run_error
        except OSError as os_error:
            raise exception(exception_data.error_builder(
                input_value=arg,
                context=context,
                field=field,
                error_code=error_code,
                message=message,
                user_message=user_message,
                expected_desc=msg.DESC_TYPE.path,
                exception_code=exception_code
            ).to_exception()) from os_error

    error_data = exception_data.error_builder(
        input_value=arg,
        context=context,
        field=field,
        error_code=error_code,
        message=message,
        user_message=user_message,
        expected_desc=msg.DESC_TYPE.path,
        exception_code=exception_code
    )
    raise exception(**error_data.to_exception())


def exists(
    *,
    arg: Path,
    exception: Type[_QFE],
    context: str,
    field: str,
    error_code: str,
    message: str,
    user_message: Optional[str] = None,
    exception_code: Optional[str] = None
) -> Path:
    """Validates if the path specified exists.

    Args:
        arg: The `pathlib.Path` object to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        context: Contextual information (e.g., 'ClassName.method_name')
            where the validation is performed.
        field: The name of the field or argument being validated.
        error_code: A specific error code for this validation failure.
        message: A developer-facing message for the exception.
        user_message (Optional[str]): A user-friendly message for the
            exception. Defaults to None.
        exception_code (Optional[str]): An optional code to associate with the
            exception. Defaults to None.

    Returns:
        The validated `pathlib.Path` object if the path exists.

    Raises:
        exception: If the path specified by `arg` does not exist.
    """
    if not arg.exists():
        error_data = exception_data.error_builder(
            input_value=arg,
            context=context,
            field=field,
            error_code=error_code,
            message=message,
            user_message=user_message,
            expected_desc=msg.DESC_TYPE.exists,
            exception_code=exception_code
        )
        raise exception(**error_data.to_exception())
        #raise exception(message.PathMessage.does_not_exist(str(arg)))
    return arg


def is_file(
    *,
    arg: Path,
    exception: Type[_QFE],
    context: str,
    field: str,
    error_code: str,
    message: str,
    user_message: Optional[str] = None,
    exception_code: Optional[str] = None
) -> Path:
    """Validates if the path specified is a file.

    Assumes `arg` is already a `pathlib.Path` object and exists.
    It's recommended to call `exists(arg, ...)` before this function.

    Args:
        arg: The `pathlib.Path` object to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        context: Contextual information (e.g., 'ClassName.method_name')
            where the validation is performed.
        field: The name of the field or argument being validated.
        error_code: A specific error code for this validation failure.
        message: A developer-facing message for the exception.
        user_message (Optional[str]): A user-friendly message for the
            exception. Defaults to None.
        exception_code (Optional[str]): An optional code to associate with the
            exception. Defaults to None.

    Returns:
        The validated `pathlib.Path` object if it points to a file.

    Raises:
        exception: If the path specified by `arg` is not a file.
    """
    if not arg.is_file():
        error_data = exception_data.error_builder(
            input_value=arg,
            context=context,
            field=field,
            error_code=error_code,
            message=message,
            user_message=user_message,
            expected_desc=msg.DESC_TYPE.is_file,
            exception_code=exception_code
        )
        raise exception(**error_data.to_exception())
        #raise exception(message.PathMessage.not_a_file(path))
    return arg


def is_dir(
    *,
    arg: Path,
    exception: Type[_QFE],
    context: str,
    field: str,
    error_code: str,
    message: str,
    user_message: Optional[str] = None,
    exception_code: Optional[str] = None
) -> Path:
    """Validates if the path specified is a directory.

    Assumes `arg` is already a `pathlib.Path` object and exists.
    It's recommended to call `exists(arg, ...)` before this function.

    Args:
        arg: The `pathlib.Path` object to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        context: Contextual information (e.g., 'ClassName.method_name')
            where the validation is performed.
        field: The name of the field or argument being validated.
        error_code: A specific error code for this validation failure.
        message: A developer-facing message for the exception.
        user_message (Optional[str]): A user-friendly message for the
            exception. Defaults to None.
        exception_code (Optional[str]): An optional code to associate with the
            exception. Defaults to None.

    Returns:
        The validated `pathlib.Path` object if it points to a directory.

    Raises:
        exception: If the path specified by `arg` is not a directory.
    """
    if not arg.is_dir():
        error_data = exception_data.error_builder(
            input_value=arg,
            context=context,
            field=field,
            error_code=error_code,
            message=message,
            user_message=user_message,
            expected_desc=msg.DESC_TYPE.is_dir,
            exception_code=exception_code
        )
        raise exception(**error_data.to_exception())
        #raise exception(message.PathMessage.not_a_directory(str(arg)))
    return arg


def is_read_ok(
    *,
    arg: Path,
    exception: Type[_QFE],
    context: str,
    field: str,
    error_code: str,
    message: str,
    user_message: Optional[str] = None,
    exception_code: Optional[str] = None
) -> Path:
    """Validates if the path specified has read permissions.

    Args:
        arg: The `pathlib.Path` object to check for read permissions.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        context: Contextual information (e.g., 'ClassName.method_name')
            where the validation is performed.
        field: The name of the field or argument being validated.
        error_code: A specific error code for this validation failure.
        message: A developer-facing message for the exception.
        user_message (Optional[str]): A user-friendly message for the
            exception. Defaults to None.
        exception_code (Optional[str]): An optional code to associate with the
            exception. Defaults to None.

    Returns:
        The validated `pathlib.Path` object if it has read permissions.

    Raises:
        exception:
            If the path specified by `arg` does not have read permissions.
    """
    if not os.access(arg, os.R_OK):
        error_data = exception_data.error_builder(
            input_value=arg,
            context=context,
            field=field,
            error_code=error_code,
            message=message,
            user_message=user_message,
            expected_desc=msg.DESC_TYPE.is_readable,
            exception_code=exception_code
        )
        raise exception(**error_data.to_exception())
        #raise exception(message.PathMessage.no_read_permission(str(arg)))
    return arg


def is_write_ok(
    *,
    arg: Path,
    exception: Type[_QFE],
    context: str,
    field: str,
    error_code: str,
    message: str,
    user_message: Optional[str] = None,
    exception_code: Optional[str] = None
) -> Path:
    """Validates if the path specified has write permissions.

    For directories, this checks if files can be created in them.
    For files, this checks if the file itself can be written to.

    Args:
        arg: The `pathlib.Path` object to check for write permissions.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        context: Contextual information (e.g., 'ClassName.method_name')
            where the validation is performed.
        field: The name of the field or argument being validated.
        error_code: A specific error code for this validation failure.
        message: A developer-facing message for the exception.
        user_message (Optional[str]): A user-friendly message for the
            exception. Defaults to None.
        exception_code (Optional[str]): An optional code to associate with the
            exception. Defaults to None.

    Returns:
        The validated `pathlib.Path` object if it has write permissions.

    Raises:
        exception:
            If the path specified by `arg` does not have write permissions.
    """
    if not os.access(arg, os.W_OK):
        error_data = exception_data.error_builder(
            input_value=arg,
            context=context,
            field=field,
            error_code=error_code,
            message=message,
            user_message=user_message,
            expected_desc=msg.DESC_TYPE.is_writable,
            exception_code=exception_code
        )
        raise exception(**error_data.to_exception())
        #raise exception(message.PathMessage.no_write_permission(str(arg)))
    return arg


def check_list_type(
    *,
    arg: Any,
    exception: Type[_QFE],
    context: str,
    field: str,
    error_code: str,
    message: str,
    user_message: Optional[str] = None,
    exception_code: Optional[str] = None
) -> List:
    """Validates if the given argument is a list, or None.

    Args:
        arg: The argument to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        context: Contextual information (e.g., 'ClassName.method_name')
            where the validation is performed.
        field: The name of the field or argument being validated.
        error_code: A specific error code for this validation failure.
        message: A developer-facing message for the exception.
        user_message (Optional[str]): A user-friendly message for the
            exception. Defaults to None.
        exception_code (Optional[str]): An optional code to associate with the
            exception. Defaults to None.

    Returns:
        The validated list argument if `arg` is a list. Returns an empty list
        if `arg` is None.

    Raises:
        exception: If the argument `arg` is not a list and not None.
    """
    final_list: List = []
    if arg is not None:
        if not isinstance(arg, list):
            error_data = exception_data.error_builder(
                input_value=arg,
                context=context,
                field=field,
                error_code=error_code,
                message=message,
                user_message=user_message,
                expected_desc=msg.DESC_TYPE.is_list,
                exception_code=exception_code
            )
            raise exception(**error_data.to_exception())
        final_list = arg
    return final_list


def content_type_error(
    *,
    arg_list: List[Any],
    exception: Type[_QFE],
    context: str,
    field: str,
    error_code: str,
    message: str,
    user_message: Optional[str] = None,
    exception_code: Optional[str] = None
) -> List[str]:
    """Validates if all elements within the given list are strings.

    Args:
        arg_list: The list of items to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        context: Contextual information (e.g., 'ClassName.method_name')
            where the validation is performed.
        field: The name of the field or argument being validated (referring
            to the list itself or its conceptual content).
        error_code: A specific error code for this validation failure.
        message: A developer-facing message for the exception.
        user_message (Optional[str]): A user-friendly message for the
            exception. Defaults to None.
        exception_code (Optional[str]): An optional code to associate with the
            exception. Defaults to None.

    Returns:
        The validated list, guaranteed to contain only strings if successful.
        The type hint `List[str]` implies this, but the check ensures it.

    Raises:
        exception: If any element in `arg_list` is not a string.
    """
    for item in arg_list:
        if not isinstance(item, str):
            error_data = exception_data.error_builder(
                input_value=item,
                context=context,
                field=f"{field} list item",
                error_code=error_code,
                message=message,
                user_message=user_message,
                expected_desc=msg.DESC_TYPE.string_list_content,
                exception_code=exception_code
            )
            raise exception(**error_data.to_exception())
    return arg_list


def content_empty_error(
    args_list: List[str],
    exception: Type[_QFE],
    context: str,
    field: str,
    error_code: str,
    message: str,
    user_message: Optional[str] = None,
    exception_code: Optional[str] = None
) -> List[str]:
    """Validates if all string elements within the given list are not empty.

    This function checks if each string in the list is not empty after
    stripping leading and trailing whitespace. Assumes `args_list` contains
    only strings (e.g., after `content_type_error` validation).

    Args:
        args_list: The list of strings to check.
        exception: The specific type of QuarryForgeError to raise on
            validation failure.
        context: Contextual information (e.g., 'ClassName.method_name')
            where the validation is performed.
        field: The name of the field or argument being validated (referring
            to the list itself or its conceptual content).
        error_code: A specific error code for this validation failure.
        message: A developer-facing message for the exception.
        user_message (Optional[str]): A user-friendly message for the
            exception. Defaults to None.
        exception_code (Optional[str]): An optional code to associate with the
            exception. Defaults to None.

    Returns:
        The validated list of non-empty strings.

    Raises:
        exception: If any string in `args_list` is empty after stripping
            whitespace.
    """
    for item in args_list:
        if not item.strip():
            error_data = exception_data.error_builder(
                input_value=item,
                context=context,
                field=f"{field} list item",
                error_code=error_code,
                message=message,
                user_message=user_message,
                expected_desc=msg.DESC_TYPE.non_empty_list_content,
                exception_code=exception_code
            )
            raise exception(**error_data.to_exception())
    return args_list
