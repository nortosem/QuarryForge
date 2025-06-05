"""fossil

This module provides an interface for interacting with Fossil SCM repositories
by executing Fossil commands via subprocess.
"""
from pathlib import Path
import subprocess
from typing import Any, Dict, List, Optional

from quarryforge import model
from quarryforge.config import fossil_config as _
from quarryforge.config.fossil_config import TIMELINE_DATA
from quarryforge.config import model_config
from quarryforge.config import root
from quarryforge.exception import fossil_exception
from quarryforge.config.exception_conf import fossil_exception_config as fossil_ec
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.config.exception_conf import exception_data as e_data
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

        Executes the Fossil 'timeline' command to retrieve the raw timeline data
        from a specified repository.

        Args:
            source (model.FossilRepo):
                The repository from which to retrieve the timeline.

        Returns:
            str: The raw timeline output string.

        Raises:
            fossil_exception.FossilProcessError:
                If the Fossil command fails with a non-zero exit code.
            fossil_exception.FossilTimeoutError:
                If the Fossil command times out.
            fossil_exception.FossilTimelineError:
                If there's an issue specific to processing the timeline.
        """
        try:
            timeline: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.get_raw_timeline(source),
                cwd=source.file.parent,
                capture_output=True,
                check=True,
                timeout=_.FOSSIL.default_timeout)
        except subprocess.CalledProcessError as error:
            process_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
                error_code=_.FOSSIL.process_error,
                arg=str(source),
                extra_details={
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.return_code: error.returncode,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            process_data = process_builder.data()
            process_error = fossil_exception.FossilProcessError(
                **process_data.to_exception()
            )
            timeline_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMELINE,
                error_code=ec.GENERIC_ERROR.external_dependency_error,
                arg=str(source),
                extra_details = {
                    ec.DESC_MSG.dependency: process_error.details[
                        _.FOSSIL.cmd
                    ],
                    ec.DESC_MSG.reason: process_error.details[
                        _.FOSSIL.stderr
                    ],
                }
            )
            timeline_data = timeline_builder.data()

            raise fossil_exception.FossilTimelineError(
                **timeline_data.to_exception()
            ) from process_error
        except subprocess.TimeoutExpired as error:
            timeout_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMEOUT,
                error_code=_.FOSSIL.timeout_error,
                arg=str(source),
                extra_details={
                    _.FOSSIL.args: error.args,
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.timeout: error.timeout,
                    _.FOSSIL.stderr: str(error)
                }
            )
            timeout_data = timeout_builder.data()
            timeout_error = fossil_exception.FossilTimeoutError(
                **timeout_data.to_exception()
            )
            timeline_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMELINE,
                error_code=ec.GENERIC_ERROR.invalid_state,
                arg=str(source),
                extra_details = {
                    _.FOSSIL.args: timeout_error.details[_.FOSSIL.args],
                    _.FOSSIL.cmd: timeout_error.details[_.FOSSIL.cmd],
                    _.FOSSIL.timeout: timeout_error.details[_.FOSSIL.timeout],
                    _.FOSSIL.stderr: timeout_error.details[
                        _.FOSSIL.stderr
                    ],
                }
            )
            timeline_data = timeline_builder.data()

            raise fossil_exception.FossilTimeoutError(
                **timeline_data.to_exception()
            ) from timeout_error

        raw_timeline = timeline.stdout.decode()
        end_index = raw_timeline.find(TIMELINE_DATA.END_MARK)
        return raw_timeline[:end_index] if end_index != -1 else raw_timeline


    @staticmethod
    def parse_timeline(timeline_output: str) -> model.FossilTimeline:
        """Parse Timeline

        Parses the raw timeline output string into a `FossilTimeline` object
        containing `FossilCommit` instances.

        Args:
            timeline_output (str): The raw string output from the Fossil
            'timeline' command.

        Returns:
            model.FossilTimeline: An object representing the parsed timeline.

        Raises:
            fossil_exception.FossilTimelineError: If parsing fails or no commit
            data is found.
        """
        parsed_commits: List[model.FossilCommit] = []
        try:
            commit_pattern = TIMELINE_DATA.commit_pattern()
            all_commits_raw = commit_pattern.split(timeline_output)
            uuid_re = TIMELINE_DATA.hash_pattern()
            date_re = TIMELINE_DATA.date_pattern()
            author_re = TIMELINE_DATA.author_pattern()
            comment_re = TIMELINE_DATA.comment_pattern()
            branch_re = TIMELINE_DATA.branch_pattern()
            tags_re = TIMELINE_DATA.tags_pattern()
            phase_re = TIMELINE_DATA.phase_pattern()
            change_re = TIMELINE_DATA.change_pattern()

            for commit in all_commits_raw:
                raw_data_lines = commit.split('\n')
                commit_data: Dict[str, Any] = {
                    TIMELINE_DATA.TAGS_KEY: [],
                    TIMELINE_DATA.CHANGES_KEY: []
                }
                for entry in raw_data_lines:
                    uuid_re_match = uuid_re.match(entry)
                    if uuid_re_match:
                        commit_data[TIMELINE_DATA.HASH_KEY] = (
                            uuid_re_match.group(TIMELINE_DATA.HASH_KEY)
                        )
                        continue
                    date_re_match = date_re.match(entry)
                    if date_re_match:
                        commit_data[TIMELINE_DATA.DATE_KEY] = (
                            date_re_match.group(TIMELINE_DATA.DATE_KEY)
                        )
                        continue
                    author_re_match = author_re.match(entry)
                    if author_re_match:
                        commit_data[TIMELINE_DATA.AUTHOR_KEY] = (
                            author_re_match.group(TIMELINE_DATA.AUTHOR_KEY)
                        )
                        continue
                    comment_re_match = comment_re.match(entry)
                    if comment_re_match:
                        commit_data[TIMELINE_DATA.COMMENT_KEY] = (
                            comment_re_match.group(TIMELINE_DATA.COMMENT_KEY)
                        )
                        continue
                    branch_re_match = branch_re.match(entry)
                    if branch_re_match:
                        commit_data[TIMELINE_DATA.BRANCH_KEY] = (
                            branch_re_match.group(TIMELINE_DATA.BRANCH_KEY)
                        )
                        continue
                    tags_re_match = tags_re.match(entry)
                    if tags_re_match:
                        commit_data[TIMELINE_DATA.TAGS_KEY] = (
                            tags_re_match.group(
                                TIMELINE_DATA.TAGS_KEY
                            ).split(', ')
                        )
                        continue
                    phase_re_match = phase_re.match(entry)
                    if phase_re_match:
                        if phase_re.match(entry) is None:
                            commit_data[TIMELINE_DATA.PHASE_KEY] = None
                        else:
                            commit_data[TIMELINE_DATA.PHASE_KEY] = (
                                phase_re_match.group(
                                    TIMELINE_DATA.PHASE_KEY)
                            )
                        continue
                    change_re_match = change_re.match(entry)
                    if change_re_match:
                        if commit_data[TIMELINE_DATA.CHANGES_KEY] is None:
                            commit_data[
                                TIMELINE_DATA.CHANGES_KEY
                            ] = [change_re_match.groups()]
                        else:
                            commit_data[TIMELINE_DATA.CHANGES_KEY].append(
                                change_re_match.groups())
                        continue
                    if commit_data[
                        TIMELINE_DATA.COMMENT_KEY
                    ] == TIMELINE_DATA.INIT_CHECKIN:
                        commit_data[TIMELINE_DATA.CHANGES_KEY] = None
                        continue

                try:
                    new_commit = model.FossilCommit(
                        uuid=commit_data.get(TIMELINE_DATA.HASH_KEY, ''),
                        date=commit_data.get(TIMELINE_DATA.DATE_KEY, ''),
                        author=commit_data.get(TIMELINE_DATA.AUTHOR_KEY, ''),
                        comment=commit_data.get(TIMELINE_DATA.COMMENT_KEY, ''),
                        branch=commit_data.get(TIMELINE_DATA.BRANCH_KEY, None),
                        tags=commit_data.get(TIMELINE_DATA.TAGS_KEY, []),
                        phase=commit_data.get(TIMELINE_DATA.PHASE_KEY, None),
                        changes=commit_data.get(TIMELINE_DATA.CHANGES_KEY, [])
                    )
                    parsed_commits.append(new_commit)
                except Exception as error:
                    builder = fossil_ec.FossilErrorBuilder(
                        error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMELINE,
                        error_code=ec.GENERIC_ERROR.value_error,
                        arg=new_commit,
                        extra_details={
                            ec.DescMsg.reason: (
                                f'{root.MODEL.fossil_commit} failue: {error}'
                            )},
                        info=(
                            f'Failed to construct commit object from parsed '
                            f'timeline data: {error}'
                        )
                    )
                    error_data = builder.data()
                    raise fossil_exception.FossilTimelineError(
                        **error_data.to_exception()
                    ) from error
                if not parsed_commits:
                    builder = fossil_ec.FossilErrorBuilder(
                        error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMELINE,
                        error_code=ec.GENERIC_ERROR.invalid_state,
                        arg=timeline_output[:100] + (
                            '...' if len(
                                timeline_output
                            ) > 100 else timeline_output
                        ),
                        info='No commit data found in timeline output.',
                    )
                    error_data = builder.data()
                    raise fossil_exception.FossilTimelineError(
                        **error_data.to_exception()
                    )

            return model.FossilTimeline(commits=parsed_commits)

        except Exception as e:
            if isinstance(e, fossil_exception.FossilTimelineError):
                raise
            builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMELINE,
                error_code=ec.GENERIC_ERROR.value_error,
                arg=timeline_output[:100] + '...' if len(
                    timeline_output) > 100 else timeline_output,
                extra_details={ec.DescMsg.reason: (
                    f'General parsing error: {e}')},
                info=f'Failed to parse timeline data: {e}'
            )
            error_data = builder.data()
            raise fossil_exception.FossilTimelineError(
                **error_data.to_exception()
            ) from e


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
        template: Optional[model.FossilRepo] = None,
        project_name: Optional[str] = None,
        project_desc: Optional[str] = None) -> str:
        """Run the new repository command to configure a new repository.

        Args:
            username (str): The admin username for the new repository.
            date_override (str):
                The date and time string to override the initial commit date.
            new_repo (model.FossilRepo):
                The FossilRepo object for the new repository.
            template (Optional[model.FossilRepo]):
                An optional template repository to copy config from.
            project_name (Optional[str]): Optional project name.
            project_desc (Optional[str]): Optional project description.

        Returns:
            str: The stdout from the fossil init command.

        Raises:
            fossil_exception.FossilProcessError:
                If the Fossil command fails.
            fossil_exception.FossilTimeoutError:
                If the Fossil command times out.
            fossil_exception.FossilSetupError:
                If there's an issue specific to repository setup.
        """
        try:
            init_repo: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.rebuild_init(
                    username,
                    date_override,
                    new_repo,
                    template,
                    project_name,
                    project_desc,
                ),
                cwd=new_repo.file.parent,
                capture_output=True,
                check=True,
                timeout=_.FOSSIL.default_timeout)
        except subprocess.CalledProcessError as error:
            process_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
                error_code=_.FOSSIL.process_error,
                arg=str(new_repo),
                extra_details={
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.return_code: error.returncode,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            process_data = process_builder.data()
            process_error = fossil_exception.FossilProcessError(
                **process_data.to_exception()
            )
            setup_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_SETUP,
                error_code=ec.GENERIC_ERROR.external_dependency_error,
                arg=str(new_repo),
                extra_details = {
                    ec.DESC_MSG.dependency: process_error.details[
                        _.FOSSIL.cmd
                    ],
                    ec.DESC_MSG.reason: process_error.details[
                        _.FOSSIL.stderr
                    ],
                    _.FOSSIL.step: _.FOSSIL.init
                }
            )
            setup_data = setup_builder.data()
            raise fossil_exception.FossilSetupError(
                **setup_data.to_exception()
            ) from process_error
        except subprocess.TimeoutExpired as error:
            timeout_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMEOUT,
                error_code=_.FOSSIL.timeout_error,
                arg=str(new_repo),
                extra_details={
                    _.FOSSIL.args: error.args,
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.timeout: error.timeout,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr,
                },
                info=str(error),
            )
            timeout_data = timeout_builder.data()
            timeout_error = fossil_exception.FossilTimeoutError(
                **timeout_data.to_exception()
            )
            setup_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_SETUP,
                error_code=ec.GENERIC_ERROR.invalid_state,
                arg=str(new_repo),
                extra_details = {
                    _.FOSSIL.args: timeout_error.details[_.FOSSIL.args],
                    _.FOSSIL.cmd: timeout_error.details[_.FOSSIL.cmd],
                    _.FOSSIL.timeout: timeout_error.details[_.FOSSIL.timeout],
                   _.FOSSIL.step: _.FOSSIL.init,
                },
                info=timeout_error.details[e_data.BUILDER_FIELD.info]
            )
            setup_data = setup_builder.data()
            raise fossil_exception.FossilSetupError(
                **setup_data.to_exception()
            ) from timeout_error

        return init_repo.stdout.decode()

    @staticmethod
    def default_user(username: str, new_repo: model.FossilRepo) -> str:
        """Run the fossil user set default user command.

        Args:
            username (str): The username to set as default.
            new_repo (model.FossilRepo): The repository to configure.

        Returns:
            str: The stdout from the fossil user default command.

        Raises:
            fossil_exception.FossilProcessError:
                If the Fossil command fails.
            fossil_exception.FossilTimeoutError:
                If the Fossil command times out.
            fossil_exception.FossilSetupError:
                If there's an issue specific to setting the default user.
        """
        try:
            default_user: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.set_default_user(username, new_repo),
                cwd=new_repo.file.parent,
                capture_output=True,
                check=True,
                timeout=_.FOSSIL.default_timeout)
        except subprocess.CalledProcessError as error:
            process_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
                error_code=_.FOSSIL.process_error,
                arg=str(new_repo),
                extra_details={
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.return_code: error.returncode,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            process_data = process_builder.data()
            process_error = fossil_exception.FossilProcessError(
                **process_data.to_exception()
            )
            setup_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_SETUP,
                error_code=ec.GENERIC_ERROR.external_dependency_error,
                arg=str(new_repo),
                extra_details = {
                    ec.DESC_MSG.dependency: process_error.details[
                        _.FOSSIL.cmd
                    ],
                    ec.DESC_MSG.reason: process_error.details[
                        _.FOSSIL.stderr
                    ],
                    _.FOSSIL.step: _.FOSSIL.username_setup
                }
            )
            setup_data = setup_builder.data()
            raise fossil_exception.FossilSetupError(
                **setup_data.to_exception()
            ) from process_error
        except subprocess.TimeoutExpired as error:
            timeout_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMEOUT,
                error_code=_.FOSSIL.timeout_error,
                arg=str(new_repo),
                info=str(error),
                extra_details={
                    _.FOSSIL.args: error.args,
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.timeout: error.timeout,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            timeout_data = timeout_builder.data()
            timeout_error = fossil_exception.FossilTimeoutError(
                **timeout_data.to_exception()
            )
            setup_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_SETUP,
                error_code=ec.GENERIC_ERROR.invalid_state,
                arg=str(new_repo),
                info=timeout_error.details[e_data.BUILDER_FIELD.info],
                extra_details = {
                    _.FOSSIL.args: timeout_error.details[_.FOSSIL.args],
                    _.FOSSIL.cmd: timeout_error.details[_.FOSSIL.cmd],
                    _.FOSSIL.timeout: timeout_error.details[_.FOSSIL.timeout],
                    _.FOSSIL.step: _.FOSSIL.username_setup
                }
            )
            setup_data = setup_builder.data()
            raise fossil_exception.FossilSetupError(
                **setup_data.to_exception()
            ) from timeout_error

        return default_user.stdout.decode()

    @staticmethod
    def user_contact(
        username: str,
        email: str,
        source: model.FossilRepo) -> str:
        """Run the fossil user contact command.

        Args:
            username (str): The username whose contact info to update.
            email (str): The new contact email address.
            source (model.FossilRepo): The repository to configure.

        Returns:
            str: The stdout from the fossil user contact command.

        Raises:
            fossil_exception.FossilProcessError:
                If the Fossil command fails.
            fossil_exception.FossilTimeoutError:
                If the Fossil command times out.
            fossil_exception.FossilSetupError:
                If there's an issue specific to setting user contact info.
        """
        try:
            user_contact: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.set_user_contact(username, email, source),
                cwd=source.file.parent,
                capture_output=True,
                check=True,
                timeout=_.FOSSIL.default_timeout)
        except subprocess.CalledProcessError as error:
            process_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
                error_code=_.FOSSIL.process_error,
                arg=str(source),
                extra_details={
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.return_code: error.returncode,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            process_data = process_builder.data()
            process_error = fossil_exception.FossilProcessError(
                **process_data.to_exception()
            )
            setup_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_SETUP,
                error_code=ec.GENERIC_ERROR.external_dependency_error,
                arg=str(source),
                extra_details = {
                    ec.DESC_MSG.dependency: process_error.details[
                        _.FOSSIL.cmd
                    ],
                    ec.DESC_MSG.reason: process_error.details[
                        _.FOSSIL.stderr
                    ],
                    _.FOSSIL.step: _.FOSSIL.user_contact
                }
            )
            setup_data = setup_builder.data()
            raise fossil_exception.FossilSetupError(
                **setup_data.to_exception()
            ) from process_error
        except subprocess.TimeoutExpired as error:
            timeout_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMEOUT,
                error_code=_.FOSSIL.timeout_error,
                arg=str(source),
                info=str(error),
                extra_details={
                    _.FOSSIL.args: error.args,
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.timeout: error.timeout,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            timeout_data = timeout_builder.data()
            timeout_error = fossil_exception.FossilTimeoutError(
                **timeout_data.to_exception()
            )
            setup_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_SETUP,
                error_code=ec.GENERIC_ERROR.invalid_state,
                arg=str(source),
                info=timeout_error.details[e_data.BUILDER_FIELD.info],
                extra_details = {
                    _.FOSSIL.args: timeout_error.details[_.FOSSIL.args],
                    _.FOSSIL.cmd: timeout_error.details[_.FOSSIL.cmd],
                    _.FOSSIL.timeout: timeout_error.details[_.FOSSIL.timeout],
                    _.FOSSIL.step: _.FOSSIL.user_contact
                }
            )
            setup_data = setup_builder.data()
            raise fossil_exception.FossilSetupError(
                **setup_data.to_exception()
            ) from timeout_error

        return user_contact.stdout.decode()


class Info(metaclass=immutable.Namespace):
    """Fossil Info Process

    Get the parent commit hash for the commit version and repository provided.
    """
    @staticmethod
    def get_parent(version: str, source: model.FossilRepo) -> str | None:
        """Get Parent Commit Version

        Retrieves the parent commit hash for a given version (check-in hash)
        from a Fossil repository.

        Args:
            version (str): The specific check-in hash to get the parent of.
            source (model.FossilRepo): The repository to query.

        Returns:
            str | None:
                The version string for the parent commit, or None if it's the
                initial commit (no parent).

        Raises:
            fossil_exception.FossilProcessError:
                If the Fossil command fails.
            fossil_exception.FossilTimeoutError:
                If the Fossil command times out.
            fossil_exception.FossilInfoError:
                If an issue occurs during info retrieval or parsing.
        """
        try:
            info_process: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.get_parent_hash(version, source),
                cwd=source.workdir.cwd(),
                capture_output=True,
                check=True,
                timeout=_.FOSSIL.default_timeout)
        except subprocess.CalledProcessError as error:
            process_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
                error_code=_.FOSSIL.process_error,
                arg=f'{version} from {str(source)}',
                extra_details={
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.return_code: error.returncode,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            process_data = process_builder.data()
            process_error = fossil_exception.FossilProcessError(
                **process_data.to_exception()
            )
            info_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_INFO,
                error_code=ec.GENERIC_ERROR.external_dependency_error,
                arg=f'{version} from {str(source)}',
                extra_details = {
                    ec.DESC_MSG.dependency: process_error.details[
                        _.FOSSIL.cmd
                    ],
                    ec.DESC_MSG.reason: process_error.details[
                        _.FOSSIL.stderr
                    ],
                }
            )
            info_data = info_builder.data()
            raise fossil_exception.FossilInfoError(
                **info_data.to_exception()
            ) from process_error
        except subprocess.TimeoutExpired as error:
            timeout_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMEOUT,
                error_code=_.FOSSIL.timeout_error,
                arg=f'{version} from {str(source)}',
                info=str(error.stdout),
                extra_details={
                    _.FOSSIL.args: error.args,
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.timeout: error.timeout,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            timeout_data = timeout_builder.data()
            timeout_error = fossil_exception.FossilTimeoutError(
                **timeout_data.to_exception()
            )
            info_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_INFO,
                error_code=ec.GENERIC_ERROR.invalid_state,
                arg=f'{version} from {str(source)}',
                info=timeout_error.details[e_data.BUILDER_FIELD.info],
                extra_details = {
                    _.FOSSIL.args: timeout_error.details[_.FOSSIL.args],
                    _.FOSSIL.cmd: timeout_error.details[_.FOSSIL.cmd],
                    _.FOSSIL.timeout: timeout_error.details[_.FOSSIL.timeout],
                }
            )
            info_data = info_builder.data()
            raise fossil_exception.FossilInfoError(
                **info_data.to_exception()
            ) from timeout_error

        raw_parent_hash = info_process.stdout.decode()
        initial_commit_re = _.INFO_DATA.init_pattern()
        commit_parent_re = _.INFO_DATA.parent_pattern()
        match_init = initial_commit_re.match(raw_parent_hash)
        match_parent = commit_parent_re.match(raw_parent_hash)

        if match_parent:
            return match_parent.group(model_config.FOSSIL_COMMIT.uuid)
        if match_init:
            return None
        else:
            info_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_INFO,
                error_code=ec.GENERIC_ERROR.value_error,
                arg=raw_parent_hash[:100] + (
                    '...' if len(raw_parent_hash) > 100 else raw_parent_hash
                ),
                info=(
                    f'Unable to parse parent hash or detect initial commit for'
                    f' version {version}.'
                ),
                extra_details={
                    'raw_output': raw_parent_hash
                }
            )
            info_data = info_builder.data()
            raise fossil_exception.FossilInfoError(**info_data.to_exception())


class Diff(metaclass=immutable.Namespace):
    """Fossil Diff Process

    Provides methods for querying file changes between commits using Fossil's
    'diff' command.
    """
    @staticmethod
    def changes(
            from_arg: str,
            to_arg: str,
            source: model.FossilRepo) -> str:
        """Get all files changed on a commit from the source repo.

        Executes the Fossil 'diff --brief' command to get a summary of changes
        between two check-ins.

        Args:
            from_arg (str): The starting check-in hash or alias.
            to_arg (str): The ending check-in hash or alias.
            source (model.FossilRepo): The repository to perform the diff on.

        Returns:
            str: The raw output string containing the file changes.

        Raises:
            fossil_exception.FossilProcessError:
                If the Fossil command fails.
            fossil_exception.FossilTimeoutError:
                If the Fossil command times out.
            fossil_exception.FossilDiffError:
                If an issue occurs during the diff operation.
        """
        try:
            diff_process: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.get_file_changes(from_arg, to_arg, source),
                cwd=source.workdir,
                capture_output=True,
                check=True,
                timeout=_.FOSSIL.default_timeout)
        except subprocess.CalledProcessError as error:
            process_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
                error_code=_.FOSSIL.process_error,
                arg=f'{from_arg} to {to_arg} in {str(source)}',
                extra_details={
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.return_code: error.returncode,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            process_data = process_builder.data()
            process_error = fossil_exception.FossilProcessError(
                **process_data.to_exception()
            )
            diff_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_DIFF,
                error_code=ec.GENERIC_ERROR.external_dependency_error,
                arg=f'{from_arg} to {to_arg} in {str(source)}',
                extra_details = {
                    ec.DESC_MSG.dependency: process_error.details[
                        _.FOSSIL.cmd
                    ],
                    ec.DESC_MSG.reason: process_error.details[
                        _.FOSSIL.stderr
                    ],
                }
            )
            diff_data = diff_builder.data()
            raise fossil_exception.FossilDiffError(
                **diff_data.to_exception()
            ) from process_error
        except subprocess.TimeoutExpired as error:
            timeout_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMEOUT,
                error_code=_.FOSSIL.timeout_error,
                arg=f'{from_arg} to {to_arg} in {str(source)}',
                info=str(error),
                extra_details={
                    _.FOSSIL.args: error.args,
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.timeout: error.timeout,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            timeout_data = timeout_builder.data()
            timeout_error = fossil_exception.FossilTimeoutError(
                **timeout_data.to_exception()
            )
            diff_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_DIFF,
                error_code=ec.GENERIC_ERROR.invalid_state,
                arg=f'{from_arg} to {to_arg} in {str(source)}',
                info=timeout_error.details[e_data.BUILDER_FIELD.info],
                extra_details = {
                    _.FOSSIL.args: timeout_error.details[_.FOSSIL.args],
                    _.FOSSIL.cmd: timeout_error.details[_.FOSSIL.cmd],
                    _.FOSSIL.timeout: timeout_error.details[_.FOSSIL.timeout],
                }
            )
            diff_data = diff_builder.data()
            raise fossil_exception.FossilDiffError(
                **diff_data.to_exception()
            ) from timeout_error
        raw_changes = diff_process.stdout.decode()
        return raw_changes


class Cat(metaclass=immutable.Namespace):
    """Fossil Cat Process

    Provides methods for retrieving file content from a Fossil repository.
    """
    @staticmethod
    def content(
        filename: str,
        outfile: str,
        version: str,
        source: model.FossilRepo,

    ) -> str:
        """Use fossil cat to transfer source content to the updated repo
        project dir.

        Retrieves the content of a specific file at a given version from a
        Fossil repository and writes it to an output file.

        Args:
            filename (str):
                The name of the file to retrieve content from.
            outfile (str):
                The path to the output file where content will be written.
            version (str):
                The specific check-in hash of the file version.
            source (model.FossilRepo):
                The repository to extract artifacts from.

        Returns:
            str:
                The stdout from the fossil cat command
                (often empty for success).

        Raises:
            fossil_exception.FossilProcessError:
                If the Fossil command fails.
            fossil_exception.FossilTimeoutError:
                If the Fossil command times out.
            fossil_exception.FossilCatError:
                If an issue occurs during the cat operation.
        """
        try:
            cat_process: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.get_file_content(
                    filename,
                    outfile,
                    version,
                    source
                ),
                cwd=source.workdir,
                capture_output=True,
                check=True,
                timeout=_.FOSSIL.default_timeout)
        except subprocess.CalledProcessError as error:
            process_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
                error_code=_.FOSSIL.process_error,
                arg=f'{filename} @ {version} from {str(source)}',
                extra_details={
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.return_code: error.returncode,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            process_data = process_builder.data()
            process_error = fossil_exception.FossilProcessError(
                **process_data.to_exception()
            )
            cat_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_CAT,
                error_code=ec.GENERIC_ERROR.external_dependency_error,
                arg=f'{filename} @ {version} from {str(source)}',
                extra_details = {
                    ec.DESC_MSG.dependency: process_error.details[
                        _.FOSSIL.cmd
                    ],
                    ec.DESC_MSG.reason: process_error.details[
                        _.FOSSIL.stderr
                    ],
                }
            )
            cat_data = cat_builder.data()
            raise fossil_exception.FossilCatError(
                **cat_data.to_exception()
            ) from process_error
        except subprocess.TimeoutExpired as error:
            timeout_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMEOUT,
                error_code=_.FOSSIL.timeout_error,
                arg=f'{filename} @ {version} from {str(source)}',
                info=str(error),
                extra_details={
                    _.FOSSIL.args: error.args,
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.timeout: error.timeout,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            timeout_data = timeout_builder.data()
            timeout_error = fossil_exception.FossilTimeoutError(
                **timeout_data.to_exception()
            )
            cat_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_CAT,
                error_code=ec.GENERIC_ERROR.invalid_state,
                arg=f'{filename} @ {version} from {str(source)}',
                info=timeout_error.details[e_data.BUILDER_FIELD.info],
                extra_details = {
                    _.FOSSIL.args: timeout_error.details[_.FOSSIL.args],
                    _.FOSSIL.cmd: timeout_error.details[_.FOSSIL.cmd],
                    _.FOSSIL.timeout: timeout_error.details[_.FOSSIL.timeout],

                }
            )
            cat_data = cat_builder.data()
            raise fossil_exception.FossilCatError(
                **cat_data.to_exception()
            ) from timeout_error
        content_changes = cat_process.stdout.decode()
        return content_changes


class Branch(metaclass=immutable.Namespace):
    """Fossil Branch Process

    Manage branch info using fossil branch
    """
    @staticmethod
    def list_all(source: model.FossilRepo) -> str:
        """List all Branches for the source reposiotory.

        Executes the Fossil 'branch list --all' command to list all branches
        in a given repository.

        Args:
            source (model.FossilRepo): The repository to list branches from.

        Returns:
            str: The raw output string containing the list of branches.

        Raises:
            fossil_exception.FossilProcessError:
                If the Fossil command fails.
            fossil_exception.FossilTimeoutError:
                If the Fossil command times out.
            fossil_exception.FossilBranchError:
                If an issue occurs during the branch operation.
        """
        try:
            list_process: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.ls_branches(source),
                cwd=source.file.parent,
                capture_output=True,
                check=True,
                timeout=_.FOSSIL.default_timeout)
            return list_process.stdout.decode()
        except subprocess.CalledProcessError as error:
            process_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
                error_code=_.FOSSIL.process_error,
                arg=str(source),
                extra_details={
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.return_code: error.returncode,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            process_data = process_builder.data()
            process_error = fossil_exception.FossilProcessError(
                **process_data.to_exception()
            )
            branch_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_BRANCH,
                error_code=ec.GENERIC_ERROR.external_dependency_error,
                arg=str(source),
                extra_details = {
                    ec.DESC_MSG.dependency: process_error.details[
                        _.FOSSIL.cmd
                    ],
                    ec.DESC_MSG.reason: process_error.details[
                        _.FOSSIL.stderr
                    ],
                }
            )
            branch_data = branch_builder.data()
            raise fossil_exception.FossilBranchError(
                **branch_data.to_exception()
            ) from process_error
        except subprocess.TimeoutExpired as error:
            timeout_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMEOUT,
                error_code=_.FOSSIL.timeout_error,
                arg=str(source),
                info=str(error),
                extra_details={
                    _.FOSSIL.args: error.args,
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.timeout: error.timeout,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            timeout_data = timeout_builder.data()
            timeout_error = fossil_exception.FossilTimeoutError(
                **timeout_data.to_exception()
            )
            branch_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_BRANCH,
                error_code=ec.GENERIC_ERROR.invalid_state,
                arg=str(source),
                info=timeout_error.details[e_data.BUILDER_FIELD.info],
                extra_details = {
                    _.FOSSIL.args: timeout_error.details[_.FOSSIL.args],
                    _.FOSSIL.cmd: timeout_error.details[_.FOSSIL.cmd],
                    _.FOSSIL.timeout: timeout_error.details[_.FOSSIL.timeout],
                }
            )
            branch_data = branch_builder.data()
            raise fossil_exception.FossilBranchError(
                **branch_data.to_exception()
            ) from timeout_error


class Add(metaclass=immutable.Namespace):
    """Fossil Add Process

    Provides methods for adding files to an open Fossil repository check-out.
    """
    __slots__ = ()

    @staticmethod
    def add_files(files: List[Path]) -> str:
        """Add files to the Fossil repository check-out.

        Args:
            files (List[Path]):
                A list of `Path` objects representing the files to add. The
                command will be run in the current working directory of the
                process.

        Returns:
            str: The stdout from the fossil add command.

        Raises:
            fossil_exception.FossilProcessError:
                If the Fossil command fails.
            fossil_exception.FossilTimeoutError:
                If the Fossil command times out.
            fossil_exception.FossilAddError:
                If an issue occurs during the add operation.
        """
        try:
            add_process: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.add_files(files),
                capture_output=True,
                check=True,
                timeout=_.FOSSIL.default_timeout
            )
            return add_process.stdout.decode()
        except subprocess.CalledProcessError as error:
            process_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
                error_code=_.FOSSIL.process_error,
                arg=f'files: {[str(f) for f in files]}',
                extra_details={
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.return_code: error.returncode,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            process_data = process_builder.data()
            process_error = fossil_exception.FossilProcessError(
                **process_data.to_exception()
            )
            add_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_ADD,
                error_code=ec.GENERIC_ERROR.external_dependency_error,
                arg=f'files: {[str(f) for f in files]}',
                extra_details = {
                    ec.DESC_MSG.dependency: process_error.details[
                        _.FOSSIL.cmd
                    ],
                    ec.DESC_MSG.reason: process_error.details[
                        _.FOSSIL.stderr
                    ],
                }
            )
            add_data = add_builder.data()
            raise fossil_exception.FossilAddError(
                **add_data.to_exception()
            ) from process_error
        except subprocess.TimeoutExpired as error:
            timeout_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMEOUT,
                error_code=_.FOSSIL.timeout_error,
                arg=f'files: {[str(f) for f in files]}',
                info=str(error),
                extra_details={
                    _.FOSSIL.args: error.args,
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.timeout: error.timeout,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            timeout_data = timeout_builder.data()
            timeout_error = fossil_exception.FossilTimeoutError(
                **timeout_data.to_exception()
            )
            add_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_ADD,
                error_code=ec.GENERIC_ERROR.invalid_state,
                arg=f'files: {[str(f) for f in files]}',
                info=timeout_error.details[e_data.BUILDER_FIELD.info],
                extra_details = {
                    _.FOSSIL.args: timeout_error.details[_.FOSSIL.args],
                    _.FOSSIL.cmd: timeout_error.details[_.FOSSIL.cmd],
                    _.FOSSIL.timeout: timeout_error.details[_.FOSSIL.timeout],
                }
            )
            add_data = add_builder.data()
            raise fossil_exception.FossilAddError(
                **add_data.to_exception()
            ) from timeout_error

    @staticmethod
    def remove_files(files: List[Path]) -> str:
        """Remove files from the Fossil repository check-out.

        Args:
            files (List[Path]):
                A list of `Path` objects representing the files to remove.

        Returns:
            str: The stdout from the fossil rm command.

        Raises:
            fossil_exception.FossilProcessError:
                If the Fossil command fails.
            fossil_exception.FossilTimeoutError:
                If the Fossil command times out.
            fossil_exception.FossilAddError:
                If an issue occurs during the remove operation.
        """
        raise NotImplementedError('Remove files not yet implemented.')

    @staticmethod
    def rename_file(old_path: Path, new_path: Path) -> str:
        """Rename a file in the Fossil repository check-out.

        Args:
            old_path (Path): The current path of the file.
            new_path (Path): The new path for the file.

        Returns:
            str: The stdout from the fossil mv command.

        Raises:
            fossil_exception.FossilProcessError:
                If the Fossil command fails.
            fossil_exception.FossilTimeoutError:
                If the Fossil command times out.
            fossil_exception.FossilAddError:
                If an issue occurs during the rename operation.
        """
        raise NotImplementedError('Rename file not yet implemented.')


class Commit(metaclass=immutable.Namespace):
    """Fossil Commit Process

    Provides methods for committing changes to a Fossil repository check-out.
    """
    __slots__ = ()

    @staticmethod
    def commit_changes(
        date_override: str,
        user_override: str,
        comment: str,
        branch: Optional[str] = None,
        tag: Optional[str] = None,
        files: Optional[List[Path]] = None
    ) -> str:
        """Commit changes to the Fossil repository.

        Args:
            date_override (str): The date string to override the commit date.
            user_override (str): The username to override the committer.
            comment (str): The commit message.
            branch (Optional[str]): The branch name for the commit.
            tag (Optional[str]): A tag to apply to the commit.
            files (Optional[List[Path]]):
                A list of `Path` objects for specific files to commit. If None,
                all pending changes are committed.

        Returns:
            str: The stdout from the fossil commit command.

        Raises:
            fossil_exception.FossilProcessError:
                If the Fossil command fails.
            fossil_exception.FossilTimeoutError:
                If the Fossil command times out.
            fossil_exception.FossilCommitError:
                If an issue occurs during the commit operation.
        """
        try:
            ci_process: subprocess.CompletedProcess[bytes] = subprocess.run(
                fossil_util.commit(
                    date_override,
                    user_override,
                    comment,
                    branch,
                    tag,
                    files or []
                ),
                capture_output=True,
                check=True,
                timeout=_.FOSSIL.default_timeout
            )
            return ci_process.stdout.decode()
        except subprocess.CalledProcessError as error:
            process_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_PROCESS,
                error_code=_.FOSSIL.process_error,
                arg=f'commit for {comment[:50]}...',
                extra_details={
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.return_code: error.returncode,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            process_data = process_builder.data()
            process_error = fossil_exception.FossilProcessError(
                **process_data.to_exception()
            )
            commit_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_COMMIT,
                error_code=ec.GENERIC_ERROR.external_dependency_error,
                arg=f'commit for {comment[:50]}...',
                extra_details = {
                    ec.DESC_MSG.dependency: process_error.details[
                        _.FOSSIL.cmd
                    ],
                    ec.DESC_MSG.reason: process_error.details[
                        _.FOSSIL.stderr
                    ],
                }
            )
            commit_data = commit_builder.data()
            raise fossil_exception.FossilCommitError(
                **commit_data.to_exception()
            ) from process_error
        except subprocess.TimeoutExpired as error:
            timeout_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMEOUT,
                error_code=_.FOSSIL.timeout_error,
                arg=f'commit for {comment[:50]}...',
                info=str(error),
                extra_details={
                    _.FOSSIL.args: error.args,
                    _.FOSSIL.cmd: error.cmd,
                    _.FOSSIL.timeout: error.timeout,
                    _.FOSSIL.output: error.stdout,
                    _.FOSSIL.stderr: error.stderr
                }
            )
            timeout_data = timeout_builder.data()
            timeout_error = fossil_exception.FossilTimeoutError(
                **timeout_data.to_exception()
            )
            commit_builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_COMMIT,
                error_code=ec.GENERIC_ERROR.invalid_state,
                arg=f'commit for {comment[:50]}...',
                info=timeout_error.details[e_data.BUILDER_FIELD.info],
                extra_details = {
                    _.FOSSIL.args: timeout_error.details[_.FOSSIL.args],
                    _.FOSSIL.cmd: timeout_error.details[_.FOSSIL.cmd],
                    _.FOSSIL.timeout: timeout_error.details[_.FOSSIL.timeout],
                }
            )
            commit_data = commit_builder.data()
            raise fossil_exception.FossilCommitError(
                **commit_data.to_exception()
            ) from timeout_error
