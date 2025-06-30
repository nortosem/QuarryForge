"""Fossil Cat Process

Provides methods for retrieving file content from a Fossil repository.
"""

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


def content(
    filename: str,
    outfile: str,
    version: str,
    source: model.FossilRepo,
) -> str:
    """Use fossil cat to transfer source content to the updated repo
    project dir.

    Retrieves the content of a specific file at a given version from a
    Fossil repository and writes it to an output file.

    Args:
        filename (str):
            The name of the file to retrieve content from.
        outfile (str):
            The path to the output file where content will be written.
        version (str):
            The specific check-in hash of the file version.
        source (model.FossilRepo):
            The repository to extract artifacts from.

    Returns:
        str:
            The stdout from the fossil cat command
            (often empty for success).

    Raises:
        fossil_exception.FossilProcessError:
            If the Fossil command fails.
        fossil_exception.FossilTimeoutError:
            If the Fossil command times out.
        fossil_exception.FossilCatError:
            If an issue occurs during the cat operation.

    """
    try:
        cat_process: subprocess.CompletedProcess[bytes] = subprocess.run(
            fossil_util.get_file_content(filename, outfile, version, source),
            cwd=source.workdir,
            capture_output=True,
            check=True,
            timeout=int(_.Fossil.DEFAULT_TIMEOUT),
        )
    except subprocess.CalledProcessError as error:
        process_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
            error_code=_.Fossil.PROCESS_ERROR,
            arg=f'{filename} @ {version} from {str(source)}',
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
        cat_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_CAT,
            error_code=ec.GenericError.EXTERNAL_DEPENDENCY_ERROR,
            arg=f'{filename} @ {version} from {str(source)}',
            extra_details={
                ec.DescMsg.DEPENDENCY: process_error.details[_.Fossil.CMD],
                ec.DescMsg.REASON: process_error.details[_.Fossil.STDERR],
            },
        )
        cat_data = cat_builder.data()
        raise fossil_exception.FossilCatError(
            **cat_data.to_exception()
        ) from process_error
    except subprocess.TimeoutExpired as error:
        timeout_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMEOUT,
            error_code=_.Fossil.TIMEOUT_ERROR,
            arg=f'{filename} @ {version} from {str(source)}',
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
        cat_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_CAT,
            error_code=ec.GenericError.INVALID_STATE_ERROR,
            arg=f'{filename} @ {version} from {str(source)}',
            info=timeout_error.details[e_data.builder_config().info],
            extra_details={
                _.Fossil.ARGS: timeout_error.details[_.Fossil.ARGS],
                _.Fossil.CMD: timeout_error.details[_.Fossil.CMD],
                _.Fossil.TIMEOUT: timeout_error.details[_.Fossil.TIMEOUT],
            },
        )
        cat_data = cat_builder.data()
        raise fossil_exception.FossilCatError(
            **cat_data.to_exception()
        ) from timeout_error
    content_changes = cat_process.stdout.decode()
    return content_changes
