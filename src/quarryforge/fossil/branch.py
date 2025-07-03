"""Fossil Branch Process

Manage branch info using fossil branch
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


def list_all(source: model.FossilRepo) -> str:
    """List all Branches for the source reposiotory.

    Executes the Fossil 'branch list --all' command to list all branches
    in a given repository.

    Args:
        source (model.FossilRepo): The repository to list branches from.

    Returns:
        str: The raw output string containing the list of branches.

    Raises:
        fossil_exception.FossilProcessError:
            If the Fossil command fails.
        fossil_exception.FossilTimeoutError:
            If the Fossil command times out.
        fossil_exception.FossilBranchError:
            If an issue occurs during the branch operation.

    """
    try:
        list_process: subprocess.CompletedProcess[bytes] = subprocess.run(
            fossil_util.ls_branches(source),
            cwd=source.file.parent,
            capture_output=True,
            check=True,
            timeout=int(_.Fossil.DEFAULT_TIMEOUT),
        )
        return list_process.stdout.decode()
    except subprocess.CalledProcessError as error:
        process_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
            error_code=_.Fossil.PROCESS_ERROR,
            arg=str(source),
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
            arg=str(source),
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
