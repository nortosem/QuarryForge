"""Fossil Timeline Process

The fossil.Timeline namespace for executing fossil timeline processes on a
fossil repository.
"""
import subprocess
from typing import Any, Dict, List

from quarryforge import model
from quarryforge.config import fossil_config as _
from quarryforge.config.fossil_config import timeline_data
from quarryforge.config import root
from quarryforge.exception import fossil_exception
from quarryforge.exception import model_exception
from quarryforge.config.exception_conf import fossil_exception_config as fossil_ec
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.util import fossil_util


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
        fossil_exception.FossilTimelineError:
            If the Fossil command fails, times out, or has an issue specific
            to timeline processing.
    """

    try:
        timeline: subprocess.CompletedProcess[bytes] = subprocess.run(
            fossil_util.get_raw_timeline(source),
            cwd=source.file.parent,
            capture_output=True,
            check=True,
            timeout=int(_.Fossil.DEFAULT_TIMEOUT)
        )
    except subprocess.CalledProcessError as error:
        stderr_output = (
            error.stderr.decode(
                errors='ignore') if error.stderr else 'No stderr output.'
        )
        builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMELINE,
            error_code=ec.GenericError.EXTERNAL_DEPENDENCY_ERROR,
            arg=str(source),
            extra_details={
                _.Fossil.CMD: error.cmd,
                _.Fossil.RETURN_CODE: error.returncode,
                _.Fossil.OUTPUT: error.stdout,
                _.Fossil.STDERR: error.stderr,
                ec.DescMsg.DEPENDENCY: error.cmd,
                ec.DescMsg.REASON: stderr_output
            }
        )
        raise fossil_exception.FossilTimelineError(
            **builder.data().to_exception()
        ) from error
    except subprocess.TimeoutExpired as error:
        builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMELINE,
            error_code=_.Fossil.TIMEOUT_ERROR,
            arg=str(source),
            extra_details={
                _.Fossil.ARGS: error.args,
                _.Fossil.CMD: error.cmd,
                _.Fossil.TIMEOUT: error.timeout,
                _.Fossil.STDERR: str(error),
                ec.DescMsg.REASON: "The 'fossil timeline' command timed out."
            }
        )
        timeout_data = builder.data()
        raise fossil_exception.FossilTimelineError(
            **timeout_data.to_exception()
        )
    raw_timeline = timeline.stdout.decode(errors='ignore')
    end_index = raw_timeline.find(timeline_data().END_MARK)
    return raw_timeline[:end_index] if end_index != -1 else raw_timeline


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
    timeline = timeline_data()
    parsed_commits: List[model.FossilCommit] = []
    commit_pattern = timeline.commit_pattern()
    all_commits_raw = commit_pattern.split(timeline_output)
    if not all_commits_raw:
        builder = fossil_ec.FossilErrorBuilder(
            error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMELINE,
            error_code=ec.GenericError.INVALID_STATE_ERROR,
            arg=timeline_output[:100] + (
                '...' if len(timeline_output
            ) > 100 else ''),
            info='No parsable commit blocks found in timeline output.',
        )
        raise fossil_exception.FossilTimelineError(
            **builder.data().to_exception()
        )
    (uuid_re, date_re, author_re, comment_re, branch_re,
     tags_re, phase_re, change_re) = (
        timeline.hash_pattern(), timeline.date_pattern(),
        timeline.author_pattern(), timeline.comment_pattern(),
        timeline.branch_pattern(), timeline.tags_pattern(),
        timeline.phase_pattern(), timeline.change_pattern()
    )
    for commit_info in all_commits_raw:
        commit_data: Dict[str, Any] = {
            timeline.TAGS_KEY: [],
            timeline.CHANGES_KEY: [],
            timeline.PHASE_KEY: [],
        }
        for entry in commit_info.split('\n'):
            if match := uuid_re.match(entry):
                commit_data[timeline.HASH_KEY] = (
                    match.group(timeline.HASH_KEY)
                )
            elif match := date_re.match(entry):
                commit_data[timeline.DATE_KEY] = (
                    match.group(timeline.DATE_KEY)
                )
            elif match := author_re.match(entry):
                commit_data[timeline.AUTHOR_KEY] = (
                    match.group(timeline.AUTHOR_KEY)
                )
            elif match := comment_re.match(entry):
                commit_data[timeline.COMMENT_KEY] = (
                    match.group(timeline.COMMENT_KEY)
                )
            elif match := branch_re.match(entry):
                commit_data[timeline.BRANCH_KEY] = (
                    match.group(timeline.BRANCH_KEY)
                )
            elif match := tags_re.match(entry):
                commit_data[timeline.TAGS_KEY] = (
                    match.group(timeline.TAGS_KEY).split(', ')
                )
            elif match := phase_re.match(entry):
                commit_data[timeline.PHASE_KEY].extend(
                    match.group(timeline.PHASE_KEY).split(', ')
                )
            elif match := change_re.match(entry):
                commit_data[timeline.CHANGES_KEY].append(match.groups())
        if commit_data[timeline.COMMENT_KEY] == timeline.INIT_CHECKIN:
            commit_data[timeline.CHANGES_KEY] = None
        try:
            new_commit = model.FossilCommit(
                uuid=commit_data.get(timeline.HASH_KEY, ''),
                date=commit_data.get(timeline.DATE_KEY, ''),
                author=commit_data.get(timeline.AUTHOR_KEY, ''),
                comment=commit_data.get(timeline.COMMENT_KEY, ''),
                branch=commit_data.get(timeline.BRANCH_KEY, None),
                tags=commit_data.get(timeline.TAGS_KEY, []),
                phase=commit_data.get(timeline.PHASE_KEY, None),
                changes=commit_data.get(timeline.CHANGES_KEY, [])
            )
            parsed_commits.append(new_commit)
        except model_exception.FossilCommitError as error:
            builder = fossil_ec.FossilErrorBuilder(
                error_context=fossil_ec.FossilErrorPath.FOSSIL_TIMELINE,
                error_code=ec.GenericError.VALUE_ERROR,
                arg=new_commit,
                extra_details={
                    ec.DescMsg.REASON: (
                        f'{root.Model.FOSSIL_COMMIT} failue: {error}'
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
            error_code=ec.GenericError.INVALID_STATE_ERROR,
            arg=timeline_output[:100] + (
                '...' if len(timeline_output) > 100 else timeline_output
            ),
            info='No valid commit data found in timeline output.',
        )
        error_data = builder.data()
        raise fossil_exception.FossilTimelineError(
            **error_data.to_exception()
        )

    return model.FossilTimeline(commits=parsed_commits)
