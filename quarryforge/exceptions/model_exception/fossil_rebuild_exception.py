"""RepoConfig Exception Module

#TODO
"""
from quarryforge.config.exception_conf.model_exception_conf import fossil_rebuild_conf
from quarryforge.exceptions.model_exception import base_model_exception


class UserTypeError(base_model_exception.FossilRebuildError, TypeError):
    """Raise for invalid user type."""
    def __init__(self, message=None):
        super().__init__(
            message or fossil_rebuild_conf.invalid_user())


class EmailTypeError(base_model_exception.FossilRebuildError, TypeError):
    """Raise for invalid email type."""
    def __init__(self, message=None):
        super().__init__(
            message or fossil_rebuild_conf.invalid_email())


class SrcRepoTypeError(base_model_exception.FossilRebuildError, TypeError):
    """Raise for invalid src_repo type."""
    def __init__(self, message=None):
        super().__init__(
            message or fossil_rebuild_conf.invalid_src())


class UpdateRepoTypeError(base_model_exception.FossilRebuildError, TypeError):
    """Raise for invalid update_repo type."""
    def __init__(self, message=None):
        super().__init__(
            message or fossil_rebuild_conf.invalid_update())


class UpdateDirTypeError(base_model_exception.FossilRebuildError, TypeError):
    """Raise for invalid update_dir type."""
    def __init__(self, message=None):
        super().__init__(
            message or fossil_rebuild_conf.invalid_update_dir())


class TemplateTypeError(base_model_exception.FossilRebuildError, TypeError):
    """Raise for invalid template type."""
    def __init__(self, message=None):
        super().__init__(
            message or fossil_rebuild_conf.invalid_update_dir())


class ProjectNameTypeError(base_model_exception.FossilRebuildError, TypeError):
    """Raise for invalid project_name type."""
    def __init__(self, message=None):
        super().__init__(
            message or fossil_rebuild_conf.project_name_invalid())


class ProjectDescTypeError(base_model_exception.FossilRebuildError, TypeError):
    """Raise for invalid project_desc type."""
    def __init__(self, message=None):
        super().__init__(
            message or fossil_rebuild_conf.project_desc_invalid())


class UserValueError(base_model_exception.FossilRebuildError, ValueError):
    """Raise for an empty user value."""
    def __init__(self, message=None):
        super().__init__(
            message or fossil_rebuild_conf.empty_user())


class EmailValueError(base_model_exception.FossilRebuildError, ValueError):
    """Raise for an empty email value."""
    def __init__(self, message=None):
        super().__init__(
            message or fossil_rebuild_conf.empty_email())


class ProjectNameValueError(
        base_model_exception.FossilRebuildError, ValueError):
    """Raise for an empty user value."""
    def __init__(self, message=None):
        super().__init__(
            message or fossil_rebuild_conf.empty_project_name())


class ProjectDescValueError(
        base_model_exception.FossilRebuildError, ValueError):
    """Raise for an empty user value."""
    def __init__(self, message=None):
        super().__init__(
            message or fossil_rebuild_conf.empty_project_desc())


class ImmutableRepoConfigError(
        base_model_exception.FossilRebuildError, TypeError):
    """Raise for any attempt to add or set attributes on RepoConfig."""
    def __init__(self, message=None):
        super().__init__(
            message or fossil_rebuild_conf.immutable_config())
