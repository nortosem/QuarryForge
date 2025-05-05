"""Commit Error Configuration


"""
from quarryforge.config.exception_conf import message as Message
from quarryforge.config.model_config import ConfigCommit

from typing import List

def invalid_commit_hash():
    """Invalid commit uuid argument"""
    return Message.Required.field_type(ConfigCommit.HASH, str)


def empty_commit_hash():
    """Commit uuid/hash cannot be empty"""
    return Message.Required.field_empty(ConfigCommit.HASH, str)


def invalid_commit_date():
    """Invalid commit date argument"""
    return Message.Required.field_type(ConfigCommit.DATE, str)


def empty_commit_date():
    """Commit date cannot be empty"""
    return Message.Required.field_empty(ConfigCommit.DATE, str)


def invalid_commit_author():
    """Invalid commit author argument"""
    return Message.Required.field_type(ConfigCommit.AUTHOR, str)


def empty_commit_author():
    """Commit author cannot be empty"""
    return Message.Required.field_empty(ConfigCommit.AUTHOR, str)


def invalid_commit_comment():
    """Invalid commit comment argument"""
    return Message.Required.field_type(ConfigCommit.COMMENT, str)


def empty_commit_comment():
    """Commit comment cannot be empty"""
    return Message.Required.field_empty(ConfigCommit.COMMENT, str)


def invalid_commit_branch():
    """Invalid commit branch argument"""
    return Message.Required.field_type(ConfigCommit.BRANCH, str)


def empty_commit_branch():
    """Commit branch cannot be empty"""
    return Message.Required.field_empty(ConfigCommit.BRANCH, str)


def invalid_commit_tags():
    """Invalid commit tags argument"""
    return Message.Required.field_type(ConfigCommit.TAGS, List)


def invalid_commit_tag_type():
    """Invalid tag in tags argument"""
    return Message.Required.field_type(ConfigCommit.TAGS, List[str])


def empty_commit_tags():
    """Tag cannot be empty"""
    return Message.Required.field_empty(ConfigCommit.TAGS, List[str])
