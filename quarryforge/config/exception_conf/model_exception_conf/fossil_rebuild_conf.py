"""RepoConfig Error Configuration


"""
from pathlib import Path
from quarryforge.config import model_config
from quarryforge.config.exception_conf import message as Message
from quarryforge.config.root import ModelNames as Model


def empty_user() -> str:
    """The user field is empty message."""
    return Required.field_empty(model_config.ConfigFossilRebuild.USER, str)


def empty_email() -> str:
    """The email field is empty message."""
    return Required.field_empty(model_config.ConfigFossilRebuild.EMAIL, str)


def empty_src() -> str:
    """The src_repo field is empty message."""
    return Required.field_empty(
        model_config.ConfigFossilRebuild.SRC_REPO, Path)


def empty_update() -> str:
    """The update_repo field is empty message."""
    return Required.field_empty(
        model_config.ConfigFossilRebuild.UPDATE_REPO, Path)


def empty_update_dir() -> str:
    """The update_dir field is empty message."""
    return Required.field_empty(
        model_config.ConfigFossilRebuild.UPDATE_REPO, Path)


def empty_template() -> str:
    """The template field is empty message."""
    return Required.field_empty(
        model_config.ConfigFossilRebuild.TEMPLATE, Path)


def empty_project_name() -> str:
    """The project_name field is empty message."""
    return Required.field_empty(
        model_config.ConfigFossilRebuild.PROJECT_NAME, str)


def empty_project_desc() -> str:
    """The project_desc field is empty message."""
    return Required.field_empty(
        model_config.ConfigFossilRebuild.PROJECT_DESC, str)


def invalid_user() -> str:
    """The user field is invalid message."""
    return Required.field_type(model_config.ConfigFossilRebuild.USER, str)


def invalid_email() -> str:
    """The email field is invalid message."""
    return Required.field_type(model_config.ConfigFossilRebuild.EMAIL, str)


def invalid_src() -> str:
    """The src_repo field is invalid message."""
    return ' '.join([
        Required.field_type(model_config.ConfigFossilRebuild.SRC_REPO, str),
        PathMessage.not_a_path(model_config.ConfigFossilRebuild.SRC_REPO)
    ])

def invalid_update() -> str:
    """The update_repo field is invalid message."""
    return ' '.join([
        Required.field_type(model_config.ConfigFossilRebuild.UPDATE_REPO, str),
        PathMessage.not_a_path(model_config.ConfigFossilRebuild.UPDATE_REPO)
    ])


def invalid_update_dir() -> str:
    """The update_dir field is invalid message."""
    return Required.field_type(
        model_config.ConfigFossilRebuild.UPDATE_DIR, Path)


def immutable_config() -> str:
    """The RepoConfig is immutable message."""
    return Immutable.error_message(Model.REPO_CONFIG)
