"""fossil

#todo
"""
from pathlib import Path
import subprocess

from quarryforge import model
from quarryforge.config import model_config
from quarryforge.config import util_config
from quarryforge.config.util_config import TimelineData as TL_Data
from quarryforge.exceptions import fossil_exception
from quarryforge.util import fossil_util
from quarryforge.util import meta


class Timeline(metaclass=meta.Immutable):
    """"""
    __slots__ = ()

    def __setattr__(self, name: Any, value: Any) -> None:
        raise Exception('no attributes')


    def __deltattr__(self, name: Any) -> None:
        raise Exception('no attributes')

    @classmethod
    def get(cls, source: model.FossilRepo) -> str:
        """Get Raw Timeline

        """
        try:
            timeline: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.get_raw_timeline(source),
                capture_output=True,
                check=True)
        except fossil_exception.FossilTimelineError as cpe:
            raise (
                cpe.returncode, cpe.cmd, cpe.stdout,
                f'Timeline Process Exception: {cpe}') from cpe

        raw_timeline = timeline.stdout.decode()
        end_index = raw_timeline.find(TL_Data.END_MARK.value)
        return raw_timeline[:end_index]


    @classmethod
    def parse_timeline(cls, timeline: str) -> model.Timeline:
        """Parse Timeline

        """
        commits = util_config.TL_Data.commit_pattern()
        all_commits = commits.split(timeline)
        uuid = util_config.TL_Data.hash_pattern()
        date = util_config.TL_Data.date_pattern()
        author = util_config.TL_Data.author_pattern()
        comment = util_config.TL_Data.comment_pattern()
        branch = util_config.TL_Data.branch_pattern()
        tags = util_config.TL_Data.tags_pattern()
        phase = util_config.TL_Data.phase_pattern()
        change = util_config.TL_Data.change_pattern()
        parsed_timeline = model.Timeline(commits = [])

        for commit in all_commits:
            raw_data = commit.split('\n')
            data = {}
            for entry in raw_data:
                if uuid.match(entry):
                    data[TL_Data.HASH.value] = uuid.match(
                        entry).group(TL_Data.HASH.value)
                elif date.match(entry):
                    data[TL_Data.DATE.value] = date.match(
                        entry).group(TL_Data.DATE.value)
                elif author.match(entry):
                    data[TL_Data.AUTHOR.value] = author.match(
                        entry).group(TL_Data.AUTHOR.value)
                elif comment.match(entry):
                    data[TL_Data.COMMENT.value] = comment.match(
                        entry).group(TL_Data.COMMENT.value)
                elif branch.match(entry):
                    data[TL_Data.BRANCH.value] = branch.match(
                        entry).group(TL_Data.BRANCH.value)
                elif tags.match(entry):
                    data[TL_Data.TAGS.value] = tags.match(
                        entry).group(TL_Data.TAGS.value).split(', ')
                elif phase.match(entry):
                    if phase.match(entry) is None:
                        data[TL_Data.PHASE.value] = None
                    else:
                        data[TL_Data.PHASE.value] = phase.match(
                            entry).group(TL_Data.PHASE.value)
                elif change.match(entry):
                    if TL_Data.CHANGES.value is None:
                        data[TL_Data.CHANGES.value] = [change.match(
                        entry).groups()]
                    else:
                        data[TL_Data.CHANGES.value].append(
                            change.match(entry).groups()
                    )
                elif data[TL_Data.COMMENT.value] == TL_Data.INIT_CHECKIN.value:
                    data[TL_Data.CHANGES.value] = None

        new_commit = model.Commit(
            uuid=data[TL_Data.HASH.value],
            date=data[TL_Data.DATE.value],
            author=data[TL_Data.AUTHOR.value],
            comment=data[TL_Data.COMMENT.value],
            branch=data[TL_Data.BRANCH.value],
            tags=data[TL_Data.TAGS.value],
            phase=data[TL_Data.PHASE.value],
            changes=data[TL_Data.CHANGES.value])

        parsed_timeline.add(new_commit)

    return parsed_timeline


class Setup(metaclass=meta.Immutable):
    """Fossil Setup

    Setup a target repository to store the changed source repository.

    Attributes:  None

    Methods:
        new_repo:
        defualt_user:
        user_contact:

    """
    __slots__ = ()

    @classmethod
    def new_repo(
        cls,
        username: str,
        date_override: str,
        new_repo: model.FossilRepo,
        template: model.FossilRepo = None,
        project_name: str = None,
        project_desc: str = None,
    ) -> str:
        """Run the fossil new repository command."""
        try:
            init_repo = subprocess.run(
                fossil_util.rebuild_init(
                    username,
                    user_email,
                    date_override,
                    new_repo,
                    template,
                    project_name,
                    project_desc,
                ),
                capture_output=True,
                check=True)
        except fossil_exception.FossilSetupError as cpe:
            raise fossil_exception.FossilSetupError(
                cpe.returncode, cpe.cmd, cpe.stdout,
                f'Repo Creation Process Error: {cpe}'
            ) from cpe

        return init_repo.stdout.decode()

    @classmethod
    def default_user(cls, username: str, new_repo: model.FossilRepo) -> str:
        """Run the fossil user set default user command"""
        try:
            default_user = subprocess.run(
                fossil_util.set_default_user(username, new_repo),
                capture_output=True,
                check=True)
        except subprocess.FossilSetupError as cpe:
            raise subprocess.FossilSetupError(
                cpe.returncode, cpe.cmd, cpe.stdout,
                f'Repo Creation Process Error: {cpe}'
            ) from cpe

        return default_user.stdout.decode()

    @classmethod
    def user_contact(
        cls,
        username: str,
        email: str,
        source: model.FossilRepo
    ) -> str:
        """Run the fossil user contact command"""
        try:
            user_contact = subprocess.run(
                    fossil_util.set_user_contact(args),
                    capture_output=True,
                    check=True)
        except fossil_exception.FossilSetupError as cpe:
            raise fossil_exception.FossilSetupError(
                cpe.returncode, cpe.cmd, cpe.stdout,
                f'Repo Creation Process Error: {cpe}'
            ) from cpe

        return user_contact.stdout.decode())

    @classmethod
    def create_target_repo(
        username: str,
        email: str,
        date_override: str,
        new_repo: model.FossilRepo,
        template: model.FossilRepo = None,
        project_name: str = None,
        project_desc: str = None,
    ) -> str:
        """Run the new repo command sequence to configure new repo."""
        try:
            target_init = cls.new_repo()
            target_user_default = cls.default_user()
            target_user_default = cls.user_contact()
        except fossil_exception.FossilSetupError as cpe:
            raise fossil_exception.FossilSetupError(
                cpe.returncode, cpe.cmd, cpe.stdout,
                f'Repo Creation Process Error: {cpe}'
            ) from cpe

        return (target_init.stdout.decode(),
                target_user_default.stdout.decode(),
                target_user_contact.stdout.decode())


class Info(metaclass=meta.Immutable):
    """Fossil Info Command

    Get the parent commit hash for the commit version and repository provided.
    """
    __slots__ = ()

    @classmethod
    def get_parent(cls, version: str, source: model.FossilRepo) -> str | None:
        """Get Parent Commit Version

        Args:
            version: (str): The specific check-in hash to get parent.
            source (FossilRepo): Valid Path to the source repository.
        Returns:
            Version string for parent or None for initial commit.
        Raises:
            e
        """
        try:
            info_process: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.get_parent_hash(version, source),
                capture_output=True,
                check=True)
        except fossil_exception.FossilInfoError as cpe:
            raise fossil_exception.FossilInfoError(
                cpe.returncode, cpe.cmd, cpe.stdout,
                f'Fossil Info Process Exception: {cpe}') from cpe
        raw_parent_hash = info_process.stdout.decode()
        initial_commit = util_config.InfoData.init_pattern()
        commit_parent = util_config.InfoData.parent_pattern()
        match_init = initial_commit.match(raw_parent_hash)
        match_parent = commit_parent.match(raw_parent_hash)
        if match_parent:
            return match_parent.group(model_config.ConfigCommit.HASH.value)
        if match_init:
            return None
        else:
            raise base_model_exception.CommitError('unexpected error')


class Diff(metaclass=meta.Immutable):
    """Fossil Diff Command

    from, to, source
    """
    __slots__ = ()

    @classmethod
    def changes(
            cls,
            from_arg: str,
            to_arg: str,
            source: model.FossilRepo
    ) -> str:
        """Get all files changed on a commit from the source repo."""
        try:
            diff_process: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.get_file_changes(from_arg, to_arg, source),
                capture_output=True,
                check=True)
        except fossil_exception.FossilDiffError as cpe:
            raise fossil_exception.FossilDiffError(
                cpe.returncode, cpe.cmd, cpe.stdout,
                f'Fossil Diff Process Exception: {cpe}'
            ) from cpe
        raw_changes = diff_process.stdout.decode()
        return raw_changes


class Cat(metaclass=meta.Immutable):
    """Get files from source and put in target project directory.

    """
    __slots__ = ()

    @classmethod
    def content(
        cls,
        filename: str,
        outfile: str,
        version: str,
        source: model.FossilRepo
    ) -> str:
        """Use fossil cat to transfer source content to the updated repo
        project dir.
        """
        try:
            cat_process: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.get_file_content(
                    filename,
                    outfile,
                    version,
                    source
                ),
                capture_output=True,
                check=True)
        except fossil_exception.FossilCatError as cpe:
            raise fossil_exception.FossilCatError(
                cpe.returncode, cpe.cmd, cpe.stdout,
                f'Fossil Cat Process Exception: {cpe}'
            ) from cpe
        content_changes = cat_process.stdout.decode()
        return content_changes


class Branch(metaclass=meta.Immutable):
    """Manage branch info using fossil branch


    """
    __slots__ = ()

    @classmethod
    def list_all(cls, source: model.FossilRepo) -> str:
        """List all Branches for the source reposiotory"""
        try:
            list_process: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.ls_branches(source),
            capture_output=True,
            check=True)
        except


class Add(metaclass=Immutable):
    """


    """
    __slots__ = ()
    pass


class Commit(metaclass=Immutable):
    """


    """
    __slots__ = ()
    pass
