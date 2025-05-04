"""fossil

#todo
"""
from pathlib import Path
import subprocess

from quarryforge import config
from quarryforge.config import TimelineData
from quarryforge import model
from quarryforge.util import fossil_util


def repo_config(user: str,
                email: str,
                src_repo: Path,
                rebuild_repo: Path,
                project_name: str,
                project_desc: str,
                template: Path = None) -> model.RepoConfig:
    """Repository Configuration

    Prepare the updated repository configuration from a source repository.
    """
    src_repo = src_repo.expanduser()
    rebuild_repo = rebuild_repo.expanduser()
    template = template.expanduser()

    return model.RepoConfig(user, email, src_repo, project_name, project_desc)


def create_new_repo(args: model.RepoConfig) -> model.GetTimelineArg:
    """Create new repo

    #todo
    """
    try:
        initial_repo = subprocess.run(
            fossil_util.init_rebuild_repo(args),
            capture_output=True,
            check=True)
        default_user = subprocess.run(
            fossil_util.set_default_user(args),
            capture_output=True,
            check=True)
        user_contact = subprocess.run(
            fossil_util.set_user_contact(args),
            capture_output=True,
            check=True)
    except subprocess.CalledProcessError as cpe:
        raise subprocess.CalledProcessError(
            cpe.returncode, cpe.cmd, cpe.stdout,
            f'Repo Creation Process Error: {cpe}'
        ) from cpe

    # log output #todo
    output = (initial_repo.stdout.decode(),
              default_user.stdout.decode(),
              user_contact.stdout.decode())
    print(output) #logging info
    return model.GetTimelineArg(args.src)


def get_timeline(repo: model.GetTimelineArg) -> str:
    """Get Timeline

    #todo
    """
    try:
        timeline: subprocess.CompletedProcess[bytes] = subprocess.run(
            fossil_util.get_raw_timeline(repo.src),
            capture_output=True,
            check=True)
    except subprocess.CalledProcessError as cpe:
        raise subprocess.CalledProcessError(
            cpe.returncode, cpe.cmd, cpe.stdout,
            f'Timeline Process Exception: {cpe}') from cpe

    raw_timeline = timeline.stdout.decode()
    end_index = raw_timeline.find(TimelineData.END_MARK.value)
    return raw_timeline[:end_index]


def parse_timeline(timeline: str) -> model.Timeline:
    """Parse Timeline

    #todo
    """
    commits = TimelineData.commit_pattern()
    all_commits = commits.split(timeline)
    ci_hash = TimelineData.hash_pattern()
    ci_date = TimelineData.date_pattern()
    ci_author = TimelineData.author_pattern()
    ci_comment = TimelineData.comment_pattern()
    ci_branch = TimelineData.branch_pattern()
    ci_tags = TimelineData.tags_pattern()
    ci_phase = TimelineData.phase_pattern()
    ci_change = TimelineData.change_pattern()
    parsed_timeline = model.Timeline(commits = [])
    initial_checkin = 'initial empty check-in'

    for commit in all_commits:
        data = commit.split('\n')
        commit_data = {}
        for entry in data:
            if ci_hash.match(entry):
                commit_data[TimelineData.HASH.value] = ci_hash.match(
                    entry).group(TimelineData.HASH.value)
            elif ci_date.match(entry):
                commit_data[TimelineData.DATE.value] = ci_date.match(
                    entry).group(TimelineData.DATE.value)
            elif ci_author.match(entry):
                commit_data[TimelineData.AUTHOR.value] = ci_author.match(
                    entry).group(TimelineData.AUTHOR.value)
            elif ci_comment.match(entry):
                commit_data[TimelineData.COMMENT.value] = ci_comment.match(
                    entry).group(TimelineData.COMMENT.value)
            elif ci_branch.match(entry):
                commit_data[TimelineData.BRANCH.value] = ci_branch.match(
                    entry).group(TimelineData.BRANCH.value)
            elif ci_tags.match(entry):
                commit_data[TimelineData.TAGS.value] = ci_tags.match(
                    entry).group(TimelineData.TAGS.value).split(', ')
            elif ci_phase.match(entry):
                if ci_phase.match(entry) is None:
                    commit_data[TimelineData.PHASE.value] = None
                else:
                    commit_data[TimelineData.PHASE.value] = ci_phase.match(
                        entry).group(TimelineData.PHASE.value)
            elif ci_change.match(entry):
                if TimelineData.CHANGES.value is None:
                    commit_data[TimelineData.CHANGES.value] = [ci_change.match(
                        entry).groups()]
                else:
                    commit_data[TimelineData.CHANGES.value].append(
                        ci_change.match(entry).groups()
                    )
            elif commit_data[TimelineData.COMMENT.value] == initial_checkin:
                commit_data[TimelineData.CHANGES.value] = None

        new_commit = model.Commit(
            uuid=commit_data[TimelineData.HASH.value],
            date=commit_data[TimelineData.DATE.value],
            author=commit_data[TimelineData.AUTHOR.value],
            comment=commit_data[TimelineData.COMMENT.value],
            branch=commit_data[TimelineData.BRANCH.value],
            tags=commit_data[TimelineData.TAGS.value],
            phase=commit_data[TimelineData.PHASE.value],
            changes=commit_data[TimelineData.CHANGES.value])

        parsed_timeline.add(new_commit)

    return parsed_timeline


def get_changes(args: model.DiffArgs) -> str:
    """Get Changes

    #todo
    """
    try:
        diff_process: subprocess.CompletedProcess[bytes] = subprocess.run(
            fossil_util.get_file_changes(args),
            capture_output=True,
            check=True)
    except subprocess.CalledProcessError as cpe:
        raise subprocess.CalledProcessError(
            cpe.returncode, cpe.cmd, cpe.stdout,
            f'Fossil Diff Process Exception: {cpe}'
        ) from cpe
    raw_changes = diff_process.stdout.decode()
    return raw_changes


def get_content(args: model.CatArgs) -> str:
    """Get Content

    #todo
    """
    try:
        cat_process: subprocess.CompletedProcess[bytes] = subprocess.run(
            fossil_util.get_file_content(args),capture_output=True,check=True)
    except subprocess.CalledProcessError as cpe:
        raise subprocess.CalledProcessError(
            cpe.returncode, cpe.cmd, cpe.stdout,
            f'Fossil Cat Process Exception: {cpe}'
        ) from cpe
    content_changes = cat_process.stdout.decode()
    return content_changes
