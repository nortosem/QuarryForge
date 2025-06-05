"""Model Utility Module

This module provides utility functions for validating different types of
arguments used within the data models. It includes functions to check for
valid string types, non-empty strings, valid and existing paths (files and
directories), and readable/writable paths. It also includes functions for
validating list types and the content of lists based on specific error
conditions.
"""
from pathlib import Path
from typing import List, Optional, Tuple, Type, TypeVar

from quarryforge.config import model_config
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.config.exception_conf import model_exception_config as model_ec
from quarryforge.exception import base_exception
from quarryforge.util import validation_util


_ModelError = TypeVar('_ModelError', bound=base_exception.ModelError)


def viable_fossil_repo(
    file: Path | str,
    workdir: Path | str,
    is_new: bool,
    exception: Type[_ModelError]
) -> Tuple[Path, Path]:
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
        file:
            The path (Path object or string) to the Fossil repository.
        workdir:
            The path (Path object or string) to the working directory of the
            repository.
        is_new:
            If True, validates for creating a new repository.
            If False (default), validates an existing repository.

    Returns:
        The validated and resolved Path object.

    Raises:
        exception: With specific codes and messages for different failures.
    """
    # first check if string or path
    file = validation_util.is_type_path(
        arg=file,
        exception=exception,
        error_builder=model_ec.FossilRepoErrorBuilder(
            error_context=model_ec.FossilCommitPath.INIT,
            error_code=ec.GENERIC_ERROR.type_error,
            arg=file,
            field=model_config.FOSSIL_REPO._fields[0],
            info=str(type(file)),
        )
    )
    workdir = validation_util.is_type_path(
        arg=workdir,
        exception=exception,
        error_builder=model_ec.FossilRepoErrorBuilder(
            error_context=model_ec.FossilCommitPath.INIT,
            error_code=ec.GENERIC_ERROR.type_error,
            arg=workdir,
            field=model_config.FOSSIL_REPO._fields[2],
            info=str(type(workdir))
        )
    )
    # second ensure path object
    file = validation_util.resolve_path_arg(
        arg=file,
        exception=exception,
        error_builder=model_ec.FossilRepoErrorBuilder(
            error_context=model_ec.FossilCommitPath.INIT,
            error_code=ec.PATH_ERROR.resolution,
            arg=file,
            field=model_config.FOSSIL_REPO._fields[0],
            info=str(type(file)),
        )
    )
    workdir = validation_util.resolve_path_arg(
        arg=workdir,
        exception=exception,
        error_builder=model_ec.FossilRepoErrorBuilder(
            error_context=model_ec.FossilCommitPath.INIT,
            error_code=ec.PATH_ERROR.resolution,
            arg=workdir,
            field=model_config.FOSSIL_REPO._fields[2],
            info=str(type(workdir)),
        )
    )
    # third is_new or not?
    if is_new: # new is the target repo
        file = validation_util.not_exist(
            arg=file,
            exception=exception,
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.PATH_ERROR.existing,
                arg=file,
                field=model_config.FOSSIL_REPO._fields[0],
                info=str(type(file)),
                )
        )
        parent_dir = validation_util.exist(
            arg=file.parent,
            exception=exception,
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.PATH_ERROR.nonexistent,
                arg=file.parent,
                field=model_config.FOSSIL_REPO._fields[0],
                info=str(type(file.parent)),
                )
        )
        parent_dir = validation_util.is_dir(
            arg=file.parent,
            exception=exception,
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.PATH_ERROR.dir_error,
                arg=file.parent,
                field=model_config.FOSSIL_REPO._fields[0],
                info=str(type(file.parent)),
                )
        )
        parent_dir = validation_util.is_write_ok(
            arg=file.parent,
            exception=exception,
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.PATH_ERROR.unwritable,
                arg=file.parent,
                field=model_config.FOSSIL_REPO._fields[0],
                info=str(type(file.parent)),
                )
        )
        if parent_dir == workdir:
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.PATH_ERROR.same_dir,
                arg=file.parent,
                field=str(
                    f'{model_config.FOSSIL_REPO._fields[0]},'
                    f'{model_config.FOSSIL_REPO._fields[2]}'
                ),
                info=(
                    f'repo dir: {str(file.parent)}'
                    f'workdir: {str(workdir)}'
                ),
                extra_details={ec.DESC_MSG.reason: 'todo'}
            )
            error_data = error_builder.data()
            raise exception(**error_data.to_exception())
    # not new means source repo
    else:
        file = validation_util.exist(
            arg=file,
            exception=exception,
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.PATH_ERROR.nonexistent,
                field=model_config.FOSSIL_REPO._fields[0]
                )
        )
        file = validation_util.is_dir(
            arg=file,
            exception=exception,
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.PATH_ERROR.file_error,
                field=model_config.FOSSIL_REPO._fields[0]
                )
        )
        file = validation_util.is_read_ok(
            arg=file,
            exception=exception,
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.PATH_ERROR.unreadable,
                field=model_config.FOSSIL_REPO._fields[0]
                )
        )
    # validate the working directory
    workdir = validation_util.exist(
            arg=workdir,
            exception=exception,
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.PATH_ERROR.nonexistent,
                field=model_config.FOSSIL_REPO._fields[2]
                )
        )
    workdir = validation_util.is_dir(
        arg=workdir,
        exception=exception,
        error_builder=model_ec.FossilRepoErrorBuilder(
            error_context=model_ec.FossilCommitPath.INIT,
            error_code=ec.PATH_ERROR.dir_error,
            field=model_config.FOSSIL_REPO._fields[2]
        )
    )
    workdir = validation_util.is_write_ok(
        arg=workdir,
        exception=exception,
        error_builder=model_ec.FossilRepoErrorBuilder(
            error_context=model_ec.FossilCommitPath.INIT,
            error_code=ec.PATH_ERROR.unwritable,
            field=model_config.FOSSIL_REPO._fields[2]
        )
    )
    return file, workdir


def viable_fossil_commit(
    *,
    uuid: str,
    date: str,
    author: str,
    comment: str,
    branch: Optional[str] = None,
    tags: Optional[List[str]] = None,
    phase: Optional[str] = None,
    changes: Optional[List[str]] = None,
    exception: Type[_ModelError],
) -> Tuple[
    str,
    str,
    str,
    str,
    Optional[str],
    Optional[List[str]],
    Optional[str],
    Optional[List[str]],
]:
    """Validates the arguements fields for FossilCommit on Initialization."""
    uuid = validation_util.is_str_not_empty(
        arg=validation_util.is_type_str(
            arg=uuid,
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.GENERIC_ERROR.type_error,
                field=uuid
            )
        ),
        exception=exception,
        error_builder=model_ec.FossilCommitErrorBuilder(
            error_context=model_ec.FossilCommitPath.INIT,
            error_code=ec.STRING_ERROR.empty,
            field=uuid
        )
    )
    date = validation_util.is_str_not_empty(
        arg=validation_util.is_type_str(
            arg=date,
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.GENERIC_ERROR.type_error,
                field=date
            )
        ),
        exception=exception,
        error_builder=model_ec.FossilCommitErrorBuilder(
            error_context=model_ec.FossilCommitPath.INIT,
            error_code=ec.STRING_ERROR.empty,
            field=date
        )
    )
    author = validation_util.is_str_not_empty(
        arg=validation_util.is_type_str(
            arg=author,
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.GENERIC_ERROR.type_error,
                field=author
            )
        ),
        exception=exception,
        error_builder=model_ec.FossilCommitErrorBuilder(
            error_context=model_ec.FossilCommitPath.INIT,
            error_code=ec.STRING_ERROR.empty,
            field=author
        )
    )
    comment = validation_util.is_str_not_empty(
        arg=validation_util.is_type_str(
            arg=comment,
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.GENERIC_ERROR.type_error,
                field=comment
            )
        ),
        exception=exception,
        error_builder=model_ec.FossilCommitErrorBuilder(
            error_context=model_ec.FossilCommitPath.INIT,
            error_code=ec.STRING_ERROR.empty,
            field=comment
        )
    )
    if branch:
        branch = validation_util.is_str_not_empty(
            arg=validation_util.is_type_str(
                arg=branch,
                exception=exception,
                error_builder=model_ec.FossilCommitErrorBuilder(
                    error_context=model_ec.FossilCommitPath.INIT,
                    error_code=ec.GENERIC_ERROR.type_error,
                    field=branch
                )
            ),
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.STRING_ERROR.empty,
                field=branch
            )
        )
    if tags:
        tags = validation_util.content_empty_error(
            arg=validation_util.content_type_error(
                arg=tags,
                exception=exception,
                error_builder=model_ec.FossilCommitErrorBuilder(
                    error_context=model_ec.FossilCommitPath.INIT,
                    error_code=ec.GENERIC_ERROR.type_error,
                    field=f'{[tag for tag in tags]}'
                ),
            ),
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.STRING_ERROR.empty,
                field=f'{[tag for tag in tags]}'
            )
        )
    if phase:
        phase  = validation_util.is_str_not_empty(
            arg=validation_util.is_type_str(
                arg=phase,
                exception=exception,
                error_builder=model_ec.FossilCommitErrorBuilder(
                    error_context=model_ec.FossilCommitPath.INIT,
                    error_code=ec.GENERIC_ERROR.type_error,
                    field=phase
                )
            ),
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.STRING_ERROR.empty,
                field=phase
            )
        )
    if changes:
        changes = validation_util.content_empty_error(
            arg=validation_util.content_type_error(
                arg=changes,
                exception=exception,
                error_builder=model_ec.FossilCommitErrorBuilder(
                    error_context=model_ec.FossilCommitPath.INIT,
                    error_code=ec.GENERIC_ERROR.type_error,
                    field=f'{[change for change in changes]}'
                )
            ),
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.FossilCommitPath.INIT,
                error_code=ec.STRING_ERROR.empty,
                field=f'{[change for change in changes]}'
            )
        )
    return (uuid, date, author, comment, branch, tags, phase, changes)
