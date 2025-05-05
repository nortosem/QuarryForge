"""Models Configuration

#TODO
"""
from quarryforge.config.root import Valid


class ConfigArgString(Valid):
    """ArgString Configuration

    The slots for an ArgString.

    Attributes:
        NAME: the name of the command line argument for a string value
        VALUE: the string value provided with a command line argument
    """
    NAME = '_name'
    VALUE = '_value'


class ConfigFossilRepo(Valid):
    """FossilRepo Configuration

    The slots for a fossil repository.

    Attributes:
        FILE: the full path to a fossil repository
    """
    FILE = '_file'


class ConfigFossilRebuild(Valid):
    """Fossil Rebuild Configuration

    The slots for a FossilRebuild.

    Args:
        USER: username to use in update
        EMAIL: email contact for the update
        SRC_REPO: the source fossil repository name
        UPDATE_REPO: the updated fossil repository name
        UPDATE_DIR: the updated project directory
        TEMPLATE: the source repository for a config template
        PROJECT_NAME: the name ofthe project for updated repo
        PROJECT_DESC: the project description for updated repo
    """
    USER = '_user'
    EMAIL = '_email'
    SRC_REPO = '_src_repo'
    UPDATE_REPO = '_update_repo'
    UPDATE_DIR = '_update_dir'
    TEMPLATE = '_template'
    PROJECT_NAME = '_project_name'
    PROJECT_DESC = '_project_desc'


class ConfigCommit(Valid):
    """Commit Configuration

    The slots for a Commit.

    Attributes:
        HASH = uuid for a commit entry
        DATE = date for a commit entry
        AUTHOR = author for a commit entry
        COMMENT = comment for a commit entry
        BRANCH = branch for a commit entry
        TAGS = tags for a commit entry
        PHASE = phase for a commit entry
        CHANGES = changes for a commit entry
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
        SRC_REPO: slot for the source fossil repository to reconstruct
    """
    SRC_REPO = ConfigArgs.SRC_REPO.value


class ConfigInfo(Valid):
    """ConfigInfo

    The slots for a valid args to a fossil info command.

    Attributes:
        VERSION: slot for the specific version of commit uuid/hash
        SRC_REPO: slot for the source repository for a fossil info command
    """
    VERSION = 'version'
    SRC_REPO = ConfigArgs.SRC_REPO.value


class ConfigDiff(Valid):
    """ConfigDiff

    The slots for a valid args to a fossil diff command.

    Attributes:
        PARENT: slot for the parent uuid/hash of the --from in fossil diff
        CHILD: slot for the child uuid/hash of hte --to in fossil diff
        SRC_REPO: slot for the source repository for a fossil diff command
    """
    PARENT = 'parent'
    CHILD = 'child'
    SRC_REPO = ConfigArgs.SRC_REPO.value


class ConfigCat(Valid):
    """ConfigCat

    The slots for a valid args to a fossil cat command.

    Attributes:
        FILENAME: slot for a filename in a repository
        OUTFILE: slot for a output filename in a repository
        VERSION: slot for the uuid/hash of a file commit
        SRC_REPO: slot for the source fossil repository to reconstruct
    """
    FILENAME = 'filename'
    OUTFILE = 'outfile'
    VERSION = ConfigInfo.VERSION.value
    SRC_REPO = ConfigArgs.SRC_REPO.value


class ConfigTimeline(Valid):
    """Timeline Config

    Defines the slots for a TimelineArg

    Attributes:
        SRC_REPO: slot for the source fossil repository to reconstruct
    """
    SRC_REPO = 'src_repo'
