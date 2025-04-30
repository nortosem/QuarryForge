"""RepoConfig Exception Module

#TODO
"""
import quarryforge.config.exception_conf.models_exception.repo_config_error_conf
from quarryforge.exceptions.model_exception.base_models_exception \
    import RepoConfigError


class UserTypeError(RepoConfigError, TypeError):
    """Raise for invalid user type."""
    def __init__(self, message=None):
        super().__init__(
            message or repo_config_error_conf.missing_user()
        )


class EmailTypeError(RepoConfigError, TypeError):
    """Raise for invalid email type."""
    def __init__(self, message=None):
        super().__init__(
            message or repo_config_error_conf.missing_email()
        )


class SrcRepoTypeError(RepoConfigError, TypeError):
    """Raise for invalid src_repo type."""
    def __init__(self, message=None):
        super().__init__(
            message or repo_config_error_conf.missing_src()
        )


class UpdateRepoTypeError(RepoConfigError, TypeError):
    """Raise for invalid update_repo type."""
    def __init__(self, message=None):
        super().__init__(
            message or repo_config_error_conf.missing_update()
        )


class UpdateDirTypeError(RepoConfigError, TypeError):
    """Raise for invalid update_dir type."""
    def __init__(self, message=None):
        super().__init__(
            message or repo_config_error_conf.missing_update_dir()
        )


class TemplateTypeError(RepoConfigError, TypeError):
    """Raise for invalid template type."""
    def __init__(self, message=None):
        super().__init__(
            message or repo_config_error_conf.missing_update_dir()
        )


class ProjectNameTypeError(RepoConfigError, TypeError):
    """Raise for invalid project_name type."""
    def __init__(self, message=None):
        super().__init__(
            message or repo_config_error_conf.project_name_invalid()
        )


class ProjectDescTypeError(RepoConfigError, TypeError):
    """Raise for invalid project_desc type."""
    def __init__(self, message=None):
        super().__init__(
            message or repo_config_error_conf.project_desc_invalid()
        )


class UserValueError(RepoConfigError, ValueError):
    """Raise for an empty user value."""
    def __init__(self, message=None):
        super().__init__(
            message or repo_config_error_conf.empty_user()
        )


class EmailValueError(RepoConfigError, ValueError):
    """Raise for an empty email value."""
    def __init__(self, message=None):
        super().__init__(
            message or repo_config_error_conf.empty_email()
        )


class ProjectNameValueError(RepoConfigError, ValueError):
    """Raise for an empty user value."""
    def __init__(self, message=None):
        super().__init__(
            message or repo_config_error_conf.empty_project_name()
        )


class ProjectDescValueError(RepoConfigError, ValueError):
    """Raise for an empty user value."""
    def __init__(self, message=None):
        super().__init__(
            message or repo_config_error_conf.empty_project_desc()
        )


class ImmutableRepoConfigError(RepoConfigError):
    """Raise for any attempt to add or set attributes on RepoConfig."""
    def __init__(self, message=None):
        super().__init__(
            message or repo_config_error_conf.immutable_config()
        )
