"""Fossil Command Utility Module

This module provides functions for rebuilding a Fossil repository.
It includes functions to generate commands (as lists of strings) for use with
`subprocess.run` to perform various Fossil operations.
"""
from pathlib import Path
from typing import List, Optional

from quarryforge import model
from quarryforge.config import fossil_config


__all__: List[str] = []


def get_raw_timeline(source: model.FossilRepo) -> List[str]:
    """Creates a command to retrieve timeline data from a fossil repo.

    Args:
        source: GetTimelineArg containing the repository path.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [
        fossil_config.COMMAND.FOSSIL,
        fossil_config.COMMAND.TIMELINE,
        fossil_config.COMMAND.VERBOSE,
        fossil_config.COMMAND.FULL,
        fossil_config.COMMAND.LIMIT,
        fossil_config.COMMAND.NO_LIMIT,
        fossil_config.COMMAND.TYPE,
        fossil_config.COMMAND.CI,
        fossil_config.COMMAND.REPO,
        str(source),
    ]
    return cmd


def rebuild_init(
    username: str,
    date_override: str,
    new_repo: model.FossilRepo,
    template: model.FossilRepo,
    project_name: str,
    project_desc: str,
) -> List[str]:
    """Creates command to initialize the target repo to rebuild a source repo.

    Args:
        username: Primary username for the new repo
        date_override: the date time for init from source repo
        new_repo: the new fossil repos for the updated inf
        template: the source repo for fossil template
        project_name: name from the source repo
        project_desc: description from the source repo

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [
        fossil_config.COMMAND.FOSSIL,
        fossil_config.COMMAND.NEW,
        fossil_config.COMMAND.TEMPLATE
        ,str(template),
        fossil_config.COMMAND.ADMIN_USER,
        username,
        fossil_config.COMMAND.DATE_OVERRIDE,
        date_override,
        fossil_config.COMMAND.PROJECT_NAME,
        project_name,
        fossil_config.COMMAND.PROJECT_DESC,
        project_desc,
        str(new_repo),
    ]
    return cmd


def set_default_user(username: str, new_repo: model.FossilRepo) -> List[str]:
    """Creates a command to set the default user for a Fossil repository.

    Args:
        username: Primary username for the new repo.
        new_repo: Name for new updated repository.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [
        fossil_config.COMMAND.FOSSIL,
        fossil_config.COMMAND.USER,
        fossil_config.COMMAND.DEFAULT,
        username,
        fossil_config.COMMAND.REPO,
        str(new_repo),
    ]
    return cmd


def set_user_contact(
    username: str,
    email: str,
    source: model.FossilRepo
) -> List[str]:
    """Creates a command to set the user's contact information (email)
    in a Fossil repository.

    Args:
        username: Primary username for the new repo.
        email: The updated email contact.
        new_repo: Name for new updated repository.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [
        fossil_config.COMMAND.FOSSIL,
        fossil_config.COMMAND.USER,
        fossil_config.COMMAND.CONTACT,
        username,
        email,
        fossil_config.COMMAND.REPO,
        str(source),
    ]
    return cmd


def open_rebuild(new_repo: model.FossilRepo, workdir: Path) -> List[str]:
    """Creates a command to open a Fossil repository.

    Args:
        new_repo (model.FossilRepo): The Fossil repository file to open.
        workdir (Path): The path opened as the working directory .

    Returns:
        A list of strings representing the command.
    """
    cmd = [
        fossil_config.COMMAND.FOSSIL,
        fossil_config.COMMAND.OPEN,
        str(new_repo),
        fossil_config.COMMAND.WORKDIR,
        str(workdir),
    ]
    return cmd


def close_rebuild() -> List[str]:
    """Close the rebuild repository check--out.

    Returns:
        A list of string representing the command.
    """
    cmd = [
        fossil_config.COMMAND.FOSSIL,
        fossil_config.COMMAND.CLOSE,
    ]
    return cmd


def get_parent_hash(version: str, source: model.FossilRepo) -> List[str]:
    """Creates a command to get the parent hash of a specific commit
    in a Fossil repository.

    Args:
        version (str): provide info about the object in the repository.
        source (model.FossilRepo):
            The source repository being used for the target rebuild repo.
    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [
        fossil_config.COMMAND.FOSSIL,
        fossil_config.COMMAND.INFO,
        version,
        fossil_config.COMMAND.REPO,
        str(source),
    ]
    return cmd


def get_file_changes(
        from_arg: str,
        to_arg: str,
        source: model.FossilRepo
) -> List[str]:
    """Creates a command to retrieve the list of files changed in a
    specific commit.

    Args:
        from_arg (str): the source check-in, or the parent version.
        to_arg (str): the check-in for the secon version of hte file.
        source (model.FossilRepo):
            The source repository to perform the diff command on.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [
        fossil_config.COMMAND.FOSSIL,
        fossil_config.COMMAND.DIFF,
        fossil_config.COMMAND.BRIEF,
        fossil_config.COMMAND.FROM,
        from_arg,
        fossil_config.COMMAND.TO,
        to_arg,
        fossil_config.COMMAND.REPO,
        str(source),
    ]
    return cmd


def get_file_content(
    filename: str,
    outfile: str,
    version: str,
    source: model.FossilRepo
) -> List[str]:
    """Creates a command to retrieve the content of a file at a specific
    version in a Fossil repository.

    Args:
        filename (str): Source file to extract the content from.
        outfile (str): for one filename, write the output to the outfile.
        version (str): The specific check-in containing the source file.
        source (model.FossilRepo):
            The repository to extract artifacts from.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [
        fossil_config.COMMAND.FOSSIL,
        fossil_config.COMMAND.CAT,
        filename,
        fossil_config.COMMAND.OUTFILE,
        outfile,
        fossil_config.COMMAND.VERSION,
        version,
        fossil_config.COMMAND.REPO,
        str(source),
    ]
    return cmd


def ls_branches(source: model.FossilRepo) -> List[str]:
    """Creates a command to list all branches in a Fossil timeline.

    Args:
        source (model.FossilRepo):
            GetTimelineArg containing the source repository path.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [
        fossil_config.COMMAND.FOSSIL,
        fossil_config.COMMAND.BRANCH,
        fossil_config.COMMAND.LIST,
        fossil_config.COMMAND.ALL,
        fossil_config.COMMAND.REPO,
        str(source),
    ]
    return cmd


def closed_branches(source: model.FossilRepo) -> List[str]:
    """Creates a command to list all closed branches in a Fossil timeline.

    Args:
        source (model.FossilRepo):
            GetTimelineArg containing the source repository path.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [
        fossil_config.COMMAND.FOSSIL,
        fossil_config.COMMAND.BRANCH,
        fossil_config.COMMAND.LIST,
        fossil_config.COMMAND.CLOSED,
        fossil_config.COMMAND.REPO,
        str(source),
    ]
    return cmd


def add_files(files: List[Path]) -> List[str]:
    """Creates a command to add files to an open fossil target repository.

    The fossil module caller handles running this command in the target repo
    working directory.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [
        fossil_config.COMMAND.FOSSIL,
        fossil_config.COMMAND.ADD,
    ]
    cmd.extend([str(file_path) for file_path in files])
    return cmd


def commit(
    date_override: str,
    user_override: str,
    comment: str,
    branch: Optional[str],
    tag: Optional[str],
    files: List[Path]) -> List[str]:
    """Creaes a commnad to commit changes to an open fossil targe repository.

    The fossil module caller handles running this command in the target repo
    working directory.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [
        fossil_config.COMMAND.FOSSIL,
        fossil_config.COMMAND.COMMIT,
        fossil_config.COMMAND.HASH,
        fossil_config.COMMAND.DATE_OVERRIDE,
        date_override,
        fossil_config.COMMAND.USER_OVERRIDE,
        user_override,
        fossil_config.COMMAND.COMMENT,
        comment,
    ]

    if branch:
        cmd.extend([''.join(['--',fossil_config.COMMAND.BRANCH]),
                    branch])

    if tag:
        cmd.extend([fossil_config.COMMAND.TAG,
                    tag])

    cmd.extend([str(file_path) for file_path in files])
    return cmd
