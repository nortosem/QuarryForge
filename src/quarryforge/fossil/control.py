"""Fossil control provides functions to manage repository state (open/close)."""

from pathlib import Path
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


__all__: list[str] = ['open_repo', 'close_repo']


def open_repo(repo: model.FossilRepo, workdir: Path) -> None:
    """Open the specified repository in the given working directory.

    Args:
        repo: The FossilRepo model instance to open.
        workdir: The directory to open the repository in.

    Raises:
        FossilProcessError: If the 'fossil open' command fails.
        FossilTimeoutError: If the command times out.
    """
    try:
        open_process: subprocess.CompletedProcess[bytes] = subprocess.run(
            fossil_util.open_repo(repo, workdir),
            cwd=workdir,
            capture_output=True,
            check=True,
            timeout=int(_.Fossil.DEFAULT_TIMEOUT),
        )
    except subprocess.CalledProcessError as error:
        builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_CONTROL,
            error_code=_.Fossil.PROCESS_ERROR,
            extra_details={
                _.Fossil.CMD: error.cmd,
                _.Fossil.RETURN_CODE: error.returncode,
                _.Fossil.OUTPUT: error.stdout,
                _.Fossil.STDERR: error.stderr,
            }
        )
        raise fossil_exception.FossilProcessError(
            **builder.data().to_exception()
        ) from error
    except subprocess.TimeoutExpired as error:
        builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_CONTROL,
            error_code=_.Fossil.TIMEOUT_ERROR,
            extra_details={
                _.Fossil.ARGS: error.args,
                _.Fossil.CMD: error.cmd,
                _.Fossil.TIMEOUT: error.timeout,
                _.Fossil.OUTPUT: error.stdout,
                _.Fossil.STDERR: error.stderr,
            }
        )
        raise fossil_exception.FossilTimeoutError(
            **builder.data().to_exception()
        ) from error


def close_repo(workdir: Path)
    """Close the fossil checkout in the given working directory."""
    try:
        close_process: subprocess.CompletedProcess[bytes] = subprocess.run(
            fossil_util.close_repo(),
            cwd=workdir,
            capture_output=True,
            check=True,
            timeout=int(_.Fossil.DEFAULT_TIMEOUT),
        )
    except subprocess.CalledProcessError as error:
        builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_CONTROL,
            error_code=_.Fossil.PROCESS_ERROR,
            extra_details={
                _.Fossil.CMD: error.cmd,
                _.Fossil.RETURN_CODE: error.returncode,
                _.Fossil.OUTPUT: error.stdout,
                _.Fossil.STDERR: error.stderr,
            }
        )
        raise fossil_exception.FossilProcessError(
            **builder.data().to_exception()
        ) from error
    except subprocess.TimeoutExpired as error:
        builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_CONTROL,
            error_code=_.Fossil.TIMEOUT_ERROR,
            extra_details={
                _.Fossil.ARGS: error.args,
                _.Fossil.CMD: error.cmd,
                _.Fossil.TIMEOUT: error.timeout,
                _.Fossil.OUTPUT: error.stdout,
                _.Fossil.STDERR: error.stderr,
            }
        )
        raise fossil_exception.FossilTimeoutError(
            **builder.data().to_exception()
        ) from error
