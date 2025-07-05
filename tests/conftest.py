"""Global fixtures for the quarryforge test suite."""

import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from quarryforge import model

DATE_NOW = datetime.now().replace(
    year=datetime.now().year-1,
    month=datetime.now().month-3).isoformat().replace('T', ' ')
SRC_REPO_FILENAME = Path("src_test_repo.fossil")
SRC_WORKDIR_NAME = Path("src_workdir")
SRC_USER = "username"
SRC_CONTACT = "src@email"
TEST_REPO_FILENAME = Path("test_repo.fossil")
TEST_WORKDIR_NAME = Path("test_workdir")
UPDATED_USER = "github-username"
UPDATED_CONTACT = "github-username@email.test"


def _run_fossil_command(cmd: list[str], workdir: Path):
    """Helper to run a Fossil command in the correct working directory."""
    #capture_output=False to capture all fossil output
    subprocess.run(cmd, cwd=workdir, check=True, capture_output=True)


def _setup_test_src_config(
        src_repo: Path, user: str, date: str, workdir: Path):
    """Create a sample source fosisl repo for testing."""
    _run_fossil_command(
        ['fossil', 'new',
         '--admin-user', user,
         '--date-override', date, # for source test repo purposes
         '--project-name', 'test_source_repo',
         '--project-desc', 'test_source_repo description',
         str(src_repo)
         ],
        workdir
    )


def _setup_test_repo_config(
        src_repo: Path, new_repo: Path, user: str, date: str, workdir: Path):
    """Create a new repo file and workdir for testing."""
    _run_fossil_command(
        ['fossil', 'new',
         '--admin-user', user,
         '--date-override', date,
         '--template', str(src_repo),
         '--project-name', str(new_repo),
         '--project-desc', 'test description text',
         str(new_repo)
         ],
        workdir
    )


def _default_user_config(test_repo: Path, user: str, workdir: Path):
    """Set default user to match admin-user on test repo."""
    _run_fossil_command(
        ['fossil', 'user',
         'default', str(user),
         '-R', str(test_repo)
         ],
        workdir
    )


def _user_contact_config(
        test_repo: Path, user: str, contact: str, workdir: Path):
    """Set default user contact info."""
    _run_fossil_command(
        ['fossil', 'user',
         'contact', str(user), str(contact),
         '-R', str(test_repo)
         ],
        workdir
    )


def _open_test_repo(test_repo: Path, test_repo_work_dir: Path, workdir: Path):
    """Open a fossil test repository."""
    _run_fossil_command(
        ['fossil', 'open',
         str(test_repo),
         '--workdir', str(test_repo_work_dir),
         ],
        workdir
    )


def _write_safe(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _create_src_repo_timeline(
        src_repo: Path, test_repo: Path,
        test_repo_work_dir: Path, workdir: Path):
    """Create a sample fossil timeline in a new fossil repository file."""
    _setup_test_src_config(src_repo, SRC_USER, DATE_NOW, workdir)
    _default_user_config(src_repo, SRC_USER, workdir)
    _user_contact_config(src_repo, SRC_USER, SRC_CONTACT, workdir)
    _open_test_repo(src_repo, test_repo_work_dir, workdir)

    def _commit(comment: str, user: str, date: str, files_to_add: list[str]):
        if files_to_add:
            _run_fossil_command(
                ['fossil', 'add', *files_to_add],
                test_repo_work_dir
            )
        _run_fossil_command(
            ['fossil',
             'commit',
             '-m', comment,
             '--date-override',
             date,
             '--user-override',
             user
             ],
            test_repo_work_dir,
        )

    _write_safe(Path(test_repo_work_dir / "README.md"), "Initial README.")
    _write_safe(Path(test_repo_work_dir / "LICENSE"), "TEST License")
    _commit(
        "Initial commit with project structure.",
        str(SRC_USER),
        str(DATE_NOW),
        ["README.md", "LICENSE"]
    )
    _write_safe(
        Path(test_repo_work_dir  / "src/app.py"),
        "print('hello world')"
    )
    _commit(
        "Add hello world print statement.",
        str(SRC_USER),
        str(DATE_NOW),
        ["src/app.py"]
    )
    _write_safe(
        Path(test_repo_work_dir / "README.md"),
        "Initial README.\n\nUpdated with more info."
    )
    _commit(
        "Update README with usage instructions.",
        str(SRC_USER),
        str(DATE_NOW), []
    )

    _run_fossil_command(
        ['fossil', 'branch', 'new',
         '--date-override', str(DATE_NOW),
         'feature-branch', 'trunk'
         ],
        test_repo_work_dir
    )
    _run_fossil_command(
        ['fossil', 'update', 'feature-branch'],
        test_repo_work_dir
    )
    _write_safe(test_repo_work_dir / "src/utils.py", "def helper(): pass")
    _commit(
        "feat: Add utility functions on feature branch.",
        str(SRC_USER),
        str(DATE_NOW),
        ["src/utils.py"]
    )

    _run_fossil_command(['fossil', 'update', 'trunk'], test_repo_work_dir)

    _write_safe(
        test_repo_work_dir / "src/app.py",
        "print('hello, quarryforge!') # updated"
    )
    _commit(
        "refactor: Improve performance of app logic.",
        str(SRC_USER),
        str(DATE_NOW),
        []
    )

    _run_fossil_command(['fossil', 'merge', 'feature-branch'], test_repo_work_dir)
    _commit(
        "Merge feature-branch into trunk.",
        str(SRC_USER),
        str(DATE_NOW),
        []
    )

    _run_fossil_command(['fossil', 'rm', 'src/utils.py'], test_repo_work_dir)
    _commit(
        "refactor: Remove unused utils and tag v1.0.",
        str(SRC_USER),
        str(DATE_NOW),
        []
    )
    _run_fossil_command(
        ['fossil', 'tag', 'add', 'v1.0', 'trunk'],
        test_repo_work_dir
    )

    _run_fossil_command(['fossil', 'close'], test_repo_work_dir)

@pytest.fixture(scope="session")
def test_fossil_repo(tmp_path_factory) -> model.FossilRepo:
    """Provide a session-scoped fixture.

    This creates a complete Fossil repository with a history for testing.
    """
    base_tmp_path = tmp_path_factory.mktemp("fossil_session")
    repo_path = base_tmp_path / SRC_REPO_FILENAME
    workdir_path = base_tmp_path / SRC_WORKDIR_NAME
    workdir_path.mkdir()

    logging.info(f"\nCreating test Fossil repository at: {repo_path}")
    _create_src_repo_timeline(repo_path, workdir_path)

    yield model.FossilRepo(
        file=repo_path, workdir=workdir_path, is_new=False
    )

    logging.info(f"\nTest session finished. Temporary repo at {base_tmp_path} will be removed.")


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
