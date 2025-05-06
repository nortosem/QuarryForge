"""Utility Module

This module provides functions for rebuilding a Fossil repository.
It includes functions to generate commands (as lists of strings) for use with
`subprocess.run` to perform various Fossil operations.
"""
from typing import List

from quarryforge import model
from quarryforge.config import util_config


def init_rebuild_repo(args: model.FossilRebuild) -> List:
    """Initiate Rebuild Repo

    Creates a command to initialize a new empty repository for rebuilding
    a source repository.

    Args:
        args: Repository configuration arguments.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.

    Raises:
        MissingArgumentError: If any required argument in args is missing.
        InvalidArgumentError: If any argument in args is invalid.
    """ #todo handle case where template is none
    if not args:
        raise MissingArgumentError("model.FossilRebuild args is required.")
    if not all(hasattr(args, attr) for attr in
               ["template", "user", "project_name", "project_desc", "rebuild_repo"]):
        raise InvalidArgumentError("model.FossilRebuild is missing required attributes.")
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


def set_default_user(args: model.FossilRebuild) -> List:
    """Set Default User

    Creates a command to set the default user for a Fossil repository.

    Args:
        args: Repository configuration arguments.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.USER.value,
           util_conf.Command.DEFAULT.value,
           args.user,
           util_conf.Command.REPO.value]
    return cmd


def set_user_contact(args: model.FossilRebuild) -> List:
    """Set User Contact

    Creates a command to set the user's contact information (email)
    in a Fossil repository.

    Args:
        args: Repository configuration arguments.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.USER.value,
           util_conf.Command.CONTACT.value,
           args.user,
           args.email,
           util_conf.Command.REPO.value,
           args.src_repo]
    return cmd


def ls_branches(src: model.GetTimelineArg) -> List:
    """List Branches

    Creates a command to list all branches in a Fossil timeline.

    Args:
        src: GetTimelineArg containing the source repository path.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.BRANCH.value,
           util_conf.Command.LIST.value,
           util_conf.Command.ALL.value,
           util_conf.Command.REPO.value,
           src]
    return cmd


def closed_branches(src: model.GetTimelineArg) -> List:
    """Closed Branches

    Creates a command to list all closed branches in a Fossil timeline.

    Args:
        src: GetTimelineArg containing the source repository path.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.BRANCH.value,
           util_conf.Command.LIST.value,
           util_conf.Command.CLOSED.value,
           util_conf.Command.REPO.value,
           src]
    return cmd


def get_raw_timeline(repo: model.GetTimelineArg) -> List:
    """Get Raw Timeline

    Creates a command to retrieve the raw timeline data from a Fossil
    repository.

    Args:
        repo: GetTimelineArg containing the repository path.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.TIMELINE.value,
           util_conf.Command.VERBOSE.value,
           util_conf.Command.FULL.value,
           util_conf.Command.LIMIT.value,
           util_conf.Command.NO_LIMIT.value,
           util_conf.Command.TYPE.value,
           util_conf.Command.CI.value,
           util_conf.Command.REPO.value,
           repo]
    return cmd


def get_parent_hash(args: model.InfoArgs):
    """Get Parent Hash ID

    Creates a command to get the parent hash of a specific commit
    in a Fossil repository.

    Args:
        args: InfoArgs containing the commit version and repository path.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.INFO.value,
           args.version,
           util_conf.Command.REPO.value,
           args.src_repo]
    return cmd


def get_file_changes(args: model.DiffArgs):
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
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.DIFF.value,
           util_conf.Command.BRIEF.value,
           util_conf.Command.FROM.value,
           args.parent, util_conf.Command.TO.value,
           args.child,
           util_conf.Command.REPO.value,
           args.src_repo]
    return cmd


def get_file_content(args: model.CatArgs):
    """Get File Content

    Creates a command to retrieve the content of a file at a specific
    version in a Fossil repository.

    Args:
        args: CatArgs containing the file path, version, and repository path.

    Returns:
        A list of strings representing the command and its arguments for use
        with `subprocess.run`.
    """
    cmd = [util_conf.Command.FOSSIL.value,
           util_conf.Command.CAT.value,
           args.file,
           util_conf.Command.VERSION.value,
           args.version,
           util_conf.Command.REPO.value,
           args.src_repo]
    return cmd
