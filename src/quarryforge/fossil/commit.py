"""Provides methods for check-ins to a Fossil repository check-out."""

import subprocess
from pathlib import Path

from quarryforge.config import fossil_config as _
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.config.exception_conf import exception_data as e_data
from quarryforge.config.exception_conf import (
    fossil_exception_config as fossil_ec,
)
from quarryforge.exception import fossil_exception
from quarryforge.util import fossil_util


def commit_changes(
    date_override: str,
    user_override: str,
    comment: str,
    branch: str | None,
    tag: str | None,
    files: list[Path] | None,
) -> str:
    """Commit changes to the Fossil repository.

    Args:
        date_override (str): The date string to override the commit date.
        user_override (str): The username to override the committer.
        comment (str): The commit message.
        branch (Optional[str]): The branch name for the commit.
        tag (Optional[str]): A tag to apply to the commit.
        files (Optional[List[Path]]):
            A list of `Path` objects for specific files to commit. If None,
            all pending changes are committed.

    Returns:
        str: The stdout from the fossil commit command.

    Raises:
        fossil_exception.FossilProcessError:
            If the Fossil command fails.
        fossil_exception.FossilTimeoutError:
            If the Fossil command times out.
        fossil_exception.FossilCommitError:
            If an issue occurs during the commit operation.

    """
    try:
        ci_process: subprocess.CompletedProcess[bytes] = subprocess.run(
            fossil_util.commit(
                date_override, user_override, comment, branch, tag, files or []
            ),
            capture_output=True,
            check=True,
            timeout=int(_.Fossil.DEFAULT_TIMEOUT),
        )
        return ci_process.stdout.decode()
    except subprocess.CalledProcessError as error:
        process_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
            error_code=_.Fossil.PROCESS_ERROR,
            arg=f'commit for {comment[:50]}...',
            extra_details={
                _.Fossil.CMD: error.cmd,
                _.Fossil.RETURN_CODE: error.returncode,
                _.Fossil.OUTPUT: error.stdout,
                _.Fossil.STDERR: error.stderr,
            },
        )
        raise fossil_exception.FossilProcessError(
            **process_builder.data().to_exception()
        ) from error
    except subprocess.TimeoutExpired as error:
        timeout_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMEOUT,
            error_code=_.Fossil.TIMEOUT_ERROR,
            arg=f'commit for {comment[:50]}...',
            info=str(error),
            extra_details={
                _.Fossil.ARGS: error.args,
                _.Fossil.CMD: error.cmd,
                _.Fossil.TIMEOUT: error.timeout,
                _.Fossil.OUTPUT: error.stdout,
                _.Fossil.STDERR: error.stderr,
            },
        )
        raise fossil_exception.FossilTimeoutError(
            **timeout_builder.data().to_exception()
        ) from error
