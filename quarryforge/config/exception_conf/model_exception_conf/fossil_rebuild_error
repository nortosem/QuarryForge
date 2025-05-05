"""RepoConfig Error Configuration


"""
from pathlib import Path
from quarryforge.config.exception_conf.fault_builder import Immutable
from quarryforge.config.exception_conf.fault_builder import PathMessage
from quarryforge.config.exception_conf.fault_builder import Required
from quarryforge.config.models_conf import ConfigArgs as Arg
from quarryforge.config.root import ModelNames as Model


def empty_user() -> str:
    """The user field is empty message."""
    return Required.field_empty(Arg.USER, str)


def empty_email() -> str:
    """The email field is empty message."""
    return Required.field_empty(Arg.EMAIL, str)


def empty_src() -> str:
    """The src_repo field is empty message."""
    return Required.field_empty(Arg.SRC_REPO, Path)


def empty_update() -> str:
    """The update_repo field is empty message."""
    return Required.field_empty(Arg.UPDATE_REPO, Path)


def empty_update_dir() -> str:
    """The update_dir field is empty message."""
    return Required.field_empty(Arg.UPDATE_REPO, Path)


def empty_template() -> str:
    """The template field is empty message."""
    return Required.field_empty(Arg.TEMPLATE, Path)


def empty_project_name() -> str:
    """The project_name field is empty message."""
    return Required.field_empty(Arg.PROJECT_NAME, str)


def empty_project_desc() -> str:
    """The project_desc field is empty message."""
    return Required.field_empty(Arg.PROJECT_DESC, str)


def invalid_user() -> str:
    """The user field is invalid message."""
    return Required.field_type(Arg.USER, str)


def invalid_email() -> str:
    """The email field is invalid message."""
    return Required.field_type(Arg.EMAIL, str)


def invalid_src() -> str:
    """The src_repo field is invalid message."""
    return ' '.join([Required.field_type(Arg.SRC_REPO, str),
        PathMessage.not_a_path(Arg.SRC_REPO)])

def invalid_update() -> str:
    """The update_repo field is invalid message."""
    return ' '.join([Required.field_type(Arg.UPDATE_REPO, str),
                     PathMessage.not_a_path(Arg.UPDATE_REPO)])


def invalid_update_dir() -> str:
    """The update_dir field is invalid message."""
    return Required.field_type(Arg.UPDATE_DIR, Path)


def immutable_config() -> str:
    """The RepoConfig is immutable message."""
    return Immutable.error_message(Model.REPO_CONFIG)
