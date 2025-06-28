"""Model Utility module provides functions for validating data model arguments.

It includes functions to check for valid string types, non-empty strings, valid
and existing paths (files and directories), and readable/writable paths. It
also includes functions for validating list types and the content of lists
based on specific error conditions.
"""

from pathlib import Path

from quarryforge.config import model_config
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.config.exception_conf import model_exception_config as model_ec
from quarryforge.exception import base_exception
from quarryforge.util import validation_util


def viable_fossil_repo[
        ModelError: base_exception.ModelError
](
    file: Path | str,
    workdir: Path | str,
    is_new: bool,
    exception: type[ModelError],
) -> tuple[Path, Path]:
    """Validate if the path points to a viable Fossil repository.

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
        exception:
            The specific type of ModelError exception to raise on error.

    Returns:
        The validated and resolved Path object.

    Raises:
        exception: With specific codes and messages for different failures.

    """
    fossil_repo_config = model_config.fossil_repo_config()

    # first check if string or path
    file = validation_util.is_type_path(
        arg=file,
        exception=exception,
        error_builder=model_ec.FossilRepoErrorBuilder(
            error_context=model_ec.ModelErrorPath.FOSSIL_REPO_INIT,
            error_code=ec.GenericError.TYPE_ERROR,
            arg=file,
            field=fossil_repo_config.file,
            info=f'arg: {file} type: {type(file)}',
        ),
    )
    workdir = validation_util.is_type_path(
        arg=workdir,
        exception=exception,
        error_builder=model_ec.FossilRepoErrorBuilder(
            error_context=model_ec.ModelErrorPath.FOSSIL_REPO_INIT,
            error_code=ec.GenericError.TYPE_ERROR,
            arg=workdir,
            field=fossil_repo_config.workdir,
            info=f'arg: {workdir} type: {type(workdir)}',
        ),
    )
    # second ensure path object
    file = validation_util.resolve_path_arg(
        arg=file,
        exception=exception,
        error_builder=model_ec.FossilRepoErrorBuilder(
            error_context=model_ec.ModelErrorPath.FOSSIL_REPO_INIT,
            error_code=ec.PathError.PATH_RESOLUTION_ERROR,
            arg=file,
            field=fossil_repo_config.file,
            info=f'arg: {file} type: {type(file)}',
        ),
    )
    workdir = validation_util.resolve_path_arg(
        arg=workdir,
        exception=exception,
        error_builder=model_ec.FossilRepoErrorBuilder(
            error_context=model_ec.ModelErrorPath.FOSSIL_REPO_INIT,
            error_code=ec.PathError.PATH_RESOLUTION_ERROR,
            arg=workdir,
            field=fossil_repo_config.workdir,
            info=f'arg: {workdir} type: {type(workdir)}',
        ),
    )
    # third is_new or not?
    if is_new:  # new is the target repo
        file = validation_util.not_exist(
            arg=file,
            exception=exception,
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_REPO_INIT,
                error_code=ec.PathError.PATH_EXISTING_ERROR,
                arg=file,
                field=fossil_repo_config.file,
                info=f'arg: {file} type: {type(file)}',
            ),
        )
        parent_dir = validation_util.exist(
            arg=file.parent,
            exception=exception,
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_REPO_INIT,
                error_code=ec.PathError.PATH_NONEXISTENT_ERROR,
                arg=file.parent,
                field=fossil_repo_config.file,
                info=f'arg: {file.parent} type: {type(file.parent)}',
            ),
        )
        parent_dir = validation_util.is_dir(
            arg=file.parent,
            exception=exception,
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_REPO_INIT,
                error_code=ec.PathError.PATH_NOT_A_DIRECTORY_ERROR,
                arg=file.parent,
                field=fossil_repo_config.file,
                info=f'arg: {file.parent} type: {type(file.parent)}',
            ),
        )
        parent_dir = validation_util.is_write_ok(
            arg=file.parent,
            exception=exception,
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_REPO_INIT,
                error_code=ec.PathError.PATH_NOT_WRITABLE_ERROR,
                arg=file.parent,
                field=fossil_repo_config.file,
                info=f'arg: {file.parent} type: {type(file.parent)}',
            ),
        )
        if parent_dir == workdir:
            error_builder = model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_REPO_INIT,
                error_code=ec.PathError.SAME_REPO_DIR_AND_WORK_DIR,
                arg=file.parent,
                field=str(
                    f'{fossil_repo_config.file},{fossil_repo_config.workdir}'
                ),
                info=(f'repo dir: {str(file.parent)}workdir: {str(workdir)}'),
                extra_details={
                    ec.DescMsg.REASON: (
                        "The repository file's parent directory cannot be the "
                        'same as the working directory to prevent checkout '
                        'conflicts.'
                    )
                },
            )
            error_data = error_builder.data()
            raise exception(**error_data.to_exception())
    # not new means source repo
    else:
        file = validation_util.exist(
            arg=file,
            exception=exception,
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_REPO_INIT,
                error_code=ec.PathError.PATH_NONEXISTENT_ERROR,
                field=fossil_repo_config.file,
                info=f'arg: {file} type: {type(file)}',
            ),
        )
        file = validation_util.is_file(
            arg=file,
            exception=exception,
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_REPO_INIT,
                error_code=ec.PathError.PATH_NOT_A_FILE_ERROR,
                field=fossil_repo_config.file,
                info=f'arg: {file} type: {type(file)}',
            ),
        )
        file = validation_util.is_read_ok(
            arg=file,
            exception=exception,
            error_builder=model_ec.FossilRepoErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_REPO_INIT,
                error_code=ec.PathError.PATH_NOT_READABLE_ERROR,
                field=fossil_repo_config.file,
                info=f'arg: {file} type: {type(file)}',
            ),
        )
    # validate the working directory
    workdir = validation_util.exist(
        arg=workdir,
        exception=exception,
        error_builder=model_ec.FossilRepoErrorBuilder(
            error_context=model_ec.ModelErrorPath.FOSSIL_REPO_INIT,
            error_code=ec.PathError.PATH_NONEXISTENT_ERROR,
            field=fossil_repo_config.workdir,
            info=f'arg: {workdir} type: {type(workdir)}',
        ),
    )
    workdir = validation_util.is_dir(
        arg=workdir,
        exception=exception,
        error_builder=model_ec.FossilRepoErrorBuilder(
            error_context=model_ec.ModelErrorPath.FOSSIL_REPO_INIT,
            error_code=ec.PathError.PATH_NOT_A_DIRECTORY_ERROR,
            field=fossil_repo_config.workdir,
            info=f'arg: {workdir} type: {type(workdir)}',
        ),
    )
    workdir = validation_util.is_write_ok(
        arg=workdir,
        exception=exception,
        error_builder=model_ec.FossilRepoErrorBuilder(
            error_context=model_ec.ModelErrorPath.FOSSIL_REPO_INIT,
            error_code=ec.PathError.PATH_NOT_WRITABLE_ERROR,
            field=fossil_repo_config.workdir,
            info=f'arg: {workdir} type: {type(workdir)}',
        ),
    )
    return file, workdir


def viable_fossil_commit[
        ModelError: base_exception.ModelError
](
    *,
    uuid: str,
    date: str,
    author: str,
    comment: str,
    branch: str | None = None,
    tags: list[str] | None = None,
    phase: list[str] | None = None,
    changes: list[tuple[str, str]] | None = None,
    exception: type[ModelError],
) -> tuple[
    str,
    str,
    str,
    str,
    str | None,
    list[str] | None,
    list[str] | None,
    list[tuple[str, str]] | None,
]:
    """Validate the arguements fields for FossilCommit on Initialization."""
    fossil_commit_config = model_config.fossil_commit_config()

    uuid = validation_util.is_str_not_empty(
        arg=validation_util.is_type_str(
            arg=uuid,
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                error_code=ec.GenericError.TYPE_ERROR,
                field=fossil_commit_config.uuid,
                info=f'arg: {uuid} type: {type(uuid)}',
            ),
        ),
        exception=exception,
        error_builder=model_ec.FossilCommitErrorBuilder(
            error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
            error_code=ec.StringError.EMPTY_STRING_ERROR,
            field=fossil_commit_config.uuid,
            info=f'arg: {uuid} type: {type(uuid)}',
        ),
    )
    date = validation_util.is_str_not_empty(
        arg=validation_util.is_type_str(
            arg=date,
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                error_code=ec.GenericError.TYPE_ERROR,
                field=fossil_commit_config.date,
                info=f'arg: {date} type: {type(date)}',
            ),
        ),
        exception=exception,
        error_builder=model_ec.FossilCommitErrorBuilder(
            error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
            error_code=ec.StringError.EMPTY_STRING_ERROR,
            field=fossil_commit_config.date,
            info=f'arg: {date} type: {type(date)}',
        ),
    )
    author = validation_util.is_str_not_empty(
        arg=validation_util.is_type_str(
            arg=author,
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                error_code=ec.GenericError.TYPE_ERROR,
                field=fossil_commit_config.author,
                info=f'arg: {author} type: {type(author)}',
            ),
        ),
        exception=exception,
        error_builder=model_ec.FossilCommitErrorBuilder(
            error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
            error_code=ec.StringError.EMPTY_STRING_ERROR,
            field=fossil_commit_config.author,
            info=f'arg: {author} type: {type(author)}',
        ),
    )
    comment = validation_util.is_str_not_empty(
        arg=validation_util.is_type_str(
            arg=comment,
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                error_code=ec.GenericError.TYPE_ERROR,
                field=fossil_commit_config.comment,
                info=f'arg: {comment} type: {type(comment)}',
            ),
        ),
        exception=exception,
        error_builder=model_ec.FossilCommitErrorBuilder(
            error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
            error_code=ec.StringError.EMPTY_STRING_ERROR,
            field=fossil_commit_config.comment,
            info=f'arg: {comment} type: {type(comment)}',
        ),
    )
    if branch:
        branch = validation_util.is_str_not_empty(
            arg=validation_util.is_type_str(
                arg=branch,
                exception=exception,
                error_builder=model_ec.FossilCommitErrorBuilder(
                    error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                    error_code=ec.GenericError.TYPE_ERROR,
                    field=fossil_commit_config.branch,
                    info=f'arg: {branch} type: {type(branch)}',
                ),
            ),
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                error_code=ec.StringError.EMPTY_STRING_ERROR,
                field=fossil_commit_config.branch,
                info=f'arg: {branch} type: {type(branch)}',
            ),
        )
    if tags:
        tags = validation_util.content_empty_error_str_list(
            arg=validation_util.content_type_error_str_list(
                arg=tags,
                exception=exception,
                error_builder=model_ec.FossilCommitErrorBuilder(
                    error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                    error_code=ec.GenericError.TYPE_ERROR,
                    field=fossil_commit_config.tags,
                    info=(
                        f'arg: {tags}, element_types: '
                        f'{[type(t).__name__ for t in tags if tags]}'
                    ),
                ),
            ),
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                error_code=ec.StringError.EMPTY_STRING_ERROR,
                field=fossil_commit_config.tags,
                info=f'arg: {tags}',
            ),
        )
    if phase:
        phase = validation_util.content_empty_error_str_list(
            arg=validation_util.content_type_error_str_list(
                arg=phase,
                exception=exception,
                error_builder=model_ec.FossilCommitErrorBuilder(
                    error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                    error_code=ec.GenericError.TYPE_ERROR,
                    field=fossil_commit_config.phase,
                    info=(
                        f'arg: {phase}, element_types: '
                        f'{[type(p).__name__ for p in phase if phase]}'
                    ),
                ),
            ),
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                error_code=ec.StringError.EMPTY_STRING_ERROR,
                field=fossil_commit_config.phase,
                info=f'arg: {phase}',
            ),
        )
    if changes:
        changes = validation_util.content_empty_error_str_tuple_list(
            arg=validation_util.content_type_error_str_tuple_list(
                arg=changes,
                exception=exception,
                error_builder=model_ec.FossilCommitErrorBuilder(
                    error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                    error_code=ec.GenericError.TYPE_ERROR,
                    field=fossil_commit_config.changes,
                    info=(
                        f'arg: {changes}, content_types: '
                        f'{
                            [
                                str(tuple(type(i).__name__ for i in c))
                                if isinstance(c, tuple)
                                else type(c).__name__
                                for c in changes
                            ]
                        }'
                    ),
                ),
            ),
            exception=exception,
            error_builder=model_ec.FossilCommitErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                error_code=ec.StringError.EMPTY_STRING_ERROR,
                field=fossil_commit_config.changes,
                info=f'arg: {changes}',
            ),
        )
    return (uuid, date, author, comment, branch, tags, phase, changes)
