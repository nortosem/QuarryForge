"""Utility Module

This module provides functions for rebuilding a Fossil repository.
It includes functions to generate commands (as lists of strings) for use with
`subprocess.run` to perform various Fossil operations.
"""
from typing import List

from quarryforge import model
from quarryforge.config import util_config
from quarryforge.config import model_config
from quarryforge.exception import util_exception


def get_raw_timeline(source: model.FossilRepo) -> List[str]:
    """Get Raw Timeline

    Creates a command to retrieve the raw timeline data from a Fossil
    repository.

    Args:
        repo: GetTimelineArg containing the repository path.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.

    Raises:
        ArgumentError: If any required argument in args is missing.
        InvalidArgumentError: If any argument in args is invalid.
    """
    if not all(
        model_util.is_valid_str_type(
            arg, util_exception.FossilUtilError
        ) and model_util.is_not_empty(
            arg, util_exception.FossilUtilError
        ) for arg in [source]):
        raise ArgumentError('#TODO is missing required attributes.')
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.TIMELINE.value,
           util_conf.Command.VERBOSE.value,
           util_conf.Command.FULL.value,
           util_conf.Command.LIMIT.value,
           util_conf.Command.NO_LIMIT.value,
           util_conf.Command.TYPE.value,
           util_conf.Command.CI.value,
           util_conf.Command.REPO.value,
           str(source)]
    return cmd


def rebuild_init(
    username: str,
    date_override: str,
    new_repo: model.FossilRepo,
    template: model.FossilRepo,
    project_name: str,
    project_desc: str,
) -> List[str]:
    """Initialize Rebuild Repo

    Creates a command to initialize a new empty repository for rebuilding
    a source repository.

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

    Raises:
        ArgumentError: If any required argument in args is missing.
        InvalidArgumentError: If any argument in args is invalid.
    """
    if not all(
        model_util.is_valid_str_type(
            arg, util_exception.FossilUtilError
        ) and model_util.is_not_empty(
            arg, util_exception.FossilUtilError
        ) for arg in [
            username, date_override, new_repo,
            template, project_name, project_desc]):
        raise ArgumentError('#TODO is missing required attributes.')
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.NEW.value,
           util_conf.Command.TEMPLATE.value,
           args.template,
           util_conf.Command.ADMIN_USER.value,
           args.user,
           util_conf.Command.PROJECT_NAME.value,
           args.project_name,
           util_conf.Command.PROJECT_DESC.value,
           args.project_desc,
           args.rebuild_repo]
    return cmd


def set_default_user(username: str, new_repo: model.FossilRepo) -> List[str]:
    """Set Default User

    Creates a command to set the default user for a Fossil repository.

    Args:
        username: Primary username for the new repo.
        new_repo: Name for new updated repository.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.

    Raises:
        ArgumentError: If any required argument in args is missing.
        InvalidArgumentError: If any argument in args is invalid.
    """
    if not all(
        model_util.is_valid_str_type(
            arg, util_exception.FossilUtilError
        ) and model_util.is_not_empty(
            arg, util_exception.FossilUtilError
        ) for arg in [
            username, new_repo]):
        raise ArgumentError('#TODO is missing required attributes.')
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.USER.value,
           util_conf.Command.DEFAULT.value,
           username,
           util_conf.Command.REPO.value,
           str(new_repo)]
    return cmd


def set_user_contact(
    username: str,
    email: str,
    source: model.FossilRepo
) -> List[str]:
    """Set User Contact

    Creates a command to set the user's contact information (email)
    in a Fossil repository.

    Args:
        username: Primary username for the new repo.
        email: The updated email contact.
        new_repo: Name for new updated repository.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.

    Raises:
        ArgumentError: If any required argument in args is missing.
        InvalidArgumentError: If any argument in args is invalid.
    """
    if not all(
        model_util.is_valid_str_type(
            arg, util_exception.FossilUtilError
        ) and model_util.is_not_empty(
            arg, util_exception.FossilUtilError
        ) for arg in [
            username, email, source]):
        raise ArgumentError('#TODO is missing required attributes.')
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.USER.value,
           util_conf.Command.CONTACT.value,
           username,
           email,
           util_conf.Command.REPO.value,
           str(source)]
    return cmd


def get_parent_hash(version: str, source: model.FossilRepo) -> List[str]:
    """Get Parent Hash ID

    Creates a command to get the parent hash of a specific commit
    in a Fossil repository.

    Args:
        args: InfoArgs containing the commit version and repository path.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    if not all(
        model_util.is_valid_str_type(
            arg, util_exception.FossilUtilError
        ) and model_util.is_not_empty(
            arg, util_exception.FossilUtilError
        ) for arg in [version, str(source)]):
        raise ArgumentError('#TODO is missing required attributes.')
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.INFO.value,
           version,
           util_conf.Command.REPO.value,
           str(source)]
    return cmd


def get_file_changes(
        from_arg: str,
        to_arg: str,
        source: model.FossilRepo
) -> List[str]:
    """Get File Changes

    Creates a command to retrieve the list of files changed in a
    specific commit.

    Args:
        args: DiffArgs containing the parent and child commit hashes
            and the repository path.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    if not all(
        model_util.is_valid_str_type(
            arg, util_exception.FossilUtilError
        ) and model_util.is_not_empty(
            arg, util_exception.FossilUtilError
        ) for arg in [from_arg, to_arg, str(source)]):
        raise ArgumentError('#TODO is missing required attributes.')
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.DIFF.value,
           util_conf.Command.BRIEF.value,
           util_conf.Command.FROM.value,
           args.parent, util_conf.Command.TO.value,
           args.child,
           util_conf.Command.REPO.value,
           args.src_repo]
    return cmd


def get_file_content(
    filename: str,
    outfile: str,
    version: str,
    source: model.FossilRepo
) -> List[str]:
    """Get File Content

    Creates a command to retrieve the content of a file at a specific
    version in a Fossil repository.

    Args:
        args: CatArgs containing the file path, version, and repository path.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    if not all(
        model_util.is_valid_str_type(
            arg, util_exception.FossilUtilError
        ) and model_util.is_not_empty(
            arg, util_exception.FossilUtilError
        ) for arg in [filename, outfile, version, str(source)]):
        raise ArgumentError('#TODO is missing required attributes.')
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.CAT.value,
           args.file,
           util_conf.Command.VERSION.value,
           args.version,
           util_conf.Command.REPO.value,
           args.src_repo]
    return cmd


def ls_branches(source: model.FossilRepo) -> List[str]:
    """List Branches

    Creates a command to list all branches in a Fossil timeline.

    Args:
        src: GetTimelineArg containing the source repository path.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    if not all(
        model_util.is_valid_str_type(
            arg, util_exception.FossilUtilError
        ) and model_util.is_not_empty(
            arg, util_exception.FossilUtilError
        ) for arg in [str(source)]):
        raise ArgumentError('#TODO is missing required attributes.')
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.BRANCH.value,
           util_conf.Command.LIST.value,
           util_conf.Command.ALL.value,
           util_conf.Command.REPO.value,
           src]
    return cmd


def closed_branches(source: model.FossilRepo) -> List[str]:
    """Closed Branches

    Creates a command to list all closed branches in a Fossil timeline.

    Args:
        src: GetTimelineArg containing the source repository path.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    if not all(
        model_util.is_valid_str_type(
            arg, util_exception.FossilUtilError
        ) and model_util.is_not_empty(
            arg, util_exception.FossilUtilError
        ) for arg in [str(source)]):
        raise ArgumentError('#TODO is missing required attributes.')
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.BRANCH.value,
           util_conf.Command.LIST.value,
           util_conf.Command.CLOSED.value,
           util_conf.Command.REPO.value,
           src]
    return cmd


def add_files(target: model.FossilRepo, *files):
    """Add Files"""
    pass



def commit(target: model.FossilRepo, *files):
    """Commit file changes"""
    pass
