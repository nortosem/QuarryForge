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
    cmd: List[str] = [
        fossil_config.Command.FOSSIL,
        fossil_config.Command.TIMELINE,
        fossil_config.Command.VERBOSE,
        fossil_config.Command.FULL,
        fossil_config.Command.LIMIT,
        fossil_config.Command.NO_LIMIT,
        fossil_config.Command.TYPE,
        fossil_config.Command.CI,
        fossil_config.Command.REPO,
        str(source),
    ]
    return cmd


def rebuild_init(
    username: str,
    date_override: str,
    new_repo: model.FossilRepo,
    template: Optional[model.FossilRepo],
    project_name: Optional[str],
    project_desc: Optional[str],
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
    cmd: List[str] = [
        fossil_config.Command.FOSSIL,
        fossil_config.Command.NEW,
        fossil_config.Command.ADMIN_USER,
        username,
        fossil_config.Command.DATE_OVERRIDE,
        date_override,
    ]
    if template:
        cmd.extend([
            fossil_config.Command.TEMPLATE,
            str(template),
        ])
    if project_name:
        cmd.extend([
            fossil_config.Command.PROJECT_NAME,
            project_name,
        ])
    if project_desc:
        cmd.extend([
            fossil_config.Command.PROJECT_DESC,
            project_desc,
        ])
    cmd.append(str(new_repo))
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
    cmd: List[str] = [
        fossil_config.Command.FOSSIL,
        fossil_config.Command.USER,
        fossil_config.Command.DEFAULT,
        username,
        fossil_config.Command.REPO,
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
    cmd: List[str] = [
        fossil_config.Command.FOSSIL,
        fossil_config.Command.USER,
        fossil_config.Command.CONTACT,
        username,
        email,
        fossil_config.Command.REPO,
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
    cmd: List[str] = [
        fossil_config.Command.FOSSIL,
        fossil_config.Command.OPEN,
        str(new_repo),
        fossil_config.Command.WORKDIR,
        str(workdir),
    ]
    return cmd


def close_rebuild() -> List[str]:
    """Close the rebuild repository check--out.

    Returns:
        A list of string representing the command.
    """
    cmd: List[str] = [
        fossil_config.Command.FOSSIL,
        fossil_config.Command.CLOSE,
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
    cmd: List[str] = [
        fossil_config.Command.FOSSIL,
        fossil_config.Command.INFO,
        version,
        fossil_config.Command.REPO,
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
    cmd: List[str] = [
        fossil_config.Command.FOSSIL,
        fossil_config.Command.DIFF,
        fossil_config.Command.BRIEF,
        fossil_config.Command.FROM,
        from_arg,
        fossil_config.Command.TO,
        to_arg,
        fossil_config.Command.REPO,
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
    cmd: List[str] = [
        fossil_config.Command.FOSSIL,
        fossil_config.Command.CAT,
        filename,
        fossil_config.Command.OUTFILE,
        outfile,
        fossil_config.Command.VERSION,
        version,
        fossil_config.Command.REPO,
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
    cmd: List[str] = [
        fossil_config.Command.FOSSIL,
        fossil_config.Command.BRANCH,
        fossil_config.Command.LIST,
        fossil_config.Command.ALL,
        fossil_config.Command.REPO,
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
    cmd: List[str] = [
        fossil_config.Command.FOSSIL,
        fossil_config.Command.BRANCH,
        fossil_config.Command.LIST,
        fossil_config.Command.CLOSED,
        fossil_config.Command.REPO,
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
    cmd: List[str] = [
        fossil_config.Command.FOSSIL,
        fossil_config.Command.ADD,
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
    cmd: List[str] = [
        fossil_config.Command.FOSSIL,
        fossil_config.Command.COMMIT,
        fossil_config.Command.HASH,
        fossil_config.Command.DATE_OVERRIDE,
        date_override,
        fossil_config.Command.USER_OVERRIDE,
        user_override,
        fossil_config.Command.COMMENT,
        comment,
    ]

    if branch:
        cmd.extend([
            ''.join(['--',fossil_config.Command.BRANCH]),
            branch
        ])

    if tag:
        cmd.extend([
            fossil_config.Command.TAG,
            tag
        ])

    cmd.extend([str(file_path) for file_path in files])
    return cmd
