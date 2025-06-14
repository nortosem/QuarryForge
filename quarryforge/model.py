"""model

This module defines the core data models for the QuarryForge application,
including representations for Fossil repositories, individual commits, and
repository timelines. All data models are designed to be immutable once created,
enforcing data integrity.
"""
from pathlib import Path
from typing import Any, cast, List, Optional, Tuple, TypeVar

from quarryforge.config import meta_config
from quarryforge.config import model_config
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.config.exception_conf import meta_exception_config as meta_ec
from quarryforge.config.exception_conf import model_exception_config as model_ec
from quarryforge.exception import meta_exception
from quarryforge.exception import model_exception
from quarryforge.meta import immutable
from quarryforge.util import model_util


_ImmutableModel = TypeVar(
    '_ImmutableModel',
    bound='immutable.ImmutableInstance'
)


class FossilRepo(
    immutable.ImmutableInstance,
    metaclass=immutable.ImmutableMetaClass):
    """Represents an immutable Fossil repository configuration.

    This class encapsulates the file path to a Fossil repository.
    It is designed to be immutable.

    Attributes:
        _file (Path):
            Internal attribute storing the path to the Fossil repository file.
        _workdir (Path):
            Internal attribute storing the path to the working directory
            associated with the repository.
        _is_new (bool):
            Internal attribute indicating if this represents a newly created
            repository or an existing one.
    """
    __slots__ = model_config.fossil_repo_config().slots()

    def __init__(
        self,
        file: Path | str,
        workdir: Path | str,
        is_new: bool
    ) -> None:
        """Initializes a new FossilRepo instance.

        Args:
            file (Path | str):
                A `pathlib.Path` object or string representing the full path to
                the Fossil repository file.
            workdir (Path | str):
                A `pathlib.Path` object or string representing the working
                directory associated with this repository.
            is_new (bool):
                A boolean indicating if this is a new repository to be created
                (True) or an existing one (False).

        Raises:
            model_exception.FossilRepoError:
                If any of the provided paths are invalid or do not meet the
                criteria (e.g., non-existent for existing repo, already exists
                for new repo).
        """
        file_path, workdir_path = model_util.viable_fossil_repo(
            file, workdir, is_new, model_exception.FossilRepoError
        )
        config = model_config.fossil_repo_config()
        object.__setattr__(self, config.file, file_path)
        object.__setattr__(self, config.is_new, is_new)
        object.__setattr__(self, config.workdir, workdir_path)

    @property
    def file(self) -> Path:
        """The path to the fossil repository file.

        Returns:
            pathlib.Path: The path object representing the repository file.
        """
        return cast(
            Path, getattr(self, model_config.fossil_repo_config().file)
        )

    @property
    def is_new(self) -> bool:
        """Indicates if the repository is a newly created one.

        Returns:
            bool: True if the repository is new, False otherwise.
        """
        return cast(
            bool, getattr(self, model_config.fossil_repo_config().is_new)
        )

    @property
    def workdir(self) -> Path:
        """The path to the working directory for the fossil repository.

        Returns:
            pathlib.Path: The path object representing the working directory of
                the fossil repository from the file attribute.
        """
        return cast(
            Path, getattr(self, model_config.fossil_repo_config().workdir)
        )

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevents attribute modification, enforcing immutability.

        Attempting to set any attribute on a `FossilRepo` instance after
        initialization will raise an `ImmutableFossilRepoError`.

        Args:
            name: The name of the attribute to set.
            value: The value to set for the attribute.

        Raises:
            meta_exception.ImmutableError: Always, as FossilRepo instances
            are immutable.
        """
        builder = meta_ec.MetaErrorBuilder(
            error_context=meta_ec.MetaErrorPath.IMMUTABLE_INSTANCE,
            error_code=meta_ec.MetaErrorCode.IMMUTABILITY_VIOLATION,
            arg=self,
            field= name,
            info=meta_config.attribute_modifier_type().set_attribute
        )
        error_data = builder.data()
        raise meta_exception.ImmutableError(**error_data.to_exception())

    def __delattr__(self, name: Any) -> None:
        """Prevents attribute deletion, enforcing immutability.

        Attempting to delete any attribute on a `FossilRepo` instance
        will raise an `ImmutableError`.

        Args:
            name (Any): The name of the attribute to delete.

        Raises:
            meta_exception.ImmutableError: Always, as FossilRepo instances
                are immutable.
        """
        builder = meta_ec.MetaErrorBuilder(
            error_context=meta_ec.MetaErrorPath.IMMUTABLE_INSTANCE,
            error_code=meta_ec.MetaErrorCode.IMMUTABILITY_VIOLATION,
            arg=self,
            field= name,
            info=meta_config.attribute_modifier_type().delete_attribute
        )
        error_data = builder.data()
        raise meta_exception.ImmutableError(**error_data.to_exception())

    def __str__(self) -> str:
        """Returns a user-friendly string representation of a Fossil repository.

        Returns:
            str: A string showing the repository file and working directory.
        """
        return (
            f'Fossil Repository File: {self.file}\n'
            f'Working Directory: {self.workdir}'
        )

    def __repr__(self) -> str:
        """The representation of a FossilRepo instance for logging/debugging.
        """
        return (
            f'{self.__class__.__name__}(file={self.file!r}, '
            f'is_new={self.is_new!r}, '
            f'workdir={self.workdir!r})'
        )

    def __eq__(self, obj: object) -> bool:
        """Checks if this FossilRepo instance is equal to another object.

        Equality is determined by comparing the `file` attribute. Two
        `FossilRepo` instances are considered equal if their `file` paths
        are the same.

        Args:
            other: The object to compare with this instance.

        Returns:
            bool: `True` if the other object is a `FossilRepo` instance and
                  their attributes are equal, `False` otherwise.
            NotImplemented:
                If the `other` object is not a `FossilRepo` instance,
                allowing for the comparison to be handled by the other
                object's `__eq__` method.
        """
        if not isinstance(obj, FossilRepo):
            return NotImplemented

        return self.file == obj.file and self.workdir == obj.workdir

    def __hash__(self) -> int:
        """Returns a hash for this repository Path instance.

        The hash is based on the immutable properties of the repository,
        ensuring that equal objects have the same hash.

        Returns:
            int: The hash value of the object.
        """
        return hash((self.file, self.is_new, self.workdir))


class FossilCommit(
    immutable.ImmutableInstance,
    metaclass=immutable.ImmutableMetaClass):
    """ Represents an immutable Fossil commit object, encapsulating all its
        metadata and associated changes.

    Attributes:
        _uuid (str):
            Internal attribute storing the unique identifier (hash)
            of the commit.
        _date (str):
            Internal attribute storing the date and time of the commit.
        _author (str):
            Internal attribute storing the author of the commit.
        _comment (str):
            Internal attribute storing the commit message.
        _branch (Optional[str]):
            Internal attribute storing the branch name associated with the
            commit.
        _tags (List[str]):
            Internal attribute storing a list of tags applied to the commit.
        _phase (Optional[str]):
            Internal attribute storing the commit phase
            (e.g., 'PUBLISHED', 'FROZEN', 'LEAF').
        _changes (List[Tuple[str, str]]):
            Internal attribute storing a list of tuples,
            where each tuple represents a file change: (status, filename).
    """
    __slots__ = model_config.fossil_commit_config().slots()

    def __init__(
        self,
        uuid: str,
        date: str,
        author: str,
        comment: str,
        branch: Optional[str] = None,
        tags: Optional[List[str]] = None,
        phase: Optional[List[str]] = None,
        changes: Optional[List[Tuple[str,str]]] = None
    ):
        (uuid_val, date_val, author_val, comment_val, branch_val, tags_val,
         phase_val, changes_val) = (
            model_util.viable_fossil_commit(
                uuid=uuid, date=date, author=author, comment=comment,
                branch=branch, tags=tags, phase=phase, changes=changes,
                exception=model_exception.FossilCommitError
            )
        )
        config = model_config.fossil_commit_config()
        object.__setattr__(self,config.uuid,uuid_val)
        object.__setattr__(self, config.date, date_val)
        object.__setattr__(self, config.author, author_val)
        object.__setattr__(self, config.comment, comment_val)
        object.__setattr__(self, config.branch, branch_val)
        object.__setattr__(
            self, config.tags, tags_val if tags_val is not None else []
        )
        object.__setattr__(self, config.phase, phase_val)
        object.__setattr__(
            self,
            config.changes,
            changes_val if changes_val is not None else []
        )

    @property
    def uuid(self) -> str:
        """The unique identifier (hash) of the commit.

        Returns:
            str: The commit UUID.
        """
        return cast(
            str, getattr(self, model_config.fossil_commit_config().uuid)
        )

    @property
    def date(self) -> str:
        """The date and time of the commit.

        Returns:
            str: The commit date string (e.g., 'YYYY-MM-DD HH:MM:SS').
        """
        return cast(
            str, getattr(self, model_config.fossil_commit_config().date)
        )


    @property
    def author(self) -> str:
        """The author of the commit.

        Returns:
            str: The author's name.
        """
        return cast(
            str, getattr(self, model_config.fossil_commit_config().author)
        )


    @property
    def comment(self) -> str:
        """The commit message.

        Returns:
            str: The commit's comment or message.
        """
        return cast(
            str, getattr(self, model_config.fossil_commit_config().comment)
        )


    @property
    def branch(self) -> Optional[str]:
        """The branch name associated with the commit.

        Returns:
            Optional[str]: The branch name string, or None if not specified.
        """
        return cast(
            str, getattr(self, model_config.fossil_commit_config().branch)
        )


    @property
    def tags(self) -> Optional[List[str]]:
        """A list of tags applied to the commit.

        Returns:
            List[str]: A list of tag strings. Can be empty if no tags.
        """
        return cast(
            List[str], getattr(self, model_config.fossil_commit_config().tags)
        )


    @property
    def phase(self) -> Optional[List[str]]:
        """The commit phase,  zero or more of:
        *CURRENT*, *MERGE*, *FORK*, *UNPUBLISHED*, *LEAF*, *BRANCH*

        Returns:
            Optional[str]: The commit phase string, or None if not specified.
        """
        return cast(
            List[str], getattr(self, model_config.fossil_commit_config().phase)
        )


    @property
    def changes(self) -> List[Tuple[str, str]]:
        """A list of file changes in the commit.

        Each tuple contains (status, filename), e.g., ('ADDED', 'file.txt').

        Returns:
            List[Tuple[str, str]]:
                A list of tuples representing file changes.
                Can be empty if no changes.
        """
        return cast(
            List[Tuple[str, str]],
            getattr(self, model_config.fossil_commit_config().changes)
        )

    def get_hash(self) -> str:
        """Get Brief Commit Hash

        Returns a shortened version of the commit's UUID (first 12 characters).

        Returns:
            str: The brief commit hash.
        """
        return self.uuid[:12]

    def __setattr__(self, name: Any, value: Any) -> None:
        """Prevents attribute modification, enforcing immutability.

        Attempting to set any attribute on a `FossilCommit` instance after
        initialization will raise an `ImmutableError`.

        Args:
            name (Any): The name of the attribute to set.
            value (Any): The value to set for the attribute.

        Raises:
            meta_exception.ImmutableError:
                Always, as FossilCommit instances are immutable.
        """
        builder = meta_ec.MetaErrorBuilder(
            error_context=meta_ec.MetaErrorPath.IMMUTABLE_INSTANCE,
            error_code=meta_ec.MetaErrorCode.IMMUTABILITY_VIOLATION,
            arg=self,
            field= name,
            info=meta_config.attribute_modifier_type().set_attribute
        )
        error_data = builder.data()
        raise meta_exception.ImmutableError(**error_data.to_exception())

    def __delattr__(self, name: Any) -> None:
        """Prevents attribute deletion, enforcing immutability.

        Attempting to delete any attribute on a `FossilCommit` instance
        will raise an `ImmutableError`.

        Args:
            name (Any): The name of the attribute to delete.

        Raises:
            meta_exception.ImmutableError:
            Always, as FossilCommit instances are immutable.
        """
        builder = meta_ec.MetaErrorBuilder(
            error_context=meta_ec.MetaErrorPath.IMMUTABLE_INSTANCE,
            error_code=meta_ec.MetaErrorCode.IMMUTABILITY_VIOLATION,
            arg=self,
            field= name,
            info=meta_config.attribute_modifier_type().delete_attribute
        )
        error_data = builder.data()
        raise meta_exception.ImmutableError(**error_data.to_exception())

    def __repr__(self) -> str:
        """Official String Representation of a Commit for developers/debugging.

        Returns:
            str:
                A detailed string representation including all commit
                attributes.
        """
        attrs = []
        for slot_name in self.__slots__:
            prop_name = slot_name.lstrip('_')
            attr_value = getattr(self, prop_name, None)

            if isinstance(attr_value, str):
                attrs.append(f'{prop_name}={attr_value!r}')
            elif isinstance(attr_value, list):
                if all(isinstance(item, str) for item in attr_value):
                    list_items = [f'{item!r}' for item in attr_value]
                    attrs.append(f"{prop_name}=[{', '.join(list_items)}]")
                elif all(isinstance(item, tuple) for item in attr_value):
                    tuple_items = []
                    for t_item in attr_value:
                        if isinstance(
                                t_item, tuple
                        ) and all(
                            isinstance(s, str) for s in t_item
                        ):
                            tuple_items.append(
                                f'({t_item[0]!r}, {t_item[1]!r})'
                            )
                        else:
                            tuple_items.append(repr(t_item))
                    attrs.append(f"{prop_name}=[{', '.join(tuple_items)}]")
                else:
                    attrs.append(f'{prop_name}={repr(attr_value)}')
            else:
                attrs.append(f'{prop_name}={attr_value}')
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    def __str__(self) -> str:
        """Standard string output for a Commit (user-friendly summary).

        Returns:
            str:
                A concise summary of the commit, including UUID, date, author,
                and comment.
        """
        uuid_short = self.get_hash()
        return (
            f'uuid: {uuid_short}\n'
            f'date: {self.date}\n'
            f'author: {self.author}\n'
            f'comment: {self.comment}'
        )


    def __hash__(self) -> int:
        """Get a hash for a commit.

        The hash is based on the immutable core properties of the commit.

        Returns:
            int: The hash value of the object.
        """
        return hash((self.uuid, self.date, self.author, self.comment))


class FossilTimeline:
    """A list of all commits from the source repository timeline.

    This class encapsulates a collection of `FossilCommit` objects, typically
    representing the historical sequence of commits in a repository.

    Attributes:
        commits (List[FossilCommit]): A list of all timeline commits, ordered
                                      chronologically (oldest to newest).
    """
    __slots__ = (model_config.fossil_timeline_config().commits,)

    def __init__(self, commits: Optional[List[FossilCommit]] = None):
        """Initializes a FossilTimeline instance.

        Args:
            commits (Optional[List[FossilCommit]]):
                An optional list of FossilCommit objects. If None, an empty
                list is used. The list is reversed internally to ensure
                chronological order (oldest to newest).

        Raises:
            model_exception.FossilTimelineError: If the `commits` argument is
                not a list or if it contains objects that are not instances of
                `FossilCommit`.
        """
        fossil_timeline_config = model_config.fossil_timeline_config()
        valid: Any = commits or []

        if not isinstance(valid, list):
            builder = model_ec.FossilTimelineErrorBuilder(
                error_context=model_ec.ModelErrorPath.FOSSIL_TIMELINE_INIT,
                error_code=ec.GenericError.TYPE_ERROR,
                arg=commits,
                field=fossil_timeline_config.commits,
                info=(f"Argument 'commits' must be a list, but got "
                      f"'{type(commits).__name__}'.")
            )
            error_data = builder.data()
            raise model_exception.FossilTimelineError(
                **error_data.to_exception()
            )
        if not all(
            isinstance(commit, FossilCommit) for commit in valid
        ):
            invalid = next(
                (c for c in valid if not isinstance(
                    c, FossilCommit
                )),
                None

            )
            info = (
                'All items in "commits" list must be '
                '"FossilCommit" instances.'
            )
            if invalid is not None:
                info += (
                    f' Found an item of type "{type(invalid).__name__}".'
                )
            builder = model_ec.FossilTimelineErrorBuilder(
                error_context=(
                    model_ec.ModelErrorPath.FOSSIL_TIMELINE_INIT
                ),
                error_code=ec.GenericError.TYPE_ERROR,
                arg=commits,
                field=fossil_timeline_config.commits,
                info=info
            )
            error_data = builder.data()
            raise model_exception.FossilTimelineError(
                **error_data.to_exception()
            )

        valid.reverse()

        object.__setattr__(
            self,
            model_config.fossil_timeline_config().commits,
            valid
        )

    def add(self, commit: FossilCommit) -> None:
        """Adds a FossilCommit to the timeline.

        Args:
            commit (FossilCommit): The commit object to add.
        """
        cast(
            List[FossilCommit],
            getattr(self,model_config.fossil_timeline_config().commits)
        ).append(commit)

    def __len__(self) -> int:
        """Returns the number of commits in the timeline."""
        return len(
            cast(
                List[FossilCommit],
                getattr(self,model_config.fossil_timeline_config().commits)
            )
        )

    def __getitem__(self, index: int) -> FossilCommit:
        """Allows indexing into the commits list.

        Args:
            index (int): The index of the commit to retrieve.

        Returns:
            FossilCommit: The commit object at the specified index.
        """
        return cast(
            List[FossilCommit],
            getattr(self,model_config.fossil_timeline_config().commits)
        )[index]

    def __iter__(self) -> Any:
        """Allows iteration over the commits."""
        return iter(
            cast(
                List[FossilCommit],
                getattr(self,model_config.fossil_timeline_config().commits)
            )
        )

    def __repr__(self) -> str:
        """Official string representation for developers/debugging.

        Returns:
            str:
                A concise representation indicating the class and number
                of commits.
        """
        commits = cast(
            List[FossilCommit],
            getattr(self,model_config.fossil_timeline_config().commits)
        )

        return (
            f'{self.__class__.__name__}(commits={len(commits)} commits)'
        )

    def __str__(self) -> str:
        """User-friendly string representation of the timeline.

        Returns:
            str: A string summarizing the timeline's content.
        """
        commits = cast(
            List[FossilCommit],
            getattr(self,model_config.fossil_timeline_config().commits)
        )
        return f'Fossil Timeline with {len(commits)} commits.'
