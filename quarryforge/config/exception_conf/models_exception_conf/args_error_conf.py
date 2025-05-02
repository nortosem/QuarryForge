"""Args Error Configuration


"""
from pathlib import Path
from quarryforge.config.exception_conf.fault_builder import Required
from quarryforge.config.exception_conf.fault_builder import Immutable
from quarryforge.config.exception_conf.fault_builder import PathMessage
from quarryforge.config.models_conf import ConfigInfo
from quarryforge.config.models_conf import ConfigDiff
from quarryforge.config.models_conf import ConfigCat
from quarryforge.config.models_conf import ConfigGetTimelineArg
from quarryforge.config.root import ModelNames as Model


def invalid_info_version():
    """Invalid InfoArgs version string argument"""
    return Required.field_type(ConfigInfo.VERSION, str)


def invalid_info_repo():
    """Invalid InfoArgs repository path argument"""
    return Required.field_type(ConfigInfo.SRC_REPO, Path)


def empty_info_version():
    """InfoArgs version cannot be empty"""
    return Required.field_empty(ConfigInfo.VERSION, str)


def empty_info_repo():
    """InfoArgs src_repo cannot be empty"""
    return Required.field_empty(ConfigInfo.SRC_REPO, Path)


def immutable_info_args() -> str:
    """The InfoArgs is immutable message."""
    return Immutable.error_message(Model.INFO_ARGS)


def invalid_diff_parent():
    """Invalid DiffArgs parent type argument"""
    return Required.field_type(ConfigDiff.PARENT, str)


def empty_diff_parent():
    """DiffArgs parent cannot be empty"""
    return Required.field_empty(ConfigDiff.PARENT, str)


def invalid_diff_child():
    """Invalid DiffArgs child type argument"""
    return Required.field_type(ConfigDiff.CHILD, str)


def empty_diff_child():
    """DiffArgs child cannot be empty"""
    return Required.field_empty(ConfigDiff.CHILD, str)


def invalid_diff_repo():
    """Invalid DiffArgs src_repo type argument"""
    return Required.field_type(ConfigDiff.SRC_REPO, Path)


def empty_diff_repo():
    """DiffArgs src_repo cannot be empty"""
    return Required.field_empty(ConfigDiff.SRC_REPO, Path)


def immutable_diff_args() -> str:
    """The DiffArgs is immutable message."""
    return Immutable.error_message(Model.DIFF_ARGS)


def invalid_cat_infile():
    """Invalid CatArgs input filename argument"""
    return Required.field_type(ConfigCat.FILENAME, Path)


def empty_cat_infile():
    """CatArgs filename cannot be empty"""
    return Required.field_empty(ConfigCat.FILENAME, Path)


def invalid_cat_outfile():
    """Invalid CatArgs output filename argument"""
    return Required.field_empty(ConfigCat.OUTFILE, Path)


def outfile_cat_dir_error():
    """CatArgs outfile filename cannot be a directory"""
    return PathMessage.dir_not_allowed(Config.OUTFILE.value)


def empty_cat_outfile():
    """CatArgs output filename cannot be empty"""
    return PathMessage.field_empty(ConfigCat.OUTFILE, Path)


def invalid_cat_version():
    """Invalid CatArgs version argument"""
    return Required.field_type(ConfigCat.VERSION, str)


def empty_cat_version():
    """CatArgs version cannot be empty"""
    return Required.field_empty(ConfigCat.VERSION, str)


def invalid_cat_repo():
    """Invalid CatArgs src_repo argument"""
    return Required.field_type(ConfigCat.SRC_REPO, Path)


def empty_cat_repo():
    """CatArgs src_repo cannot be empty"""
    return Required.field_empty(ConfigCat.SRC_REPO, Path)


def immutable_cat_args() -> str:
    """The CatArgs is immutable message."""
    return Immutable.error_message(Model.CAT_ARGS)


def invalid_get_timeline_repo() -> str:
    """Invalid GetTimelineArg src_repo type"""
    return Required.field_type(ConfigGetTimelineArg.SRC_REPO, Path)


def empty_get_timeline_repo() -> str:
    """GetTimelineArg src_repo cannot be empty"""
    return Required.field_empty(ConfigGetTimelineArg.SRC_REPO, Path)


def immutable_get_timeline_arg() -> str:
    """GetTimelineArg is immutable message"""
    return Immutable.error_message(Model.GET_TIMELINE_ARG)
