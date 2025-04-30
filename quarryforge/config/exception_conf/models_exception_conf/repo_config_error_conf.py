"""


"""
from quarryforge.config.exception_conf.fault_builder import Required
from quarryforge.config.exception_conf.fault_builder import Immutable
from quarryforge.config.models_conf import ConfigArgs as Arg
from quarryforge.config.root import ModelNames as Model


def empty_user() -> str:
    """The user field is empty message."""
    return Required.field_empty(Arg.USER)


def empty_email() -> str:
    """The email field is empty message."""
    return Required.field_empty(Arg.EMAIL)


def empty_src() -> str:
    """The src_repo field is empty message."""
    return Required.field_empty(Arg.SRC_REPO)


def empty_update() -> str:
    """The update_repo field is empty message."""
    return Required.field_empty(Arg.UPDATE_REPO)


def empty_update_dir() -> str:
    """The update_dir field is empty message."""
    return Required.field_empty(Arg.UPDATE_REPO)


def empty_template() -> str:
    """The template field is empty message."""
    return Required.field_empty(Arg.TEMPLATE)


def empty_project_name() -> str:
    """The project_name field is empty message."""
    return Required.field_empty(Arg.PROJECT_NAME)


def empty_project_desc() -> str:
    """The project_desc field is empty message."""
    return Required.field_empty(Arg.PROJECT_DESC)


def missing_user() -> str:
    """The user field is missing message."""
    return Required.field_missing(Arg.USER)


def missing_email() -> str:
    """The email field is missing message."""
    return Required.field_missing(Arg.EMAIL)


def missing_src() -> str:
    """The src_repo field is missing message."""
    return Required.field_missing(Arg.SRC_REPO)


def missing_update() -> str:
    """The update_repo field is missing message."""
    return Required.field_missing(Arg.UPDATE_REPO)


def missing_update_dir() -> str:
    """The update_dir field is missing message."""
    return Required.field_missing(Arg.UPDATE_DIR)


def immutable_config() -> str:
    """The RepoConfig is immutable message."""
    return Immutable.error_message(Model.REPO_CONFIG)
