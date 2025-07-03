"""Get parent commit hash for the commit version and repository provided."""

import subprocess

from quarryforge import model
from quarryforge.config import fossil_config as _
from quarryforge.config import model_config
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.config.exception_conf import exception_data as e_data
from quarryforge.config.exception_conf import (
    fossil_exception_config as fossil_ec,
)
from quarryforge.exception import fossil_exception
from quarryforge.util import fossil_util


def get_parent(version: str, source: model.FossilRepo) -> str | None:
    """Get Parent Commit Version.

    Retrieves the parent commit hash for a given version (check-in hash)
    from a Fossil repository.

    Args:
        version (str): The specific check-in hash to get the parent of.
        source (model.FossilRepo): The repository to query.

    Returns:
        str | None:
            The version string for the parent commit, or None if it's the
            initial commit (no parent).

    Raises:
        FossilProcessError: If the Fossil command fails.
        FossilTimeoutError: If the Fossil command times out.
        FossilInfoError: If parsing the command's output fails.

    """
    try:
        info_process: subprocess.CompletedProcess[bytes] = subprocess.run(
            fossil_util.get_parent_hash(version, source),
            cwd=source.workdir.cwd(),
            capture_output=True,
            check=True,
            timeout=int(_.Fossil.DEFAULT_TIMEOUT),
        )
    except subprocess.CalledProcessError as error:
        process_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
            error_code=_.Fossil.PROCESS_ERROR,
            arg=f'{version} from {str(source)}',
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
            arg=f'{version} from {str(source)}',
            info=str(error.stdout),
            extra_details={
                _.Fossil.CMD: error.cmd,
                _.Fossil.TIMEOUT: error.timeout,
                _.Fossil.OUTPUT: error.stdout,
                _.Fossil.STDERR: error.stderr,
            },
        )
        raise fossil_exception.FossilTimeoutError(
            **timeout_builder.data().to_exception()
        ) from error

    raw_parent_hash = info_process.stdout.decode()
    initial_commit_re = _.info_data().init_pattern()
    commit_parent_re = _.info_data().parent_pattern()
    match_init = initial_commit_re.match(raw_parent_hash)
    match_parent = commit_parent_re.match(raw_parent_hash)

    if match_parent:
        return match_parent.group(model_config.fossil_commit_config().uuid)
    if match_init:
        return None
    else:
        info_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_INFO,
            error_code=ec.GenericError.VALUE_ERROR,
            arg=raw_parent_hash[:100]
            + ('...' if len(raw_parent_hash) > 100 else raw_parent_hash),
            info=(
                f'Unable to parse parent hash or detect initial commit for'
                f' version {version}.'
            ),
            extra_details={'raw_output': raw_parent_hash},
        )
        info_data = info_builder.data()
        raise fossil_exception.FossilOperationError(**info_data.to_exception())
