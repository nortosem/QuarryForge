"""Utility Module

#todo
"""
from collections import namedtuple

from quarryforge.config import CatConfig
from quarryforge.config import ConfigArgs
from quarryforge.config import Command
from quarryforge.config import DiffConfig
from quarryforge.config import InfoConfig
from quarryforge.config import TimelineConfig

from typing import List


RepoConfig = namedtuple(ConfigArgs.type_name(), ConfigArgs.slots())
RepoConfig.__doc__ = ConfigArgs.docs()


TimelineArg = namedtuple(TimelineConfig.type_name(), TimelineConfig.slots())
TimelineArg.__doc__ = TimelineConfig.docs()


InfoArgs = namedtuple(InfoConfig.type_name(), InfoConfig.slots())
InfoArgs.__doc__ = InfoConfig.docs()


DiffArgs = namedtuple(DiffConfig.type_name(), DiffConfig.slots())
DiffArgs.__doc__ = DiffConfig.docs()


CatArgs = namedtuple(CatConfig.type_name(), CatConfig.slots())
CatArgs.__doc__ = CatConfig.docs()


def init_rebuild_repo(args: RepoConfig) -> List:
    """Initiate Rebuild Repo

    Create a new empty repo for the source repo being rebuilt.
    Args:
        args (RepoConfig): Repository configuration arguments.
    Returns:
        cmd (List): A list of the command and arguments to use with the
            subprocess.run method.
    #todo handle case where template is none
    """
    cmd = [Command.FOSSIL.value, Command.NEW.value, Command.TEMPLATE.value,
           args.template, Command.ADMIN_USER.value, args.user,
           Command.PROJECT_NAME.value, args.project_name,
           Command.PROJECT_DESC.value, args.project_desc,
           args.rebuild_repo]
    return cmd


def set_default_user(args: RepoConfig) -> List:
    """Set Default User


    Args:
        args (RepoConfig):
    Returns:
        cmd (List):
    """
    cmd = [Command.FOSSIL.value, Command.USER.value, Command.DEFAULT.value,
           args.user, Command.REPO.value]
    return cmd


def set_user_contact(args: RepoConfig) -> List:
    """Set User Contact

    Return the subprocess.run command list for setting user email.

    Args:
        args (RepoConfig):
    Returns:
        cmd (List):
    """
    cmd = [Command.FOSSIL.value, Command.USER.value, Command.CONTACT.value,
           args.user, args.email, Command.REPO.value, args.src_repo]
    return cmd


def ls_branches(src: TimelineArg) -> List:
    """List Branches

    List all branches found in the fossil timeline
    """
    cmd = [Command.FOSSIL.value, Command.BRANCH.value, Command.LIST.value,
           Command.ALL.value, Command.REPO.value, src]
    return cmd


def closed_branches(src: TimelineArg) -> List:
    """Closed Branches

    Returns all closed branches in the fossil timeline
    """
    cmd = [Command.FOSSIL.value, Command.BRANCH.value, Command.LIST.value,
           Command.CLOSED.value, Command.REPO.value, src]
    return cmd


def get_raw_timeline(repo: TimelineArg) -> List:
    """Get Raw Timeline

    Returns a command to get the full timeline for a fossil repo.
    """
    cmd = [Command.FOSSIL.value, Command.TIMELINE.value, Command.VERBOSE.value,
           Command.FULL.value, Command.LIMIT.value, Command.NO_LIMIT.value,
           Command.TYPE.value, Command.CI.value, Command.REPO.value, repo]
    return cmd


def get_parent_hash(args: InfoArgs):
    """Get Parent Hash ID

    Returns the command for a final Parent hash of a commit.
    """
    cmd = [Command.FOSSIL.value, Command.INFO.value, args.version,
           Command.REPO.value, args.src_repo]
    return cmd


def get_file_changes(args: DiffArgs):
    """Get File Changes

    Returns the command to get all files changed for a commit.
    """
    cmd = [Command.FOSSIL.value, Command.DIFF.value, Command.BRIEF.value,
           Command.FROM.value, args.parent, Command.TO.value, args.child,
           Command.REPO.value, args.src_repo]
    return cmd


def get_file_content(args: CatArgs):
    """Get File Content

    Returns the command to get all added/changed file content for a file.
    """
    cmd = [Command.FOSSIL.value, Command.CAT.value, args.file,
           Command.VERSION.value, args.version, Command.REPO.value,
           args.src_repo]
    return cmd
