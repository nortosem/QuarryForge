"""models

#todo
"""
from quarryforge.config import InfoData
from quarryforge.config import TimelineData

from quarryforge.util import InfoArgs
from quarryforge.util import get_parent_hash

import subprocess
from subprocess import CalledProcessError
from subprocess import CompletedProcess

from typing import List
from typing import Optional


class Commit:
    """Commit

    #todo
    """
    __slots__ = TimelineData.commit_slots()

    def __init__(self, uuid: str = None, date: str = None, author: str = None,
                 comment: str = None, branch: str = None,
                 tags: Optional[List[str]] = None, phase: str = None,
                 changes: Optional[List[str]] = None):
        object.__setattr__(self, TimelineData.HASH.value, uuid)
        object.__setattr__(self, TimelineData.DATE.value, date)
        object.__setattr__(self, TimelineData.AUTHOR.value, author)
        object.__setattr__(self, TimelineData.COMMENT.value, comment)
        object.__setattr__(self, TimelineData.BRANCH.value, branch)
        if tags:
            object.__setattr__(self, TimelineData.TAGS.value, tags)
        if tags is None:
            object.__setattr__(self, TimelineData.TAGS.value, [])
        object.__setattr__(self, TimelineData.PHASE.value, phase)
        if changes:
            object.__setattr__(self,TimelineData.CHANGES.value,changes)
        if changes is None:
            object.__setattr__(self, TimelineData.CHANGES.value, [])

    def __setattr__(self, name, value):
        """Commits are Immutable"""
        #custom package exceptions
        raise Exception('Commits are immutable')

    def __repr__(self):
        """Official String Represenation of a Commit"""
        #todo unquote list args && quote str args
        attributes = ', '.join(
            f"{slot}={getattr(self,slot)}" for slot in self.__slots__)
        return f'{self.__class__.__name__}({attributes})'

    def __str__(self):
        """Standard string output for a Commit."""
        uuid = self.uuid[:12]
        return f'uuid: {uuid}\ndate: {self.date}\ncomment: {self.comment}'

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
            return match_parent.group(TimelineData.HASH.value)
        if match_init:
            return None
        else:
            raise Exception('unexpected error')

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
