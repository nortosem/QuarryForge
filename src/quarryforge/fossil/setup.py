"""Setup a target repository to store the changed source repository.

Order of setup operations:
# 1. Create new fossil repo for the rebuild:
    cd ~/dev/fossil/; #fossil repo dir
#2 Fossil init command:
fossil init {rebuild}.fossil
--date-override DATETIME # sourced from init commit from original repo
--admin-user USERNAME # the name configured for use with github account
--template ./source_repo.fossil #to match existing config
--project-name # copy from source repo
--project-desc #copy from source repo

#2 The init only defines the admin-user, but a default user remains
necessary and undefined so far. Set the default user:
fossil user default USERNAME -R {rebuild}.fossil

#3 Update the default user with the correct contact mail
## This will match the user name and email used with github for the repo.
fossil user contact USERNAME contact@email.com -R {rebuild}.fossil

Functions:
    new_repo:
    defualt_user:
    user_contact:
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


def new_repo(
    username: str,
    date_override: str,
    new_repo: model.FossilRepo,
    template: model.FossilRepo | None,
    project_name: str | None,
    project_desc: str | None,
) -> str:
    """Run the new repository command to configure a new repository.

    Args:
        username (str): The admin username for the new repository.
        date_override (str):
            The date and time string to override the initial commit date.
        new_repo (model.FossilRepo):
            The FossilRepo object for the new repository.
        template (Optional[model.FossilRepo]):
            An optional template repository to copy config from.
        project_name (Optional[str]): Optional project name.
        project_desc (Optional[str]): Optional project description.

    Returns:
        str: The stdout from the fossil init command.

    Raises:
        fossil_exception.FossilProcessError:
            If the Fossil command fails.
        fossil_exception.FossilTimeoutError:
            If the Fossil command times out.
        fossil_exception.FossilSetupError:
            If there's an issue specific to repository setup.

    """
    try:
        init_repo: subprocess.CompletedProcess[bytes] = subprocess.run(
            fossil_util.rebuild_init(
                username,
                date_override,
                new_repo,
                template,
                project_name,
                project_desc,
            ),
            cwd=new_repo.file.parent,
            capture_output=True,
            check=True,
            timeout=int(_.Fossil.DEFAULT_TIMEOUT),
        )
        return init_repo.stdout.decode()
    except subprocess.CalledProcessError as error:
        process_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
            error_code=_.Fossil.PROCESS_ERROR,
            arg=str(new_repo),
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
            arg=str(new_repo),
            extra_details={
                _.Fossil.ARGS: error.args,
                _.Fossil.CMD: error.cmd,
                _.Fossil.TIMEOUT: error.timeout,
                _.Fossil.OUTPUT: error.stdout,
                _.Fossil.STDERR: error.stderr,
            },
            info=str(error),
        )
        raise fossil_exception.FossilTimeoutError(
            **timeout_builder.data().to_exception()
        ) from error


def default_user(username: str, new_repo: model.FossilRepo) -> str:
    """Run the fossil user set default user command.

    Args:
        username (str): The username to set as default.
        new_repo (model.FossilRepo): The repository to configure.

    Returns:
        str: The stdout from the fossil user default command.

    Raises:
        fossil_exception.FossilProcessError:
            If the Fossil command fails.
        fossil_exception.FossilTimeoutError:
            If the Fossil command times out.
        fossil_exception.FossilSetupError:
            If there's an issue specific to setting the default user.

    """
    try:
        default_user: subprocess.CompletedProcess[bytes] = subprocess.run(
            fossil_util.set_default_user(username, new_repo),
            cwd=new_repo.file.parent,
            capture_output=True,
            check=True,
            timeout=int(_.Fossil.DEFAULT_TIMEOUT),
        )
        return default_user.stdout.decode()
    except subprocess.CalledProcessError as error:
        process_builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
            error_code=_.Fossil.PROCESS_ERROR,
            arg=str(new_repo),
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
            arg=str(new_repo),
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


def user_contact(username: str, email: str, source: model.FossilRepo) -> str:
    """Run the fossil user contact command.

    Args:
        username (str): The username whose contact info to update.
        email (str): The new contact email address.
        source (model.FossilRepo): The repository to configure.

    Returns:
        str: The stdout from the fossil user contact command.

    Raises:
        fossil_exception.FossilProcessError:
            If the Fossil command fails.
        fossil_exception.FossilTimeoutError:
            If the Fossil command times out.
        fossil_exception.FossilSetupError:
            If there's an issue specific to setting user contact info.

    """
    try:
        user_contact: subprocess.CompletedProcess[bytes] = subprocess.run(
            fossil_util.set_user_contact(username, email, source),
            cwd=source.file.parent,
            capture_output=True,
            check=True,
            timeout=int(_.Fossil.DEFAULT_TIMEOUT),
        )
        return user_contact.stdout.decode()
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
