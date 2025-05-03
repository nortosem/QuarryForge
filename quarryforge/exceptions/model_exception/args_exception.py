"""Args Exception Module


"""
from quarryforge.config.exception_conf.models_exception \
    import args_config_error_conf
from quarryforge.exceptions.model_exception import base_models_exception


class InfoVersionTypeError(base_models_exception.InfoArgsError, TypeError):
    """Raise for invalid version type"""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.invalid_info_version())


class InfoRepoTypeError(base_models_exception.InfoArgsError, TypeError):
    """Raise for invalid src_repo type"""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.invalid_info_repo()
        )

class InfoVersionValueError(base_models_exception.InfoArgsError, ValueError):
    """Raise for empty version"""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.empty_info_version()
        )

class InfoRepoValueError(base_models_exception.InfoArgsError, ValueError):
    """Raise for empty src_repoe"""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.empty_info_repo()
        )

class ImmutableInfoArgsError(base_models_exception.InfoArgsError, TypeError):
    """Raise for any attempt to add or set attributes on InfoArgs."""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.immutable_info_config()
        )

class DiffParentTypeError(base_models_exception.DiffArgsError, TypeError):
    """Raise for invalid parent type"""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.invalid_diff_parent()
        )

class DiffParentValueError(base_models_exception.DiffArgsError, ValueError):
    """Raise for empty parent type"""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.empty_diff_parent()
        )

class DiffChildTypeError(base_models_exception.DiffArgsError, TypeError):
    """Raise for invalid child type"""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.invalid_diff_child()
        )

class DiffChildValueError(base_models_exception.DiffArgsError, ValueError):
    """Raise for empty child type"""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.empty_diff_child()
        )

class DiffRepoTypeError(base_models_exception.DiffArgsError, TypeError):
    """Raise for invalid src_repo type"""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.invalid_diff_repo()
        )

class DiffRepoValueError(base_models_exception.DiffArgsError, ValueError):
    """Raise for empty src_repo type"""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.empty_diff_repo()
        )

class ImmutableDiffArgsError(base_models_exception.DiffArgsError, TypeError):
    """Raise for any attempt to add or set attributes on InfoArgs."""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.immutable_diff_args()
        )

class CatInFileTypeError(base_models_exception.CatArgsError, TypeError):
    """Raise for invalid input filename type."""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.invalid_cat_infile()
        )

class CatOutFileTypeError(base_models_exception.CatArgsError, TypeError):
    """Raise for invalid output filename type."""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.invalid_cat_outfile()
        )

class CatVersionTypeError(base_models_exception.CatArgsError, TypeError):
    """Raise for invalid version type."""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.invalid_cat_version()
        )

class CatInFileValueError(base_models_exception.CatArgsError, ValueError):
    """Raise for empty input filename."""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.empty_cat_infile()
        )

class CatOutFileValueError(base_models_exception.CatArgsError, ValueError):
    """Raise for empty output filename."""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.empty_cat_outfile()
        )

class CatOutFileDirError(base_models_exception.CatArgsError, TypeError):
    """Raise for output filename path being a directory."""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.outfile_cat_dir_error()
        )

class CatVersionValueError(base_models_exception.CatArgsError, ValueError):
    """Raise for empty version argument."""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.empty_cat_version()
        )

class CatRepoTypeError(base_models_exception.CatArgsError, TypeError):
    """Raise for invalid src_repo type."""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.invalid_cat_repo()
        )

class CatRepoValueError(base_models_exception.CatArgsError, ValueError):
    """Raise for empty src_repo."""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.empty_cat_repo())


class ImmutableCatArgsError(base_models_exception.CatArgsError, TypeError):
    """Raise for any attempt to add or set attributes on InfoArgs."""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.immutable_cat_args())


class GetTimelineArgTypeError(
        base_models_exception.GetTimelineArgError, TypeError):
    """Raise for invalid src_repo type."""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.missing_user())


class GetTimelineArgValueError(
        base_models_exception.GetTimelineArgError, ValueError):
    """Raise for empty src_repo type."""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.missing_user())


class ImmutableGetTimelineArgError(
        base_models_exception.GetTimelineArgError, TypeError):
    """Raise for any attempt to add or set attributes on GetTimelineArg."""
    def __init__(self, message=None):
        super().__init__(
            message or args_config_error_conf.immutable_get_timeline_arg())
