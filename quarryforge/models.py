"""models

#todo
"""
from pathlib import Path
import subprocess
from typing import List, Optional

from quarryforge import config
from quarryforge.config import models_config
from quarryforge.exceptions import model_exception
from quarryforge.exceptions.model_exception import args_exception
from quarryforge.exceptions.model_exception import base_models_exception
from quarryforge.exceptions.model_exception import commit_exception
from quarryforge.exceptions.model_exception import repo_config_exception
from quarryforge.util import fossil_util
from quarryforge.util import model_util


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

    #TODO email regex check
    #TODO create fossil file validation function
    """
    __slots__ = models_config.ConfigArgs.slots()

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
        user = model_util.is_valid_str_type(
            user, repo_config_exception.UserTypeError)
        user = model_util.is_not_empty(
            user, repo_config_exception.UserValueError)
        email = model_util.is_valid_str_type(
            email, repo_config_exception.EmailTypeError)
        email = model_util.is_not_empty(
            email, repo_config_exception.EmailValueError)

        src_repo = model_util.is_valid_path_type(
            src_repo,
            repo_config_exception.SrcRepoTypeError)
        src_repo = model_util.viable_source(
            src_repo, base_models_exception.RepoConfigError)
        update_repo = model_util.is_valid_path_type(
            update_repo, repo_config_exception.UpdateRepoTypeError)
        update_repo = model_util.viable_output(
            update_repo, base_models_exception.RepoConfigError)
        update_dir = model_util.is_valid_path_type(
            update_repo, repo_config_exception.UpdateDirTypeError)
        update_dir = model_util.viable_update_dir(
            update_dir, base_models_exception.RepoConfigError)
        if template is not None:
            template = model_util.is_valid_path_type(
                template, repo_config_exception.TemplateTypeError)
            template = model_util.viable_source(
                template, base_models_exception.RepoConfigError)
        if project_name is not None:
            project_name = model_util.is_valid_str_type(
                project_name,
                repo_config_exception.ProjectNameTypeError)
            project_name = model_util.is_not_empty(
                project_name,
                repo_config_exception.ProjectNameValueError)
        if project_desc is not None:
            project_desc = model_util.is_valid_str_type(
                project_desc, repo_config_exception.ProjectDescTypeError)
            project_desc = model_util.is_not_empty(
                project_desc, repo_config_exception.ProjectDescValueError)

        object.__setattr__(self, models_config.ConfigArgs.USER.value, user)
        object.__setattr__(self, models_config.ConfigArgs.EMAIL.value, email)
        object.__setattr__(self, models_config.ConfigArgs.SRC_REPO.value, src_repo)
        object.__setattr__(
            self, models_config.ConfigArgs.UPDATE_REPO.value, update_repo)
        object.__setattr__(
            self, models_config.ConfigArgs.UPDATE_DIR.value, update_dir)
        object.__setattr__(
            self, models_config.ConfigArgs.TEMPLATE.value, template)
        object.__setattr__(
            self, models_config.ConfigArgs.PROJECT_NAME.value, project_name)
        object.__setattr__(
            self, models_config.ConfigArgs.PROJECT_DESC.value, project_desc)


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
    __slots__ = models_config.ConfigInfo.slots()

    def __init__(self, version: str, src_repo: Path):

        version = model_util.is_valid_str_type(
            version, args_exception.InfoVersionTypeError)
        version = model_util.is_not_empty(
            version, args_exception.InfoVersionValueError)
        src_repo = model_util.is_valid_path_type(
            src_repo, args_exception.InfoRepoTypeError)
        src_repo = model_util.viable_source(
            src_repo, base_models_exception.InfoArgsError)

        object.__setattr__(
            self, models_config.ConfigInfo.VERSION.value, version)
        object.__setattr__(
            self, models_config.ConfigInfo.SRC_REPO.value, src_repo)

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
    __slots__ = models_config.ConfigDiff.slots()

    def __init__(self, parent: str, child: str, src_repo: Path):

        parent = model_util.is_valid_str_type(
            parent, args_exception.DiffParentTypeError)
        parent = model_util.is_not_empty(
            parent, args_exception.DiffParentValueError)
        child = model_util.is_valid_str_type(
            child, args_exception.DiffChildTypeError)
        child = model_util.is_not_empty(
            child, args_exception.DiffChildValueError)
        src_repo = model_util.is_valid_path_type(
            src_repo, args_exception.DiffRepoTypeError)
        src_repo = model_util.viable_source(
            src_repo, base_models_exception.DiffRepoValueError)

        object.__setattr__(self, models_config.ConfigDiff.PARENT.value, parent)
        object.__setattr__(self, models_config.ConfigDiff.CHILD.value, child)
        object.__setattr__(
            self, models_config.ConfigDiff.SRC_REPO.value, src_repo)

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
    __slots__ = models_config.ConfigCat.slots()

    def __init__(self, filename, outfile, version, src_repo):

        filename = model_util.is_valid_path_type(
            filename, args_exception.CatInFileTypeError)
        filename = model_util.viable_source(
            filename, args_exception.CatInFileValueError)
        outfile = model_util.is_valid_path_type(
            outfile, args_exception.CatOutFileTypeError)
        outfile = model_util.viable_output(
            outfile, args_exception.CatOutFileValueError)
        version = model_util.is_valid_str_type(
            version, args_exception.CatVersionTypeError)
        version = model_util.is_not_empty(
            version, args_exception.CatVersionValueError)
        src_repo = model_util.is_valid_path_type(
            src_repo, args_exception.CatRepoTypeError)
        src_repo = model_util.viable_source(
            src_repo, base_models_exception.CatRepoValueError)

        object.__setattr__(
            self, models_config.ConfigCat.FILENAME.value, filename)
        object.__setattr__(
            self, models_config.ConfigCat.OUTFILE.value, outfile)
        object.__setattr__(
            self, models_config.ConfigCat.VERSION.value, version)
        object.__setattr__(
            self, models_config.ConfigCat.SRC_REPO.value, src_repo)

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
    __slots__ = models_config.ConfigGetTimelineArg.slots()

    def __init__(self, src_repo: Path):

        src_repo = model_util.is_valid_path_type(
            src_repo, args_exception.GetTimelineArgTypeError)
        src_repo = model_util.viable_source(
            src_repo, base_models_exception.GetTimelineArgValueError)

        object.__setattr__(
            self, models_config.ConfigGetTimelineArg.SRC_REPO.value, src_repo)

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
    __slots__ = models_config.ConfigCommit.slots()

    def __init__(self,
                 uuid: str,
                 date: str,
                 author: str,
                 comment: str,
                 branch: str,
                 tags: Optional[List[str]] = None,
                 phase: str = None,
                 changes: Optional[List[str]] = None):

        uuid = model_util.is_valid_str_type(
            uuid, commit_exception.UuidTypeError)
        uuid = model_util.is_not_empty(uuid, commit_exception.UuidValueError)

        date = model_util.is_valid_str_type(
            date, commit_exception.DateTypeError)
        date = model_util.is_not_empty(date, commit_exception.DateValueError)

        author = model_util.is_valid_str_type(
            author, commit_exception.AuthorTypeError)
        author = model_util.is_not_empty(
            author, commit_exception.AuthorValueError)

        comment = model_util.is_valid_str_type(
            comment, commit_exception.CommentTypeError)
        comment = model_util.is_not_empty(comment, commit_exception.CommentValueError)

        branch = model_util.is_valid_str_type(
            branch, commit_exception.BranchTypeError)
        branch = model_util.is_not_empty(
            uuid, commit_exception.BranchValueError)

        object.__setattr__(self, models_config.ConfigCommit.HASH.value, uuid)
        object.__setattr__(self, models_config.ConfigCommit.DATE.value, date)
        object.__setattr__(
            self, models_config.ConfigCommit.AUTHOR.value, author)
        object.__setattr__(
            self, models_config.ConfigCommit.COMMENT.value, comment)
        object.__setattr__(
            self, models_config.ConfigCommit.BRANCH.value, branch)

        tags = model_util.check_list_type(tags, commit_exception.TagsListError)
        tags = model_util.check_list_content(
            tags, commit_exception.TagsCommitError)
        object.__setattr__(self, models_config.ConfigCommit.TAGS.value, tags)

        object.__setattr__(self, models_config.ConfigCommit.PHASE.value, phase)

        changes = model_util.check_list_type(
            changes, commit_exception.ChangesTypeError)
        changes = model_util.check_list_content(
            changes, commit_exception.ChangeValueError)

        if changes is not None:
            changes = model_util.is_valid_str_type(
                changes, commit_exception.ChangesTypeError)
            changes = model_util.is_not_empty(
                changes, commit_exception.ChangesValueError)
            object.__setattr__(
                self,models_config.ConfigCommit.CHANGES.value,changes)

        if changes is None:
            object.__setattr__(
                self, models_config.ConfigCommit.CHANGES.value, [])

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
            info_process: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.get_parent_hash(args),
                capture_output=True,
                check=True
            )
        except subprocess.CalledProcessError as cpe:
            raise subprocess.CalledProcessError(
                cpe.returncode, cpe.cmd, cpe.stdout,
                f'Fossil Info Process Exception: {cpe}'
            ) from cpe
        raw_parent_hash = info_process.stdout.decode()
        initial_commit = config.InfoData.init_pattern()
        commit_parent = config.InfoData.parent_pattern()
        match_init = initial_commit.match(raw_parent_hash)
        match_parent = commit_parent.match(raw_parent_hash)
        if match_parent:
            return match_parent.group(models_config.ConfigCommit.HASH.value)
        if match_init:
            return None
        else:
            raise model_base_models_exception.CommitError('unexpected error')

class Timeline:
    """Timeline

    A collection of timeline data structures representing all commits made to
    a fossil repository.
    """
    __slots__ = tuple(config.TimelineData.COMMITS.value)

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
