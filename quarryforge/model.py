"""model

#todo
"""
from pathlib import Path
import subprocess
from typing import Any, List, Optional

from quarryforge.config import model_config
from quarryforge.config import util_config
from quarryforge.exceptions.model_exception import args_exception
from quarryforge.exceptions.model_exception import base_model_exception
from quarryforge.exceptions.model_exception import commit_exception
from quarryforge.exceptions.model_exception import fossil_rebuild_exception
from quarryforge import protocol
from quarryforge.util import model_util


class ArgString:
    """ArgString

    Implementation of the Argument Protocol.

    Attributes:
        name: String name for the argument option with a defined value.
        value: String value for an argument.
    """
    __slots__ = model_config.ConfigArgString.slots()

    def __init__(self, name: str, value: str) -> None:
        """Initialize ArgString

        Parse the string arguments and create a readonly ArgString object.

        Args:
            name: The name of the command line option
            value: The value provided to the named option

        Raises:

        """
        object.__setattr__(
            self,
            model_config.ConfigArgString.NAME.value,
            name)
        object.__setattr__(
            self,
            model_config.ConfigArgString.VALUE.value,
            value)

    @property
    def name(self) -> str:
        """Argument name for the string provided."""
        return self._name

    @property
    def value(self) -> str:
        """Argument string value for a valid argument name provided."""
        return self._value

    def is_valid(self, name: str, value: str) -> bool:
        """is_valid

        Validate inputs for ArgString

        Args:
            name: string name of an argument
            value: string value for a named argument

        Returns:
            True if name & value are not empty or none & are strings else
            returns False.

        Raises:

        """

    def __setattr__(self, name: Any, value: Any) -> None:
        """ArgString is immutable"""
        raise fossil_rebuild_exception.ImmutableRepoConfigError()

    def __delattr__(self, name: Any) -> None:
        """ArgString is immutable"""
        raise fossil_rebuild_exception.ImmutableRepoConfigError()


class FossilRepo:
    """FossilRepo


    """
    __slots__ = model_config.ConfigFossilRepo.slots()

    def __init__(self) -> None:
        object.__setattr__(
            self,
            model_config.ConfigFossilRepo.FILE.value,
            name)

    @property
    def file(self) -> Path:
        return self._file

    def __setattr__(self, name: Any, value: Any) -> None:
        """FossilRepo is immutable"""
        raise fossil_rebuild_exception.ImmutableRepoConfigError()

    def __delattr__(self, name: Any) -> None:
        """FossilRepo is immutable"""
        raise fossil_rebuild_exception.ImmutableRepoConfigError()

    def __str__(self) -> str:
        self.file.__str__()


class FossilRebuild:
    """FossilRebuild

    Validate and Stores a valid config obtained from a parsed toml file.

    FossilRebuild holds settings for rebuilding a fossil repository with updated
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
    __slots__ = model_config.ConfigFossilRebuild.slots()

    def __init__(self,
                 user: ArgString,
                 email: ArgString,
                 src_repo: protocol.FossilRepoFile,
                 update_repo: protocol.FossilRepoFile,
                 update_dir: Path,
                 template: Optional[protocol.FossilRepoFile] = None,
                 project_name: Optional[ArgString] = None,
                 project_desc: Optional[ArgString] = None) -> None:
        """Validate and initialize a Repository Configuration."""
        user = model_util.is_valid_str_type(
            user, fossil_rebuild_exception.UserTypeError)
        user = model_util.is_not_empty(
            user, fossil_rebuild_exception.UserValueError)
        email = model_util.is_valid_str_type(
            email, fossil_rebuild_exception.EmailTypeError)
        email = model_util.is_not_empty(
            email, fossil_rebuild_exception.EmailValueError)

        src_repo = model_util.is_valid_path_type(
            src_repo,
            fossil_rebuild_exception.SrcRepoTypeError)
        src_repo = model_util.viable_source(
            src_repo, base_model_exception.RepoConfigError)
        update_repo = model_util.is_valid_path_type(
            update_repo, fossil_rebuild_exception.UpdateRepoTypeError)
        update_repo = model_util.viable_output(
            update_repo, base_model_exception.RepoConfigError)
        update_dir = model_util.is_valid_path_type(
            update_repo, fossil_rebuild_exception.UpdateDirTypeError)
        update_dir = model_util.viable_update_dir(
            update_dir, base_model_exception.RepoConfigError)
        if template is not None:
            template = model_util.is_valid_path_type(
                template, fossil_rebuild_exception.TemplateTypeError)
            template = model_util.viable_source(
                template, base_model_exception.RepoConfigError)
        if project_name is not None:
            project_name = model_util.is_valid_str_type(
                project_name,
                fossil_rebuild_exception.ProjectNameTypeError)
            project_name = model_util.is_not_empty(
                project_name,
                fossil_rebuild_exception.ProjectNameValueError)
        if project_desc is not None:
            project_desc = model_util.is_valid_str_type(
                project_desc, fossil_rebuild_exception.ProjectDescTypeError)
            project_desc = model_util.is_not_empty(
                project_desc, fossil_rebuild_exception.ProjectDescValueError)

        object.__setattr__(
            self,
            model_config.ConfigFossilRebuild.USER.value,
            user)
        object.__setattr__(
            self,
            model_config.ConfigFossilRebuild.EMAIL.value,
            email)
        object.__setattr__(
            self,
            model_config.ConfigFossilRebuild.SRC_REPO.value,
            src_repo)
        object.__setattr__(
            self,
            model_config.ConfigFossilRebuild.UPDATE_REPO.value,
            update_repo)
        object.__setattr__(
            self,
            model_config.ConfigFossilRebuild.UPDATE_DIR.value,
            update_dir)
        object.__setattr__(
            self,
            model_config.ConfigFossilRebuild.TEMPLATE.value,
            template)
        object.__setattr__(
            self,
            model_config.ConfigFossilRebuild.PROJECT_NAME.value,
            project_name)
        object.__setattr__(
            self,
            model_config.ConfigFossilRebuild.PROJECT_DESC.value,
            project_desc)

    @property
    def user(self) -> str:
        return self._user

    @property
    def email(self) -> str:
        return self._email

    @property
    def src_repo(self) -> FossilRepo:
        return self._src_repo

    @property
    def update_repo(self) -> FossilRepo:
        return self._update_repo

    @property
    def update_dir(self) -> Path:
        return self._update_dir

    @property
    def template(self) -> Optional[FossilRepo]:
        return self._template

    @property
    def project_name(self) -> Optional[str]:
        return self._project_name

    @property
    def project_desc(self) -> Optional[str]:
        return self._project_desc

    def __setattr__(self, name: Any, value: Any) -> None:
        """Repository configurations are immutable"""
        raise fossil_rebuild_exception.ImmutableRepoConfigError()

    def __deltattr__(self, name: Any) -> None:
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
    __slots__ = model_config.ConfigInfo.slots()

    def __init__(self, version: ArgString, src_repo: FossilRepo):

        version = model_util.is_valid_str_type(
            version, args_exception.InfoVersionTypeError)
        version = model_util.is_not_empty(
            version, args_exception.InfoVersionValueError)
        src_repo = model_util.is_valid_path_type(
            src_repo, args_exception.InfoRepoTypeError)
        src_repo = model_util.viable_source(
            src_repo, base_model_exception.InfoArgsError)

        object.__setattr__(
            self, model_config.ConfigInfo.VERSION.value, version)
        object.__setattr__(
            self, model_config.ConfigInfo.SRC_REPO.value, src_repo)

    def __setattr__(self, name: Any, value: Any) -> None:
        """Fossil info args are immutable."""
        raise args_exception.ImmutableInfoArgsError()

    def __delattr__(self, name: Any) -> None:
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
    __slots__ = model_config.ConfigDiff.slots()

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
            src_repo, base_model_exception.DiffRepoValueError)

        object.__setattr__(self, model_config.ConfigDiff.PARENT.value, parent)
        object.__setattr__(self, model_config.ConfigDiff.CHILD.value, child)
        object.__setattr__(
            self, model_config.ConfigDiff.SRC_REPO.value, src_repo)

    def __setattr__(self, name: Any, value: Any) -> None:
        """Fossil diff args are immutable."""
        raise args_exception.ImmutableDiffArgsError()

    def __delattr__(self, name: Any) -> None:
        """Fossil diff args are immutable."""
        raise args_exception.ImmutableDiffArgsError()


class CatArgs:
    """CatArgs

    The valid arguments for a fossil cat command.
    The arguments to retrieve the file content changed for a commit.

    Attributes:
        filename (str): Name
    """
    __slots__ = model_config.ConfigCat.slots()

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
            src_repo, base_model_exception.CatRepoValueError)

        object.__setattr__(
            self, model_config.ConfigCat.FILENAME.value, filename)
        object.__setattr__(
            self, model_config.ConfigCat.OUTFILE.value, outfile)
        object.__setattr__(
            self, model_config.ConfigCat.VERSION.value, version)
        object.__setattr__(
            self, model_config.ConfigCat.SRC_REPO.value, src_repo)

    def __setattr__(self, name: Any, value: Any) -> None:
        """Fossil cat args are immutable."""
        raise args_exception.ImmutableCatArgsError()

    def __deltattr__(self, name: Any) -> None:
        """Fossil cat args are immutable."""
        raise args_exception.ImmutableCatArgsError()


class GetTimelineArg:
    """GetTimelineArg

    This arg is to get the complete raw timeline from a fossil repo.

    Attributes:
        src_repo (Path): Path to the source repo to update.
    """
    __slots__ = model_config.ConfigGetTimelineArg.slots()

    def __init__(self, src_repo: Path):

        src_repo = model_util.is_valid_path_type(
            src_repo,
            args_exception.GetTimelineArgTypeError)
        src_repo = model_util.viable_source(
            src_repo,
            base_model_exception.GetTimelineArgValueError)

        object.__setattr__(
            self,
            model_config.ConfigGetTimelineArg.SRC_REPO.value,
            src_repo)

    def __setattr__(self, name: Any, value: Any) -> None:
        """Fossil cat args are immutable."""
        raise args_exception.ImmutableGetTimelineArgError()

    def __deltattr__(self, name: Any) -> None:
        """Fossil cat args are immutable."""
        raise args_exception.ImmutableGetTimelineArgError()


class Commit:
    """Commit

    #todo
    """
    __slots__ = model_config.ConfigCommit.slots()

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
        comment = model_util.is_not_empty(
            comment, commit_exception.CommentValueError)

        branch = model_util.is_valid_str_type(
            branch, commit_exception.BranchTypeError)
        branch = model_util.is_not_empty(
            uuid, commit_exception.BranchValueError)

        object.__setattr__(self, model_config.ConfigCommit.HASH.value, uuid)
        object.__setattr__(self, model_config.ConfigCommit.DATE.value, date)
        object.__setattr__(
            self, model_config.ConfigCommit.AUTHOR.value, author)
        object.__setattr__(
            self, model_config.ConfigCommit.COMMENT.value, comment)
        object.__setattr__(
            self, model_config.ConfigCommit.BRANCH.value, branch)

        tags = model_util.check_list_type(tags, commit_exception.TagsListError)
        tags = model_util.check_list_content(
            tags, commit_exception.TagsCommitError)
        object.__setattr__(self, model_config.ConfigCommit.TAGS.value, tags)

        object.__setattr__(self, model_config.ConfigCommit.PHASE.value, phase)

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
                self,model_config.ConfigCommit.CHANGES.value,changes)

        if changes is None:
            object.__setattr__(
                self, model_config.ConfigCommit.CHANGES.value, [])

    def __setattr__(self, name: Any, value: Any) -> None:
        """Commits are Immutable"""
        raise commit_exception.ImmutableCommitError()

    def __deltattr__(self, name: Any) -> None:
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


class Timeline:
    """Timeline

    A collection of timeline data structures representing all commits made to
    a fossil repository.
    """
    __slots__ = tuple(util_config.TimelineData.COMMITS.value)

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
