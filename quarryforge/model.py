"""model

#todo
"""
from pathlib import Path
import subprocess
from typing import Any, List, Optional

from quarryforge.config import model_config
from quarryforge.config import util_config
from quarryforge.exceptions import model_exception
from quarryforge.util import fossil_util
from quarryforge.util import model_util


class FossilRepo:
    """Represents an immutable Fossil repository configuration.

    This class encapsulates the file path to a Fossil repository.
    It is designed to be immutable.

    Attributes:
        file (Path): A read-only property providing the path to the Fossil
                     repository file.    """
    __slots__ = model_config.ConfigFossilRepo.slots()

    def __init__(self, file: Path | str, is_new: bool) -> None:
        """Initializes a new FossilRepo instance.

        Args:
            file: A `pathlib.Path` object representing the full path to the
                  Fossil repository file.
        """
        file = model_util.viable_fossil_repo(file, is_new)
        object.__setattr__(
            self,
            model_config.ConfigFossilRepo.FILE.value,
            file)

    @property
    def file(self) -> Path:
        """The path to the fossil repository file.

        This property provides read-only access to the repository's file path.

        Returns:
            pathlib.Path: The path object representing the repository file.
        """
        return getattr(self, ConfigFossilRepo.FILE.value)

    def __setattr__(self, name: Any, value: Any) -> None:
        """Prevents attribute modification, enforcing immutability.

        Attempting to set any attribute on a `FossilRepo` instance after
        initialization will raise an `ImmutableFossilRepoError`.

        Args:
            name: The name of the attribute to set.
            value: The value to set for the attribute.

        Raises:
            fossil_rebuild_exception.ImmutableFossilRepoError: Always, as
                FossilRepo instances are immutable.
        """
        raise fossil_repo.ImmutableError()

    def __delattr__(self, name: Any) -> None:
        """Prevents attribute deletion, enforcing immutability.

        Attempting to delete any attribute on a `FossilRepo` instance
        will raise an `ImmutableFossilRepoError`.

        Args:
            name: The name of the attribute to delete.

        Raises:
            fossil_rebuild_exception.ImmutableFossilRepoError: Always, as
                FossilRepo instances are immutable.
        """
        raise fossil_repo.ImmutableError()

    def __str__(self) -> str:
        """The string for the fossil repository's file path.

        Returns:
            str: The string form of the repository's `Path` object.
        """
        return str(getattr(self, ConfigFossilRepo.FILE.value))

    def __repr__(self) -> str:
        """The representation of a FossilRepo instance for logging/debugging.
        """
        return f'{self.__class__.__name__}(file={self.file!r})'

    def __eq__(self, obj: object) -> bool:
        """Checks if this FossilRepo instance is equal to another object.

        Equality is determined by comparing the `file` attribute. Two
        `FossilRepo` instances are considered equal if their `file` paths
        are the same.

        Args:
            other: The object to compare with this instance.

        Returns:
            bool: `True` if the other object is a `FossilRepo` instance and
                  their `file` attributes are equal, `False` otherwise.
            NotImplemented: If the `other` object is not a `FossilRepo` instance,
                            allowing for the comparison to be handled by the
                            other object's `__eq__` method.
        """
        if not isinstance(obj, FossilRepo):
            return NotImplemented
        return getattr(self, ConfigFossilRepo.FILE.value) == obj.file

    def __hash__(self) -> int:
        """Returns a hash for this reposiory Path instance."""
        return hash(getattr(self, ConfigFossilRepo.FILE.value))


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
    """A list of all commits from the source repository timeline.

    Attributes:
        commits List[Commit]: A list of all timeline commits
    """
    __slots__ = tuple(util_config.TimelineData.COMMITS.value)

    def __init__(self, commits: List = None):
        self.commits = commits

    def add(self, commit: Commit) -> None:
        self.commits.append(commit)

    def reverse(self) -> List[Commit] -> None:
        """Reverse Commit Order

        Default order is latest commit first.
        Reverse once return commits in order from iniital commit.
        """
        self.commits.reverse()
        return self.commits
