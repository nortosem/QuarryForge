"""Methods for querying changes between commits with `fossil diff`."""

import subprocess

from quarryforge import model
from quarryforge.config import fossil_config as _
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.config.exception_conf import exception_data as e_data
from quarryforge.config.exception_conf import (
    fossil_exception_config as fossil_ec,
)
from quarryforge.exception import fossil_exception
from quarryforge.util import fossil_util


def changes(from_arg: str, to_arg: str, source: model.FossilRepo) -> str:
    """Get all files changed on a commit from the source repo.

    Executes the Fossil 'diff --brief' command to get a summary of changes
    between two check-ins.

    Args:
        from_arg (str): The starting check-in hash or alias.
        to_arg (str): The ending check-in hash or alias.
        source (model.FossilRepo): The repository to perform the diff on.

    Returns:
        str: The raw output string containing the file changes.

    Raises:
        fossil_exception.FossilProcessError:
            If the Fossil command fails.
        fossil_exception.FossilTimeoutError:
            If the Fossil command times out.
        fossil_exception.FossilDiffError:
            If an issue occurs during the diff operation.

    """
    try:
        diff_process: subprocess.CompletedProcess[bytes] = subprocess.run(
            fossil_util.get_file_changes(from_arg, to_arg, source),
            cwd=source.workdir,
            capture_output=True,
            check=True,
            timeout=int(_.Fossil.DEFAULT_TIMEOUT),
        )
    except subprocess.CalledProcessError as error:
        process_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
            error_code=_.Fossil.PROCESS_ERROR,
            arg=f'{from_arg} to {to_arg} in {str(source)}',
            extra_details={
                _.Fossil.CMD: error.cmd,
                _.Fossil.RETURN_CODE: error.returncode,
                _.Fossil.OUTPUT: error.stdout,
                _.Fossil.STDERR: error.stderr,
            },
        )
        process_data = process_builder.data()
        process_error = fossil_exception.FossilProcessError(
            **process_data.to_exception()
        )
        diff_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_DIFF,
            error_code=ec.GenericError.EXTERNAL_DEPENDENCY_ERROR,
            arg=f'{from_arg} to {to_arg} in {str(source)}',
            extra_details={
                ec.DescMsg.DEPENDENCY: process_error.details[_.Fossil.CMD],
                ec.DescMsg.REASON: process_error.details[_.Fossil.STDERR],
            },
        )
        diff_data = diff_builder.data()
        raise fossil_exception.FossilDiffError(
            **diff_data.to_exception()
        ) from process_error
    except subprocess.TimeoutExpired as error:
        timeout_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMEOUT,
            error_code=_.Fossil.TIMEOUT_ERROR,
            arg=f'{from_arg} to {to_arg} in {str(source)}',
            info=str(error),
            extra_details={
                _.Fossil.ARGS: error.args,
                _.Fossil.CMD: error.cmd,
                _.Fossil.TIMEOUT: error.timeout,
                _.Fossil.OUTPUT: error.stdout,
                _.Fossil.STDERR: error.stderr,
            },
        )
        timeout_data = timeout_builder.data()
        timeout_error = fossil_exception.FossilTimeoutError(
            **timeout_data.to_exception()
        )
        diff_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_DIFF,
            error_code=ec.GenericError.INVALID_STATE_ERROR,
            arg=f'{from_arg} to {to_arg} in {str(source)}',
            info=timeout_error.details[e_data.builder_config().info],
            extra_details={
                _.Fossil.ARGS: timeout_error.details[_.Fossil.ARGS],
                _.Fossil.CMD: timeout_error.details[_.Fossil.CMD],
                _.Fossil.TIMEOUT: timeout_error.details[_.Fossil.TIMEOUT],
            },
        )
        diff_data = diff_builder.data()
        raise fossil_exception.FossilDiffError(
            **diff_data.to_exception()
        ) from timeout_error
    raw_changes = diff_process.stdout.decode()
    return raw_changes
