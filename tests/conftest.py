"""Global fixtures for the quarryforge test suite."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock
from typing import Any

import pytest

from quarryforge import model


TEST_REPO_FILENAME = "test-repo.fossil"
TEST_WORKDIR_NAME = "test-workdir"
USER_A = "original-username"
USER_B = "github-username"


def _run_fossil_command(cmd: list[str], workdir: Path):
    """Helper to run a Fossil command in the correct working directory."""
    subprocess.run(
        cmd,
        cwd=workdir,
        check=True,
        capture_output=True,
    )


def _create_test_repo_history(repo_path: Path, workdir: Path):
    """Create and populate a new Fossil repository with a commit history."""
    _run_fossil_command(
        ['fossil', 'new', str(repo_path)], workdir.parent
    )
    _run_fossil_command(
        ['fossil', 'open', str(repo_path)], workdir
    )

    def _commit(comment: str, user: str, date: str, files_to_add: list[str]):
        if files_to_add:
            _run_fossil_command(['fossil', 'add', *files_to_add], workdir)
        _run_fossil_command(
            [
                'fossil', 'commit',
                '-m', comment,
                '--date-override', date,
                '--user-override', user,
            ],
            workdir,
        )


    (workdir / "README.md").write_text("Initial README.")
    (workdir / "LICENSE").write_text("MIT License")
    _commit("Initial commit with project structure.", USER_A, "2024-01-01T10:00:00", ["README.md", "LICENSE"])

    (workdir / "src").mkdir()
    (workdir / "src/app.py").write_text("print('hello world')")
    _commit("Add core application logic.", USER_A, "2024-01-02T11:00:00", ["src/app.py"])

    (workdir / "README.md").write_text("Initial README.\n\nUpdated with more info.")
    _commit("Update README with usage instructions.", USER_A, "2024-01-03T12:00:00", [])

    _run_fossil_command(['fossil', 'branch', 'new', 'feature-branch', 'trunk'], workdir)
    _run_fossil_command(['fossil', 'update', 'feature-branch'], workdir)
    (workdir / "src/utils.py").write_text("def helper(): pass")
    _commit("feat: Add utility functions on feature branch.", USER_B, "2024-01-04T13:00:00", ["src/utils.py"])

    _run_fossil_command(['fossil', 'update', 'trunk'], workdir)
    (workdir / "src/app.py").write_text("print('hello, quarryforge!') # updated")
    _commit("refactor: Improve performance of app logic.", USER_A, "2024-01-04T14:00:00", [])

    _run_fossil_command(['fossil', 'merge', 'feature-branch'], workdir)
    _commit("Merge feature-branch into trunk.", USER_A, "2024-01-05T15:00:00", [])

    _run_fossil_command(['fossil', 'rm', 'src/utils.py'], workdir)
    _commit("refactor: Remove unused utils and tag v1.0.", USER_A, "2024-01-06T16:00:00", [])
    _run_fossil_command(['fossil', 'tag', 'add', 'v1.0', 'trunk'], workdir)

    _run_fossil_command(['fossil', 'close'], workdir)


@pytest.fixture(scope="session")
def test_fossil_repo(tmp_path_factory) -> model.FossilRepo:
    """Provide a session-scoped fixture.

    This creates a complete Fossil repository with a history for testing.
    """
    base_tmp_path = tmp_path_factory.mktemp("fossil_session")
    repo_path = base_tmp_path / TEST_REPO_FILENAME
    workdir_path = base_tmp_path / TEST_WORKDIR_NAME
    workdir_path.mkdir()

    print(f"\nCreating test Fossil repository at: {repo_path}")
    _create_test_repo_history(repo_path, workdir_path)

    yield model.FossilRepo(
        file=repo_path, workdir=workdir_path, is_new=False
    )

    print(f"\nTest session finished. Temporary repo at {base_tmp_path} will be removed.")


@pytest.fixture
def sample_repo_paths(tmp_path: Path) -> dict[str, Path]:
    """Provide valid, temporary Path objects for a repo and workdir."""
    return {'file': tmp_path / 'test.fossil', 'workdir': tmp_path / 'work'}


@pytest.fixture
def mock_repo() -> MagicMock:
    """Provide a reusable mock FossilRepo object for unit tests."""
    repo = MagicMock(spec=model.FossilRepo)
    repo.__str__.return_value = '/mock/repo.fossil'
    repo.file = Path('/mock/repo.fossil')
    repo.workdir = Path('/mock/workdir')
    return repo


@pytest.fixture
def sample_commit_data() -> dict[str, Any]:
    """Provide a dictionary of valid, reusable data for a FossilCommit."""
    return {
        'uuid': 'a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6',
        'date': '2023-01-01 12:00:00',
        'author': 'test_user',
        'comment': 'Initial commit',
        'branch': 'trunk',
        'tags': ['v1.0', 'stable'],
        'phase': ['LEAF'],
        'changes': [('ADDED', 'file1.txt'), ('EDITED', 'file2.txt')],
    }


@pytest.fixture
def sample_commit(sample_commit_data: dict[str, Any]) -> model.FossilCommit:
    """Provide a fully-formed FossilCommit instance for testing."""
    validator_return_tuple = (
        sample_commit_data['uuid'],
        sample_commit_data['date'],
        sample_commit_data['author'],
        sample_commit_data['comment'],
        sample_commit_data['branch'],
        sample_commit_data['tags'],
        sample_commit_data['phase'],
        sample_commit_data['changes'],
    )
    with patch(
        'quarryforge.util.model_util.viable_fossil_commit',
        return_value=validator_return_tuple,
    ):
        yield model.FossilCommit(**sample_commit_data)
