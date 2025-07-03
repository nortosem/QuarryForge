"""Add provides methods for adding files to open Fossil check-out."""

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


def files(files: list[Path]) -> str:
    """Add files to the Fossil repository check-out.

    Args:
        files (List[Path]):
            A list of `Path` objects representing the files to add. The
            command will be run in the current working directory of the
            process.

    Returns:
        str: The stdout from the fossil add command.

    Raises:
        fossil_exception.FossilProcessError:
            If the Fossil command fails.
        fossil_exception.FossilTimeoutError:
            If the Fossil command times out.
        fossil_exception.FossilAddError:
            If an issue occurs during the add operation.

    """
    try:
        add_process: subprocess.CompletedProcess[bytes] = subprocess.run(
            fossil_util.add_files(files),
            capture_output=True,
            check=True,
            timeout=int(_.Fossil.DEFAULT_TIMEOUT),
        )
        return add_process.stdout.decode()
    except subprocess.CalledProcessError as error:
        process_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
            error_code=_.Fossil.PROCESS_ERROR,
            arg=f'files: {[str(f) for f in files]}',
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
            arg=f'files: {[str(f) for f in files]}',
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


def remove_files(files: list[Path]) -> str:
    """Remove files from the Fossil repository check-out.

    Args:
        files (List[Path]):
            A list of `Path` objects representing the files to remove.

    Returns:
        str: The stdout from the fossil rm command.

    Raises:
        fossil_exception.FossilProcessError:
            If the Fossil command fails.
        fossil_exception.FossilTimeoutError:
            If the Fossil command times out.
        fossil_exception.FossilAddError:
            If an issue occurs during the remove operation.

    """
    raise NotImplementedError('Remove files not yet implemented.')


def rename_file(old_path: Path, new_path: Path) -> str:
    """Rename a file in the Fossil repository check-out.

    Args:
        old_path (Path): The current path of the file.
        new_path (Path): The new path for the file.

    Returns:
        str: The stdout from the fossil mv command.

    Raises:
        fossil_exception.FossilProcessError:
            If the Fossil command fails.
        fossil_exception.FossilTimeoutError:
            If the Fossil command times out.
        fossil_exception.FossilAddError:
            If an issue occurs during the rename operation.

    """
    raise NotImplementedError('Rename file not yet implemented.')
