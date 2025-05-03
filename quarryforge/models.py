"""models

#todo
"""
from pathlib import Path

#from quarryforge.config import Command
from quarryforge.config import InfoData
from quarryforge.config import TimelineData

from quarryforge.config.models_conf import ConfigArgs
from quarryforge.config.models_conf import ConfigCat
from quarryforge.config.models_conf import ConfigCommit
from quarryforge.config.models_conf import ConfigDiff
from quarryforge.config.models_conf import ConfigGetTimelineArg
from quarryforge.config.models_conf import ConfigInfo
#from quarryforge.config.models_conf import ConfigTimeline

from quarryforge.exceptions.model_exceptions import args_exception
from quarryforge.exceptions.model_exception import base_models_exception
from quarryforge.exceptions.model_exceptions import commit_exception
from quarryforge.exceptions.model_exceptions import repo_config_exception
from quarryforge.exceptions.model_exception.base_models_exception \
    import CommitError

from quarryforge.util import get_parent_hash

from quarryforge.util.model_util import check_list_type
from quarryforge.util.model_util import check_list_content
from quarryforge.util.model_util import is_not_empty
from quarryforge.util.model_util import is_valid_path_type
from quarryforge.util.model_util import is_valid_str_type
from quarryforge.util.model_util import viable_source
from quarryforge.util.model_util import viable_output
from quarryforge.util.model_util import viable_update_dir


import subprocess
from subprocess import CalledProcessError
from subprocess import CompletedProcess

from typing import List
from typing import Optional


class RepoConfig:
    """RepoConfig

    Validate and Stores a valid config obtained from a parsed toml file.

    RepoConfig holds settings for rebuilding a fossil repository with updated
    user information, repository paths, and project details.

    Attributes:
        user (str): Username.
        emai (str)l: User email.
        src_repo (Path): Path to the source repository.
        update_repo (Path): Path to the updated repository.
        update_dir (Path): Path to the updated project direcory.
        template (Path): Path for the source repository template.
        project_name (str): Name of the project.
        project_desc (str): Description of the project.
    """
    __slots__ = ConfigArgs.slots()

    def __init__(self,
                 user: str,
                 email: str,
                 src_repo: Path,
                 update_repo: Path,
                 update_dir: Path,
                 template: Optional[Path] = None,
                 project_name: Optional[str] = None,
                 project_desc: Optional[str] = None):
        """Validate and initialize a Repository Configuration."""
        user = is_valid_str_type(user, repo_config_exception.UserTypeError)
        user = is_not_empty(user, repo_config_exception.UserValueError)
        email = is_valid_str_type(email, repo_config_exception.EmailTypeError)
        email = is_not_empty(email, repo_config_exception.EmailValueError)
        # email regex check TODO
        #TODO create fossil file validation function
        src_repo = is_valid_path_type(
            src_repo,
            repo_config_exception.SrcRepoTypeError)
        src_repo = viable_source(
            src_repo, base_models_exception.RepoConfigError)
        update_repo = is_valid_path_type(
            update_repo, repo_config_exception.UpdateRepoTypeError)
        update_repo = viable_output(
            update_repo, base_models_exception.RepoConfigError)
        update_dir = is_valid_path_type(
            update_repo, repo_config_exception.UpdateDirTypeError)
        update_dir = viable_update_dir(
            update_dir, base_models_exception.RepoConfigError)
        if template is not None:
            template = is_valid_path_type(
                template, repo_config_exception.TemplateTypeError)
            template = viable_source(
                template, base_models_exception.RepoConfigError)
        if project_name is not None:
            project_name = is_valid_str_type(
                project_name,
                repo_config_exception.ProjectNameTypeError)
            project_name = is_not_empty(
                project_name,
                repo_config_exception.ProjectNameValueError)
        if project_desc is not None:
            project_desc = is_valid_str_type(
                project_desc, repo_config_exception.ProjectDescTypeError)
            project_desc = is_not_empty(
                project_desc, repo_config_exception.ProjectDescValueError)

        object.__setattr__(self, ConfigArgs.USER.value, user)
        object.__setattr__(self, ConfigArgs.EMAIL.value, email)
        object.__setattr__(self, ConfigArgs.SRC_REPO.value, src_repo)
        object.__setattr__(self, ConfigArgs.UPDATE_REPO.value, update_repo)
        object.__setattr__(self, ConfigArgs.UPDATE_DIR.value, update_dir)
        object.__setattr__(self, ConfigArgs.TEMPLATE.value, template)
        object.__setattr__(self, ConfigArgs.PROJECT_NAME.value, project_name)
        object.__setattr__(self, ConfigArgs.PROJECT_DESC.value, project_desc)


    def __setattr__(self, name, value):
        """Repository configurations are immutable"""
        raise repo_config_exception.ImmutableRepoConfigError()

    def __deltattr__(self, name):
        """Repository configurations are immutable"""
        raise args_exception.ImmutableRepoConfigError()


class InfoArgs:
    """InfoArgs

    The valid arguments for the fossil diff command.
    This is used to find the check-in parent of a commit.
    If no parent hash is in the results then this is the initial empty commit
    of the fossil repository.

    Attributes:
        version: (str): The specific check-in hash to get parent.
        src_repo (Path): Path to the source repository.
    """
    __slots__ = ConfigInfo.slots()

    def __init__(self, version: str, src_repo: Path):

        version = is_valid_str_type(
            version, args_exception.InfoVersionTypeError)
        version = is_not_empty(
            version, args_exception.InfoVersionValueError)
        src_repo = is_valid_path_type(
            src_repo, args_exception.InfoRepoTypeError)
        src_repo = viable_source(
            src_repo, base_models_exception.InfoArgsError)

        object.__setattr__(self, ConfigInfo.VERSION.value, version)
        object.__setattr__(self, ConfigInfo.SRC_REPO.value, src_repo)

    def __setattr__(self, name, value):
        """Fossil info args are immutable."""
        raise args_exception.ImmutableInfoArgsError()

    def __delattr__(self, name):
        """Fossil info args are immutable."""
        raise args_exception.ImmutableInfoArgsError()


class DiffArgs:
    """DiffArgs

    The valid arguments for a fossil diff command.
    The arguments used to get all of the files changed for a specific commit.

    Attributes:
        parent (str): The preceding check-in.
        child (str): The following check-in.
        src_repo (Path): Path to the source repository.
    """
    __slots__ = ConfigDiff.slots()

    def __init__(self, parent: str, child: str, src_repo: Path):

        parent = is_valid_str_type(
            parent, args_exception.DiffParentTypeError)
        parent = is_not_empty(
            parent, args_exception.DiffParentValueError)
        child = is_valid_str_type(
            child, args_exception.DiffChildTypeError)
        child = is_not_empty(
            child, args_exception.DiffChildValueError)
        src_repo = is_valid_path_type(
            src_repo, args_exception.DiffRepoTypeError)
        src_repo = viable_source(
            src_repo, base_models_exception.DiffRepoValueError)

        object.__setattr__(self, ConfigDiff.PARENT.value, parent)
        object.__setattr__(self, ConfigDiff.CHILD.value, child)
        object.__setattr__(self, ConfigDiff.SRC_REPO.value, src_repo)

    def __setattr__(self, name, value):
        """Fossil diff args are immutable."""
        raise args_exception.ImmutableDiffArgsError()

    def __delattr__(self, name):
        """Fossil diff args are immutable."""
        raise args_exception.ImmutableDiffArgsError()


class CatArgs:
    """CatArgs

    The valid arguments for a fossil cat command.
    The arguments to retrieve the file content changed for a commit.

    Attributes:
        filename (str): Name
    """
    __slots__ = ConfigCat.slots()

    def __init__(self, filename, outfile, version, src_repo):

        filename = is_valid_path_type(
            filename, args_exception.CatInFileTypeError)
        filename = viable_source(
            filename, args_exception.CatInFileValueError)
        outfile = is_valid_path_type(
            outfile, args_exception.CatOutFileTypeError)
        outfile = viable_output(
            outfile, args_exception.CatOutFileValueError)
        version = is_valid_str_type(
            version, args_exception.CatVersionTypeError)
        version = is_not_empty(
            version, args_exception.CatVersionValueError)
        src_repo = is_valid_path_type(
            src_repo, args_exception.CatRepoTypeError)
        src_repo = viable_source(
            src_repo, base_models_exception.CatRepoValueError)

        object.__setattr__(self, ConfigCat.FILENAME.value, filename)
        object.__setattr__(self, ConfigCat.OUTFILE.value, outfile)
        object.__setattr__(self, ConfigCat.VERSION.value, version)
        object.__setattr__(self, ConfigCat.SRC_REPO.value, src_repo)

    def __setattr__(self, name, value):
        """Fossil cat args are immutable."""
        raise args_exception.ImmutableCatArgsError()

    def __delattr__(self, name):
        """Fossil cat args are immutable."""
        raise args_exception.ImmutableCatArgsError()


class GetTimelineArg:
    """GetTimelineArg

    This arg is to get the complete raw timeline from a fossil repo.

    Attributes:
        src_repo (Path): Path to the source repo to update.
    """
    __slots__ = ConfigGetTimelineArg.slots()

    def __init__(self, src_repo: Path):

        src_repo = is_valid_path_type(
            src_repo, args_exception.GetTimelineArgTypeError)
        src_repo = viable_source(
            src_repo, base_models_exception.GetTimelineArgValueError)

        object.__setattr__(self, ConfigGetTimelineArg.SRC_REPO.value, src_repo)

    def __setattr__(self, name, value):
        """Fossil cat args are immutable."""
        raise args_exception.ImmutableGetTimelineArgError()

    def __delattr__(self, name):
        """Fossil cat args are immutable."""
        raise args_exception.ImmutableGetTimelineArgError()


class Commit:
    """Commit

    #todo
    """
    __slots__ = ConfigCommit.slots()

    def __init__(self,
                 uuid: str,
                 date: str,
                 author: str,
                 comment: str,
                 branch: str,
                 tags: Optional[List[str]] = None,
                 phase: str = None,
                 changes: Optional[List[str]] = None):

        uuid = is_valid_str_type(uuid, commit_exception.UuidTypeError)
        uuid = is_not_empty(uuid, commit_exception.UuidValueError)
        date = is_valid_str_type(date, commit_exception.DateTypeError)
        date = is_not_empty(date, commit_exception.DateValueError)
        author = is_valid_str_type(author, commit_exception.AuthorTypeError)
        author = is_not_empty(author, commit_exception.AuthorValueError)
        comment = is_valid_str_type(comment, commit_exception.CommentTypeError)
        comment = is_not_empty(comment, commit_exception.CommentValueError)
        branch = is_valid_str_type(branch, commit_exception.BranchTypeError)
        branch = is_not_empty(uuid, commit_exception.BranchValueError)

        object.__setattr__(self, ConfigCommit.HASH.value, uuid)
        object.__setattr__(self, ConfigCommit.DATE.value, date)
        object.__setattr__(self, ConfigCommit.AUTHOR.value, author)
        object.__setattr__(self, ConfigCommit.COMMENT.value, comment)
        object.__setattr__(self, ConfigCommit.BRANCH.value, branch)

        tags = check_list_type(tags, commit_exception.TagsListError)
        tags = check_list_content(tags, commit_exception.TagsCommitError)
        object.__setattr__(self, ConfigCommit.TAGS.value, tags)

        object.__setattr__(self, ConfigCommit.PHASE.value, phase)

        changes = check_list_type(changes, commit_exception.ChangesTypeError)
        changes = check_list_content(changes, commit_exception.ChangeValueError)
        if changes is not None:
            changes = is_valid_str_type(changes,
                commit_exception.ChangesTypeError)
            changes = is_not_empty(changes,
                commit_exception.ChangesValueError)
            object.__setattr__(self,ConfigCommit.CHANGES.value,changes)
        if changes is None:
            object.__setattr__(self, ConfigCommit.CHANGES.value, [])

    def __setattr__(self, name, value):
        """Commits are Immutable"""
        raise commit_exception.ImmutableCommitError()

    def __delattr__(self, name):
        """Commits are Immutable"""
        raise commit_exception.ImmutableCommitError()

    def __repr__(self):
        """Official String Represenation of a Commit"""
        #todo unquote list args && quote str args
        attributes = ', '.join(
            f"{slot}={getattr(self,slot)}" for slot in self.__slots__)
        return f'{self.__class__.__name__}({attributes})'

    def __str__(self):
        """Standard string output for a Commit."""
        uuid = self.uuid[:12]
        return f'uuid: {uuid}\ns ate: {self.date}\ncomment: {self.comment}'

    def get_hash(self):
        """Get Brief Commit Hash"""
        return self.uuid[:12]

    def get_parent(self, args: InfoArgs) -> str:
        """Get Parent Commit

        #todo
        """
        try:
            info_process: CompletedProcess[bytes] = subprocess.run(
                get_parent_hash(args),capture_output=True,check=True
            )
        except CalledProcessError as cpe:
            raise CalledProcessError(
                cpe.returncode, cpe.cmd, cpe.stdout,
                f'Fossil Info Process Exception: {cpe}'
            ) from cpe
        raw_parent_hash = info_process.stdout.decode()
        initial_commit = InfoData.init_pattern()
        commit_parent = InfoData.parent_pattern()
        match_init = initial_commit.match(raw_parent_hash)
        match_parent = commit_parent.match(raw_parent_hash)
        if match_parent:
            return match_parent.group(ConfigCommit.HASH.value)
        if match_init:
            return None
        else:
            raise CommitError('unexpected error')

class Timeline:
    """Timeline

    A collection of timeline data structures representing all commits made to
    a fossil repository.
    """
    __slots__ = tuple(TimelineData.COMMITS.value)

    def __init__(self, commits: List = None):
        self.commits = commits

    def add(self, commit: Commit):
        self.commits.append(commit)

    def reverse(self) -> List[Commit]:
        """Reverse Commit Order

        Default order is latest commit first.
        Reverse once return commits in order from iniital commit.
        """
        self.commits.reverse()
        return self.commits
