"""Models Configuration

#TODO
"""
from quarryforge.config.root import Valid


class ConfigArgs(Valid):
    """Configuration Arguments

    The slots for a Repo Config.

    Args:
        user (str): Username.
        emai (str)l: User email.
        src_repo (Path): Path to the source repository.
        update_repo (Path): Path to the updated repository.
        update_dir (Path): Path to the updated project direcory.
        template (Path): Path for the source repository template.
        project_name (str): Name of the project.
        project_desc (str): Description of the project.
    """
    USER = 'user'
    EMAIL = 'email'
    SRC_REPO = 'src_repo'
    UPDATE_REPO = 'update_repo'
    UPDATE_DIR = 'update_dir'
    TEMPLATE = 'template'
    PROJECT_NAME = 'project_name'
    PROJECT_DESC = 'project_desc'


class ConfigCommit(Valid):
    """Commit Configuration

    The slots for a Commit.
    """
    HASH = 'uuid'
    DATE = 'date'
    AUTHOR = 'author'
    COMMENT = 'comment'
    BRANCH = 'branch'
    TAGS = 'tags'
    PHASE = 'phase'
    CHANGES = 'changes'


class ConfigGetTimelineArg(Valid):
    """GetConfigTimelineArg

    Defines the slots for a GetTimelineArg.

    Attributes:
        src: (Path): pathlib.Path location of the fossil repo to reconstruct.
    """
    SRC_REPO = ConfigArgs.SRC_REPO.value


class ConfigInfo(Valid):
    """ConfigInfo

    The slots for a valid args to a fossil info command.
    """
    VERSION = 'version'
    SRC_REPO = ConfigArgs.SRC_REPO.value

#initial empty check-in
class ConfigDiff(Valid):
    """ConfigDiff

    The slots for a valid args to a fossil diff command.
    """
    PARENT = 'parent'
    CHILD = 'child'
    SRC_REPO = ConfigArgs.SRC_REPO.value


class ConfigCat(Valid):
    """ConfigCat

    The slots for a valid args to a fossil cat command.
    """
    FILENAME = 'filename'
    OUTFILE = 'outfile'
    VERSION = ConfigInfo.VERSION.value
    SRC_REPO = ConfigArgs.SRC_REPO.value


class ConfigTimeline(Valid):
    """Timeline Config

    Defines the slots for a TimelineArg

    Attributes:
        src: (Path): pathlib.Path location of the fossil repo to reconstruct.
    """
    SRC_REPO = 'src_repo'
