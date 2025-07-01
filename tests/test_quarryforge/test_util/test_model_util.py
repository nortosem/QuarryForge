"""Test suite for the core data models in quarryforge.model."""

from pathlib import Path

import pytest

from quarryforge.exception import meta_exception, model_exception
from quarryforge.model import FossilCommit, FossilRepo, FossilTimeline


@pytest.fixture
def mock_dependencies(mocker):
    """Mocks all external dependencies for the model module."""
    # Mock validation utilities
    mocker.patch('quarryforge.util.model_util.viable_fossil_repo')
    mocker.patch('quarryforge.util.model_util.viable_fossil_commit')

    # Mock configuration modules and error builders
    mocker.patch('quarryforge.model.model_config')
    mocker.patch('quarryforge.model.meta_config')
    mocker.patch('quarryforge.model.meta_ec.MetaErrorBuilder')
    mocker.patch('quarryforge.model.model_ec.FossilTimelineErrorBuilder')


@pytest.mark.usefixtures('mock_dependencies')
class TestFossilRepo:
    def test_init_success(self, sample_repo_paths):
        """Tests successful initialization of FossilRepo."""
        from quarryforge.util import model_util

        repo_paths = sample_repo_paths
        model_util.viable_fossil_repo.return_value = (
            repo_paths['file'],
            repo_paths['workdir'],
        )

        repo = FossilRepo(
            file=repo_paths['file'], workdir=repo_paths['workdir'], is_new=False
        )

        assert repo.file == repo_paths['file']
        assert repo.workdir == repo_paths['workdir']
        assert repo.is_new is False
        model_util.viable_fossil_repo.assert_called_once_with(
            repo_paths['file'],
            repo_paths['workdir'],
            False,
            model_exception.FossilRepoError,
        )

    def test_init_failure(self, sample_repo_paths):
        """Tests that FossilRepo raises an error if validation fails."""
        from quarryforge.util import model_util

        repo_paths = sample_repo_paths
        model_util.viable_fossil_repo.side_effect = (
            model_exception.FossilRepoError('Validation failed')
        )

        with pytest.raises(
            model_exception.FossilRepoError, match='Validation failed'
        ):
            FossilRepo(
                file=repo_paths['file'],
                workdir=repo_paths['workdir'],
                is_new=True,
            )

    def test_immutability(self, sample_repo_paths):
        """Tests that FossilRepo instances are immutable."""
        from quarryforge.util import model_util

        repo_paths = sample_repo_paths
        model_util.viable_fossil_repo.return_value = (
            repo_paths['file'],
            repo_paths['workdir'],
        )
        repo = FossilRepo(
            file=repo_paths['file'], workdir=repo_paths['workdir'], is_new=False
        )

        with pytest.raises(meta_exception.ImmutableError):
            repo.file = Path('/new/path')
        with pytest.raises(meta_exception.ImmutableError):
            del repo.file

    def test_str_representation(self, sample_repo_paths):
        """Tests the __str__ method."""
        from quarryforge.util import model_util

        repo_paths = sample_repo_paths
        model_util.viable_fossil_repo.return_value = (
            repo_paths['file'],
            repo_paths['workdir'],
        )
        repo = FossilRepo(
            file=repo_paths['file'], workdir=repo_paths['workdir'], is_new=False
        )

        expected_str = (
            f'Fossil Repository File: {repo.file}\n'
            f'Working Directory: {repo.workdir}'
        )
        assert str(repo) == expected_str

    def test_repr_representation(self, sample_repo_paths):
        """Tests the __repr__ method."""
        from quarryforge.util import model_util

        repo_paths = sample_repo_paths
        model_util.viable_fossil_repo.return_value = (
            repo_paths['file'],
            repo_paths['workdir'],
        )
        repo = FossilRepo(
            file=repo_paths['file'], workdir=repo_paths['workdir'], is_new=False
        )

        expected_repr = (
            f'FossilRepo(file={repo.file!r}, '
            f'is_new={repo.is_new!r}, '
            f'workdir={repo.workdir!r})'
        )
        assert repr(repo) == expected_repr

    def test_equality_and_hash(self, sample_repo_paths):
        """Tests the __eq__ and __hash__ methods."""
        from quarryforge.util import model_util

        repo_paths = sample_repo_paths
        model_util.viable_fossil_repo.return_value = (
            repo_paths['file'],
            repo_paths['workdir'],
        )

        repo1 = FossilRepo(
            file=repo_paths['file'], workdir=repo_paths['workdir'], is_new=False
        )
        repo2 = FossilRepo(
            file=repo_paths['file'], workdir=repo_paths['workdir'], is_new=False
        )
        repo3 = FossilRepo(
            file=repo_paths['file'], workdir=repo_paths['workdir'], is_new=True
        )  # Different is_new
        repo4 = FossilRepo(
            file=repo_paths['file'], workdir=Path('/different'), is_new=False
        )  # Different workdir

        assert repo1 == repo2
        assert repo1 != repo3
        assert repo1 != repo4
        assert repo1 != 'not a repo'
        assert hash(repo1) == hash(repo2)
        assert hash(repo1) != hash(repo3)
        assert hash(repo1) != hash(repo4)


@pytest.mark.usefixtures('mock_dependencies')
class TestFossilCommit:
    def test_init_success_all_args(self, sample_commit_args):
        """Tests successful initialization with all arguments."""
        from quarryforge.util import model_util

        model_util.viable_fossil_commit.return_value = tuple(
            sample_commit_args.values()
        )

        commit = FossilCommit(**sample_commit_args)

        assert commit.uuid == sample_commit_args['uuid']
        assert commit.author == sample_commit_args['author']
        assert commit.branch == sample_commit_args['branch']
        assert commit.tags == sample_commit_args['tags']
        assert commit.phase == sample_commit_args['phase']
        assert commit.changes == sample_commit_args['changes']
        model_util.viable_fossil_commit.assert_called_once_with(
            **sample_commit_args, exception=model_exception.FossilCommitError
        )

    def test_init_success_optional_args_as_none(self, sample_commit_args):
        """Tests that optional None arguments result in empty lists."""
        from quarryforge.util import model_util

        args = sample_commit_args.copy()
        args['tags'] = None
        args['changes'] = None

        # Simulate validation returning None for optional args
        validated_args = list(args.values())
        model_util.viable_fossil_commit.return_value = tuple(validated_args)

        commit = FossilCommit(**args)
        assert commit.tags == []
        assert commit.changes == []

    def test_init_failure(self, sample_commit_args):
        """Tests that FossilCommit raises an error if validation fails."""
        from quarryforge.util import model_util

        model_util.viable_fossil_commit.side_effect = (
            model_exception.FossilCommitError('Invalid commit data')
        )

        with pytest.raises(
            model_exception.FossilCommitError, match='Invalid commit data'
        ):
            FossilCommit(**sample_commit_args)

    def test_get_hash(self, sample_commit):
        """Tests the get_hash method for correct slicing."""
        assert sample_commit.get_hash() == sample_commit.uuid[:12]

    def test_immutability(self, sample_commit):
        """Tests that FossilCommit instances are immutable."""
        with pytest.raises(meta_exception.ImmutableError):
            sample_commit.uuid = 'new_uuid'
        with pytest.raises(meta_exception.ImmutableError):
            del sample_commit.uuid

    def test_str_representation(self, sample_commit):
        """Tests the __str__ method for user-friendly output."""
        expected_str = (
            f'uuid: {sample_commit.get_hash()}\n'
            f'date: {sample_commit.date}\n'
            f'author: {sample_commit.author}\n'
            f'comment: {sample_commit.comment}'
        )
        assert str(sample_commit) == expected_str

    def test_repr_representation(self, sample_commit):
        """Tests the __repr__ method for developer-friendly output."""
        # Just check for key elements, as the full repr is complex
        repr_str = repr(sample_commit)
        assert 'FossilCommit' in repr_str
        assert f"uuid='{sample_commit.uuid}'" in repr_str
        assert f"author='{sample_commit.author}'" in repr_str
        assert "tags=['v1.0']" in repr_str
        assert "changes=[('ADDED', 'file.txt')]" in repr_str


@pytest.mark.usefixtures('mock_dependencies')
class TestFossilTimeline:
    def test_init_success_empty_and_none(self):
        """Tests initialization with no commits or None."""
        timeline_none = FossilTimeline(commits=None)
        timeline_empty = FossilTimeline(commits=[])
        assert len(timeline_none) == 0
        assert len(timeline_empty) == 0

    def test_init_success_with_commits(self, sample_commit):
        """Tests initialization with a list of commits and verifies reversal."""
        commit1 = sample_commit
        commit2 = FossilCommit(
            uuid='b' * 40, date='2023-01-02...', author='t', comment='c'
        )

        timeline = FossilTimeline(commits=[commit1, commit2])
        assert len(timeline) == 2
        assert timeline[0] == commit2
        assert timeline[1] == commit1

    def test_init_fail_not_a_list(self):
        """Tests that __init__ raises an error if `commits` is not a list."""
        with pytest.raises(
            model_exception.FossilTimelineError, match='must be a list'
        ):
            FossilTimeline(commits='not a list')

    def test_init_fail_invalid_item_in_list(self, sample_commit):
        """Tests that __init__ raises an error if list contains
        non-FossilCommit items.
        """
        with pytest.raises(
            model_exception.FossilTimelineError,
            match='must be .*FossilCommit.* instances',
        ):
            FossilTimeline(commits=[sample_commit, 'not a commit'])

    def test_add_commit(self, sample_commit):
        """Tests the add method."""
        timeline = FossilTimeline()
        timeline.add(sample_commit)
        assert len(timeline) == 1
        assert timeline[0] == sample_commit

    def test_container_protocol(self, sample_commit):
        """Tests __len__, __getitem__, and __iter__."""
        commit1 = sample_commit
        commit2 = FossilCommit(
            uuid='b' * 40, date='2023-01-02...', author='t', comment='c'
        )
        timeline = FossilTimeline(commits=[commit1, commit2])

        assert len(timeline) == 2
        assert timeline[0] == commit2

        items = [c for c in timeline]
        assert items == [commit2, commit1]

    def test_repr_and_str_representation(self, sample_commit):
        """Tests the __repr__ and __str__ methods."""
        timeline = FossilTimeline(commits=[sample_commit])
        assert repr(timeline) == 'FossilTimeline(commits=1 commits)'
        assert str(timeline) == 'Fossil Timeline with 1 commits.'
