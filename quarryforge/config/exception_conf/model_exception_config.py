"""Model Exception Configuration

1st check if arg is a string,
next strip if it is a string.
if it is empty string raise error.
else turn string into a path object.
expanduser and resolve.
must exist if is_new is False.
must be a file
must be fossilrrepor
if new repo true:
mst be path or path from string.
file does not exist.
is parent dir exist and writeable?
"""
from typing import List, Tuple

from quarryforge.config import model_config
from quarryforge.config import root
from quarryforge.config.exception_conf import base_exception_config
from quarryforge.config.exception_conf import exception_config
from quarryforge.meta import immutable


__all__: List[str] = [
    'DefaultCode',
    'DefaultMessage',
    'FossilRepoError',
    'FossilRepoContext',
]


class ModelErrorContext(metaclass=immutable.Namespace):
    """Context for Model Errors"""
    FOSSIL_COMMIT: str = model_config.FOSSIL_COMMIT.path()
    FOSSIL_REPO: str = model_config.FOSSIL_REPO.path()
    FOSSIL_TIMELINE: str = model_config.FOSSIL_TIMELINE.path()

    @staticmethod
    def default_error(context: str):
        """Default Exception Context Code"""
        return f'{context}.{exception_config.Default.ERROR}'


class DefaultCode(metaclass=immutable.Namespace):
    """The Default Exception Codes for Model Exceptions."""
    fossil_repo: str = ModelErrorContext.default_error(
        ModelErrorContext.FOSSIL_REPO)
    fossil_commit: str = ModelErrorContext.default_error(
        ModelErrorContext.FOSSIL_COMMIT)
    fossil_timeline: str = ModelErrorContext.default_error(
        ModelErrorContext.FOSSIL_TIMELINE)


class DefaultMessage(metaclass=immutable.Namespace):
    """The Default Exception Messages for Model Exceptions."""
    base_message: str = (
        f'{base_exception_config.DefaultMessage.unexpected_error}'
        f'.{root.Module.model}'
    )
    fossil_repo: str = f'{base_message}.{root.Model.fossil_repo}'
    fossil_commit: str = f'{base_message}.{root.Model.fossil_commit}'
    fossil_timeline: str = f'{base_message}.{root.Model.fossil_timeline}'


class FossilRepoError(metaclass=immutable.Namespace):
    """Defined FossilRepo Errors"""
    init = 'init'
    immutable = 'immutable'
    not_implemented = 'not_implemented'


class FossilRepoContext(metaclass=immutable.Namespace):
    """FossilRepo Context

    Messages for FossilRepo.
    """
    _fields: Tuple[str] = (
        FossilRepoError.init,
        FossilRepoError.immutable,
        FossilRepoError.not_implemented,
    )
    init: str = f'{ModelErrorContext.FOSSIL_REPO}.__init__'
    immutable: str = f'{ModelErrorContext.FOSSIL_REPO}.immutable'
    not_implemented: str = f'{ModelErrorContext.FOSSIL_REPO}.not_implemented'


class FossilRepoDesc(metaclass=immutable.Namespace):
    """Find the Desc from the Error Type name."""
    _fields: Tuple[str] = (
        'type_error', 'value_error', 'empty_string', 'invalid_string',
        'non_path_object', 'invalid_path_string', 'path_resolution',
        'path_nonexistent', 'path_parent_nonexistent', 'path_file_error',
        'path_dir_error', 'path_unreadable', 'path_unwritable',
        'path_unexecutable'
    )
    type_error: str = exception_config.DESC_TYPE.string
    value_error: str = exception_config.DESC_TYPE.string
    empty_string: str = exception_config.DESC_TYPE.string
    invalid_string: str = exception_config.DESC_TYPE.string
    non_path_object: str = exception_config.DESC_TYPE.path
    non_path_object: str = exception_config.DESC_TYPE.path
    path_resolution: str = exception_config.DESC_TYPE.path
    path_nonexistent: str = exception_config.DESC_TYPE.path
    path_parent_nonexistent: str = exception_config.DESC_TYPE.path
    path_file_error: str = exception_config.DESC_TYPE.path
    path_dir_error: str = exception_config.DESC_TYPE.path
    path_unreadable: str = exception_config.DESC_TYPE.path
    path_unwritable: str = exception_config.DESC_TYPE.path
    path_unexecutable: str = exception_config.DESC_TYPE.path


class FossilRepoMessage(metaclass=immutable.Namespace):
    """"""
    str_path_usr_exception_config: str = (
        exception_config.Required.field_type(
            model_config.ConfigFossilRepo.field_name(), exception_config.DescType.string
        )
    )
    empty_str_user_exception_config: str = (
        exception_config.Required.field_type(
            model_config.ConfigFossilRepo.field_name(), exception_config.DescType.empty
        )
    )

    @staticmethod
    def str_path_exception_config(arg: str) -> str:
        return exception_config.Argument.message(
            FossilRepoContext.init,
            model_config.ConfigFossilRepo.field_name(),
            arg
        )

    @staticmethod
    def empty_str_exception_config(arg: str) -> str:
        return (

        )
