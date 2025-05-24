"""Model Utility Module

This module provides utility functions for validating different types of
arguments used within the data models. It includes functions to check for
valid string types, non-empty strings, valid and existing paths (files and
directories), and readable/writable paths. It also includes functions for
validating list types and the content of lists based on specific error
conditions.
"""
import os
from pathlib import Path
from typing import List, TypeVar

from quarryforge.config import model_config
from quarryforge.config.exception_conf import exception_config
from quarryforge.config.exception_conf import model_exception_config as config
from quarryforge.exception import base_exception
from quarryforge.exception import model_exception
from quarryforge.util import model_error_util as error
from quarryforge.util import validation_util

_ModelError = TypeVar('_ModelError', bound=base_exception.ModelError)


def viable_fossil_repo(
    self,
    file: Path | str,
    is_new: bool,
    exception: Type[_ModelError]
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
    file_path = validation_util.is_type_str(
        arg=file,
        exception=exception,
        error_builder=FossilRepoErrorBuilder(
            error_context=config.FossilRepoContext.init,
            error_code=exception_config.type_error,
            input_value=file
        )
    )
    file_path = validation_util.is_str_not_empty(
        arg=file,
        exception=exception,
        context=config.FossilRepoContext.init,
        error_code=exception_config.StringErrorType.empty,
        message=config.FossilRepoMessage.empty_str_msg(arg),
        user_message=config.FossilRepoMessage.empty_str_usr_msg,
        exception_code=config.FossilRepoCode.exception_code(
            msg.ERROR_TYPE.type_error
        )
    )
    file_path = validation_util.is_type_path(
        arg=file,
        exception=exception,
        context=,
        field=model_config.FOSSIL_REPO.field_name,
        error_code=msg.ERROR_TYPE.empty_string,
        message=,
        user_message=,
        exception_code=
    )
    file_path = validation_util.resolve_path_arg(
        arg=file,
        exception=exception,
        context=,
        field=model_config.FOSSIL_REPO.field_name,
        error_code=msg.ERROR_TYPE.empty_string,
        message=,
        user_message=,
        exception_code=
    )

    if is_new:
        if not file_path.exists():
            if file_path.parent.exists():
                file_path = validation_util.is_write_ok(
                    arg=file_path,
                    exception=exception,
                    context=,
                    field=model_config.FOSSIL_REPO.field_name,
                    error_code=msg.ERROR_TYPE.empty_string,
                    message=,
                    user_message=,
                    exception_code=
                )
            else:
                error_data = {}
        else:
            error_data = {}
    file_path = validation_util.is_file()
    file_path = validation_util.is_read_ok()
    #TODO fossil repo file type check

    return file_path


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
