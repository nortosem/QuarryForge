"""Model Utility MOdule

#TODO
# fossil file validation TODO
"""
import os
from pathlib import Path
from typing import List

from quarryforge.config.exception_conf import PathMessage
from quarryforge.exceptions.model_exception.base_models_exception \
    import ModelError
from quarryforge.exceptions.model_exception import commit_exception


def is_valid_str_type(arg: str, exception: type[ModelError]) -> str:
    """Validate String Arg

    Returns a valid string argument type or raises an error.

    Args:
        arg (str): The string argument to check.
        exception (Exception): The specific type of exception to raise.

    Returns:
        attribute (str): Returns a valid string attribute.
    """
    attribute = arg
    if not isinstance(attribute, str):
        raise exception()
    return attribute


def is_not_empty(arg: str, exception: type[ModelError]) -> str:
    """Is Not Empty String

    Validate the given argument is not an empty string.

    Args:
        arg (str): The string argument to check.

    Returns:
        attribute (str): Returns a valid string attribute.
    """
    attribute = arg
    if not attribute.strip():
        raise exception()
    return attribute


def is_valid_path_type(arg: Path, exception: type[ModelError]) -> Path:
    """Valid Path Type

    Returns a valid path argument type or raises an error.

    Args:
        arg (Path): The repo path argument to check.
        exception (Exception): The specific type of exception to raise.

    Returns:
        path (Path): Returns a valid path path attribute.
    """
    path = arg
    if not isinstance(path, Path):
        raise exception()
    return path


def exists(arg: Path, exception: type[ModelError]) -> Path:
    """Verify the path exists

    Assumes Path already is a pathlib.Path.

    Args:
        arg (Path): The repo path argument to check.
        exception (Exception): The specific type of exception to raise.

    Returns:
        path (Path): Returns a valid path path attribute.
    """
    path = arg
    if not path.exists():
        raise exception(PathMessage.does_not_exist(path))
    return path


def is_file(arg: Path, exception: type[ModelError]) -> Path:
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


def viable_infile(arg: Path, exception: type[ModelError]) -> Path:
    """Viable Input Filename


    """
    path = arg
    path = exists(path, exception)
    path = is_file(path, exception)
    path = is_read_ok(path, exception)
    return path


def is_dir(arg: Path, exception: type[ModelError]) -> Path:
    """Verify the path is a directory

    Assumes Path already is a pathlib.Path.

    Args:
        arg (Path): The repo path argument to check.
        exception (Exception): The specific type of exception to raise.

    Returns:
        path (Path): Returns a valid path path attribute.
    """
    path = arg
    if not path.is_dir():
        raise exception(PathMessage.not_a_directory(path))
    return path


def is_read_ok(arg: Path, exception: type[ModelError]) -> Path:
    """Verify the path is ok to read

    Assumes Path already is a pathlib.Path.

    Args:
        arg (Path): The repo path argument to check.
        exception (Exception): The specific type of exception to raise.

    Returns:
        path (Path): Returns a valid path path attribute.
    """
    path = arg
    if not os.access(path, os.R_OK):
        raise exception(PathMessage.no_read_permission(path))
    return path


def is_write_ok(arg: Path, exception: type[ModelError]) -> Path:
    """Verify the path is ok to write

    Assumes Path already is a pathlib.Path.

    Args:
        arg (Path): The repo path argument to check.
        exception (Exception): The specific type of exception to raise.

    Returns:
        path (Path): Returns a valid path path attribute.
    """
    path = arg
    if not os.acces(path, os.W_OK):
        raise exception(PathMessage.no_write_permission(path))
    return path


def viable_source(arg: Path, exception: type[ModelError]) -> Path:
    """Viable Source Check

    Args:
        arg (Path): The repo path argument to check.
        exception (Exception): The specific type of exception to raise.

    Returns:
        path (Path): Returns a valid path path attribute.
    """
    path = arg
    path = exists(path, exception)
    path = is_file(path, exception)
    path = is_read_ok(path, exception)
    return path


def viable_output(arg: Path, exception: type[ModelError]) -> Path:
    """Viable Output Check

    Args:
        arg (Path): The repo path argument to check.
        exception (Exception): The specific type of exception to raise.

    Returns:
        path (Path): Returns a valid path path attribute.
    """
    path = arg
    path = exists(path, exception)
    path = is_file(path, exception)
    path = is_write_ok(path, exception)
    return path


def viable_update_dir(arg: Path, exception: type[ModelError]) -> Path:
    """Viable Project Update Directory Check

    Args:
        arg (Path): The repo path argument to check.
        exception (Exception): The specific type of exception to raise.

    Returns:
        path (Path): Returns a valid path path attribute.
    """
    path = arg
    path = exists(path, exception)
    path = is_dir(path, exception)
    path = is_write_ok(path, exception)
    return path


def check_list_type(arg: List, exception: type[ModelError]) -> List:
    """Check list arguments for a Commit are valid

    Returns a valid List argument type or raises an error.

    Args:
        arg (List): The string argument to check.
        exception (Exception): The specific type of exception to raise.

    Returns:
        attribute (List): Returns a valid List attribute.
    """
    final_list = []
    if arg is not None:
        if not isinstance(arg, list):
            raise exception()
        final_list = arg
    return final_list


def content_type_error(args: List, exception: type[ModelError]) -> str:
    """content_type_error"""
    items = args
    for item in items:
        if not isinstance(item, str):
            raise exception()

    return items


def content_empty_error(args: List, exception: type[ModelError]) -> str:
    """content_empty_error"""
    items = args
    for item in items:
        if not item.strip():
            raise exception()

    return items


def check_list_content(arg: List[str], exception: type[ModelError]) -> List:
    """Check contents of list for valid elements
    Returns a valid List argument type or raises an error.

    Args:
        arg (List): The string argument to check.
        exception (Exception): The specific type of exception to raise.

    Returns:
        attribute (List): Returns a valid List attribute.
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
