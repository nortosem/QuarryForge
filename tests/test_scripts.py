"""Comprehensive unit tests for the scripts.py module.

This suite uses pytest, mocker, and CliRunner to test the command-line
interface functions in isolation. It verifies that the correct subprocess
commands are constructed based on user input, without executing them.
"""

import subprocess
from unittest.mock import MagicMock, call

import pytest
from click.testing import CliRunner

import quarryforge
import scripts


@pytest.fixture
def mock_subprocess(mocker: MagicMock) -> MagicMock:
    """Fixture to mock subprocess.run, returning success by default.

    Patch 'scripts.subprocess.run' because that is where the object is looked
    up when the code under test is executed.
    """
    mock = mocker.patch('scripts.subprocess.run', autospec=True)
    mock.return_value = subprocess.CompletedProcess(args=[], returncode=0)
    return mock


class TestScripts:
    """Test suite for the command-line scripts."""

    def test_format_code_default(self, mock_subprocess: MagicMock) -> None:
        """Test `format-code` with default paths."""
        runner = CliRunner()
        result = runner.invoke(scripts.format_code)

        assert result.exit_code == 0
        expected_cmd = ['ruff', 'format', 'src', 'tests']
        mock_subprocess.assert_called_once_with(expected_cmd, check=False)

    def test_format_code_with_check(self, mock_subprocess: MagicMock) -> None:
        """Test `format-code` with the --check flag."""
        runner = CliRunner()
        result = runner.invoke(scripts.format_code, ['--check'])

        assert result.exit_code == 0
        expected_cmd = ['ruff', 'format', 'src', 'tests', '--check']
        mock_subprocess.assert_called_once_with(expected_cmd, check=False)

    def test_lint_with_fix_and_path(
        self, mock_subprocess: MagicMock, tmp_path
    ) -> None:
        """Test `lint` with --fix and a custom path."""
        runner = CliRunner()
        custom_path = tmp_path / 'my_module'
        custom_path.mkdir()
        result = runner.invoke(scripts.lint, ['--fix', str(custom_path)])

        assert result.exit_code == 0
        expected_cmd = ['ruff', 'check', str(custom_path), '--fix']
        mock_subprocess.assert_called_once_with(expected_cmd, check=False)

    def test_type_check_default(self, mock_subprocess: MagicMock) -> None:
        """Test `type-check` with its default package target."""
        runner = CliRunner()
        result = runner.invoke(scripts.type_check)

        assert result.exit_code == 0
        expected_cmd = ['mypy', '-p', 'quarryforge']
        mock_subprocess.assert_called_once_with(expected_cmd, check=False)

    def test_type_check_with_paths(self, mock_subprocess: MagicMock) -> None:
        """Test `type-check` when provided with explicit paths."""
        runner = CliRunner()
        paths_to_check = ['src/quarryforge', 'tests']
        result = runner.invoke(scripts.type_check, paths_to_check)

        assert result.exit_code == 0
        expected_cmd = ['mypy', 'src/quarryforge', 'tests']
        mock_subprocess.assert_called_once_with(expected_cmd, check=False)

    def test_command_failure_exits(self, mock_subprocess: MagicMock) -> None:
        """Test that a failed command returns a non-zero exit code."""
        mock_subprocess.return_value = subprocess.CompletedProcess(
            args=[], returncode=1
        )
        runner = CliRunner()
        result = runner.invoke(scripts.lint)

        # Assert on the exit code that CliRunner captures from SystemExit
        assert result.exit_code == 1
        mock_subprocess.assert_called_once()

    def test_quality_invokes_all_checks(self, mock_subprocess: MagicMock) -> None:
        """Verify `quality` invokes all three checks with correct args."""
        runner = CliRunner()
        result = runner.invoke(scripts.quality)

        assert result.exit_code == 0
        calls = [
            call(['ruff', 'format', 'src', 'tests', '--check'], check=False),
            call(['ruff', 'check', 'src', 'tests'], check=False),
            call(['mypy', '-p', 'quarryforge'], check=False),
        ]
        mock_subprocess.assert_has_calls(calls, any_order=False)
        assert mock_subprocess.call_count == 3

    def test_run_coverage_default(self, mock_subprocess: MagicMock) -> None:
        """Test `run-coverage` with no specific test paths."""
        runner = CliRunner()
        result = runner.invoke(scripts.run_coverage)

        assert result.exit_code == 0
        expected_cmd = ['coverage', 'run', '-m', 'pytest']
        mock_subprocess.assert_called_once_with(expected_cmd, check=False)

    def test_run_coverage_with_args(self, mock_subprocess: MagicMock) -> None:
        """Test `run-coverage` with specific pytest arguments."""
        runner = CliRunner()
        result = runner.invoke(scripts.run_coverage, ['tests/test_a.py'])

        assert result.exit_code == 0
        expected_cmd = ['coverage', 'run', '-m', 'pytest', 'tests/test_a.py']
        mock_subprocess.assert_called_once_with(expected_cmd, check=False)

    def test_report_coverage_default(self, mock_subprocess: MagicMock) -> None:
        """Test `report-coverage` default behavior."""
        runner = CliRunner()
        result = runner.invoke(scripts.report_coverage)

        assert result.exit_code == 0
        calls = [
            call(['coverage', 'report'], check=False),
            call(['coverage', 'html'], check=False),
        ]
        mock_subprocess.assert_has_calls(calls, any_order=False)

    def test_report_coverage_with_show_missing(
        self, mock_subprocess: MagicMock
    ) -> None:
        """Test `report-coverage` with the --show-missing flag."""
        runner = CliRunner()
        result = runner.invoke(scripts.report_coverage, ['--show-missing'])

        assert result.exit_code == 0
        calls = [
            call(['coverage', 'report', '-m'], check=False),
            call(['coverage', 'html'], check=False),
        ]
        mock_subprocess.assert_has_calls(calls, any_order=False)

    def test_full_coverage_invokes_pipeline(
        self, mock_subprocess: MagicMock
    ) -> None:
        """Verify `full-coverage` invokes run and report sequentially."""
        runner = CliRunner()
        result = runner.invoke(
            scripts.full_coverage, ['tests/test_specific.py']
        )

        assert result.exit_code == 0
        calls = [
            call(
                ['coverage', 'run', '-m', 'pytest', 'tests/test_specific.py'],
                check=False,
            ),
            call(['coverage', 'report'], check=False),
            call(['coverage', 'html'], check=False),
        ]
        mock_subprocess.assert_has_calls(calls, any_order=False)
        assert mock_subprocess.call_count == 3
