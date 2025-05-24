"""fossil

#todo
"""
import subprocess

from quarryforge import model
from quarryforge.config import fossil_config
from quarryforge.config import model_config
from quarryforge.config import util_config
from quarryforge.config.util_config import TimelineData as TL_Data
from quarryforge.exception import fossil_exception
from quarryforge.meta import immutable
from quarryforge.util import fossil_util


class Timeline(metaclass=immutable.Namespace):
    """Fossil Timeline Process

    The fossil.Timeline namespace for executing fossil timeline processes on a
    fossil repository.
    """
    __slots__ = ()

    @staticmethod
    def get(source: model.FossilRepo) -> str:
        """Get Raw Timeline

        """
        try:
            timeline: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.get_raw_timeline(source),
                capture_output=True,
                check=True,
                timeout=fossil_config.ConfigFossil.default_timeout)
        except subprocess.CalledProcessError as error:
            process_error = fossil_exception.FossilProcessError(
                returncode=error.returncode,
                cmd=error.cmd,
                stdout=error.stdout,
                stderr=error.stderr,
                message=f'Failed to get timeline for {source.file.path}'
            )
            raise fossil_exception.FossilTimelineError(
                message=(
                    f'Timeline Process Exception: '
                    f'Failed to get raw timeline from {source.file.path}.'),
                details=process_error.details,
                user_message=(
                    f'Timeline data from repository {source.file.path} '
                    f'could net be retrieved.'
                )
            ) from process_error
        except subprocess.TimeoutExpired as error:
            timeout_error = fossil_exception.FossilTimeoutError(
                cmd=error.cmd,
                timeout=error.timeout,
                stdout=error.stdout,
                stderr=error.stderr,
                message=(
                    f'Fossil timeline command timed out for {source.file.path}'
                )
            )
            raise fossil_exception.FossilTimelineError(
                message=(
                    f'Timeline Process Timeout: '
                    f'Unable to get raw timeline from {source.file.path}.'
                ),
                details=timeout_error.details,
                user_message=(
                    f'Timeline data retrieval from '
                    f'{source.file.path} took too long.'
                )
            ) from timeout_error

        raw_timeline = timeline.stdout.decode()
        end_index = raw_timeline.find(TL_Data.END_MARK.value)
        return raw_timeline[:end_index]


    @staticmethod
    def parse_timeline(timeline: str) -> model.FossilTimeline:
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


class Setup(metaclass=immutable.Namespace):
    """Fossil Setup Process

    Setup a target repository to store the changed source repository.

    Order of setup operations:
    # 1. Create new fossil repo for the rebuild:
    cd ~/dev/fossil/; #fossil repo dir
    #2 Fossil init command:
    fossil init {rebuild}.fossil
    --date-override DATETIME # sourced from init commit from original repo
    --admin-user USERNAME # the name configured for use with github account
    --template ./source_repo.fossil #to match existing config
    --project-name # copy from source repo
    --project-desc #copy from source repo

    #2 The init only defines the admin-user, but a default user remains
    necessary and undefined so far. Set the default user:
    fossil user default USERNAME -R {rebuild}.fossil

    #3 Update the default user with the correct contact mail
    ## This will match the user name and email used with github for the repo.
    fossil user contact USERNAME contact@email.com -R {rebuild}.fossil

    Attributes:  None

    Methods:
        new_repo:
        defualt_user:
        user_contact:

    """
    @staticmethod
    def new_repo(
        username: str,
        date_override: str,
        new_repo: model.FossilRepo,
        template: model.FossilRepo = None,
        project_name: str = None,
        project_desc: str = None) -> str:
        """new_repo

        Run the fossil new repository command to configure a new repository.
        """
        try:
            init_repo = subprocess.run(
                fossil_util.rebuild_init(
                    username,
                    date_override,
                    new_repo,
                    template,
                    project_name,
                    project_desc,
                ),
                capture_output=True,
                check=True,
                timeout=fossil_config.ConfigFossil.default_timeout)
        except subprocess.CalledProcessError as error:
            process_error = fossil_exception.FossilProcessError(
                returncode=error.returncode,
                cmd=error.cmd,
                stdout=error.stdout,
                stderr=error.stderr,
                message=f'Failed to create new repo for {new_repo}'
            )
            raise fossil_exception.FossilSetupError(
                error.returncode, error.cmd, error.stdout,
                f'Fossil Setup Process Error: {error}'
            ) from process_error

        return init_repo.stdout.decode()

    @staticmethod
    def default_user(username: str, new_repo: model.FossilRepo) -> str:
        """Run the fossil user set default user command"""
        try:
            default_user = subprocess.run(
                fossil_util.set_default_user(username, new_repo),
                capture_output=True,
                check=True,
                timeout=fossil_config.ConfigFossil.default_timeout)
        except subprocess.CalledProcessError as error:
            process_error = fossil_exception.FossilProcessError(
                returncode=error.returncode,
                cmd=error.cmd,
                stdout=error.stdout,
                stderr=error.stderr,
                message=f'Failed to set default user for {new_repo}'
            )
            raise fossil_exception.FossilSetupError(
                error.returncode, error.cmd, error.stdout,
                f'Fossil Setup Process Error: {error}'
            ) from process_error

        return default_user.stdout.decode()

    @staticmethod
    def user_contact(
        username: str,
        email: str,
        source: model.FossilRepo) -> str:
        """Run the fossil user contact command"""
        try:
            user_contact = subprocess.run(
                fossil_util.set_user_contact(username, email, source),
                capture_output=True,
                check=True,
                timeout=fossil_config.ConfigFossil.default_timeout)
        except subprocess.CalledProcessError as error:
            process_error = fossil_exception.FossilProcessError(
                returncode=error.returncode,
                cmd=error.cmd,
                stdout=error.stdout,
                stderr=error.stderr,
                message=f'Failed to set user email for {source}'
            )
            raise fossil_exception.FossilSetupError(
                error.returncode, error.cmd, error.stdout,
                f'Fossil Setup Process Error: {error}'
            ) from process_error

        return user_contact.stdout.decode()


class Info(metaclass=immutable.Namespace):
    """Fossil Info Process

    Get the parent commit hash for the commit version and repository provided.
    """
    @staticmethod
    def get_parent(version: str, source: model.FossilRepo) -> str | None:
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
                check=True,
                timeout=fossil_config.ConfigFossil.default_timeout)
        except subprocess.CalledProcessError as error:
            process_error = fossil_exception.FossilProcessError(
                returncode=error.returncode,
                cmd=error.cmd,
                stdout=error.stdout,
                stderr=error.stderr,
                message=f'Failed to fetch info from {source}'
            )
            raise fossil_exception.FossilInfoError(
                error.returncode, error.cmd, error.stdout,
                f'Fossil Info Process Error: {error}'
            ) from process_error
        raw_parent_hash = info_process.stdout.decode()
        initial_commit = util_config.INFO_DATA.init_pattern()
        commit_parent = util_config.INFO_DATA.parent_pattern()
        match_init = initial_commit.match(raw_parent_hash)
        match_parent = commit_parent.match(raw_parent_hash)
        if match_parent:
            return match_parent.group(model_config.ConfigCommit.HASH.value)
        if match_init:
            return None
        else:
            raise fossil_exception.FossilInfoError()


class Diff(metaclass=immutable.Namespace):
    """Fossil Diff Process

    from, to, source
    """
    @staticmethod
    def changes(
            from_arg: str,
            to_arg: str,
            source: model.FossilRepo) -> str:
        """Get all files changed on a commit from the source repo."""
        try:
            diff_process: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.get_file_changes(from_arg, to_arg, source),
                capture_output=True,
                check=True,
                timeout=fossil_config.ConfigFossil.default_timeout)
        except subprocess.CalledProcessError as error:
            process_error = fossil_exception.FossilProcessError(
                returncode=error.returncode,
                cmd=error.cmd,
                stdout=error.stdout,
                stderr=error.stderr,
                message=f'Failed to fetch Diff from {source}'
            )
            raise fossil_exception.FossilDiffError(
                error.returncode, error.cmd, error.stdout,
                f'Fossil Diff Process Error: {error}'
            ) from process_error
        raw_changes = diff_process.stdout.decode()
        return raw_changes


class Cat(metaclass=immutable.Namespace):
    """Fossil Cat Process

    Get files from source and put in target project directory.
    """
    @staticmethod
    def content(
        filename: str,
        outfile: str,
        version: str,
        source: model.FossilRepo) -> str:
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
                check=True,
                timeout=fossil_config.ConfigFossil.default_timeout)
        except subprocess.CalledProcessError as error:
            process_error = fossil_exception.FossilProcessError(
                returncode=error.returncode,
                cmd=error.cmd,
                stdout=error.stdout,
                stderr=error.stderr,
                message=f'Failed to fetch Cat from {source}'
            )
            raise fossil_exception.FossilCatError(
                error.returncode, error.cmd, error.stdout,
                f'Fossil Cat Process Error: {error}'
            ) from process_error
        content_changes = cat_process.stdout.decode()
        return content_changes


class Branch(metaclass=immutable.Namespace):
    """Fossil Branch Process

    Manage branch info using fossil branch
    """
    @staticmethod
    def list_all(source: model.FossilRepo) -> str:
        """List all Branches for the source reposiotory"""
        try:
            list_process: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.ls_branches(source),
                capture_output=True,
                check=True,
                timeout=fossil_config.ConfigFossil.default_timeout)
            return list_process.stdout.decode()
        except subprocess.CalledProcessError as error:
            process_error = fossil_exception.FossilProcessError(
                returncode=error.returncode,
                cmd=error.cmd,
                stdout=error.stdout,
                stderr=error.stderr,
                message=f'Failed to fetch Branch from {source}'
            )
            raise fossil_exception.FossilBranchError(
                error.returncode, error.cmd, error.stdout,
                f'Fossil Branch Process Error: {error}'
            ) from process_error


class Add(metaclass=immutable.Namespace):
    """Fossil Add Process


    """
    pass


class Commit(metaclass=immutable.Namespace):
    """Fossil Commit Process


    """
    pass
