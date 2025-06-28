"""Provide common scripts as a python module.

This module uses 'click' to create command-line entry points for common
development tasks like formatting, linting, and type-checking. It is
designed to be integrated with the [project.scripts] section of pyproject.toml.
"""

import subprocess
import sys

import click


def _run_command(command: list[str], description: str) -> None:
    """Run a shell command and stream its output directly.

    This version avoids shell=True for security and allows the subprocess
    to inherit the main terminal, enabling real-time colored output
    from tools like ruff and mypy.

    Args:
        command: The command to execute as a list of strings.
        description: A user-friendly description of the action.

    """
    click.echo(click.style(f'--- {description} ---', bold=True))
    click.echo(click.style(f'$ {" ".join(command)}', fg='yellow'))

    process = subprocess.run(command, check=False)

    if process.returncode == 0:
        click.echo(
            click.style('---> Command finished successfully.\n', fg='green')
        )
    else:
        click.echo(
            click.style(
                f'---> Command failed with exit code {process.returncode}.\n',
                fg='red',
            ),
            err=True,
        )
        sys.exit(process.returncode)


@click.command()
@click.option(
    '--check',
    is_flag=True,
    help='Run formatters in check-only mode without modifying files.',
)
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
def format_code(check: bool, paths: tuple[str, ...]) -> None:
    """Run ruff to format code. Default paths are 'src' and 'tests'."""
    target_paths = paths or ('src', 'tests')
    description = (
        'Checking Python code formatting with ruff format'
        if check
        else 'Formatting Python code with ruff format'
    )
    cmd = ['ruff', 'format', *target_paths]
    if check:
        cmd.append('--check')
    _run_command(cmd, description)


@click.command()
@click.option('--fix', is_flag=True, help='Automatically fix lint errors.')
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
def lint(fix: bool, paths: tuple[str, ...]) -> None:
    """Run ruff to check for errors and style issues."""
    target_paths = paths or ('src', 'tests')
    description = (
        'Fixing lint errors with ruff check'
        if fix
        else 'Linting code with ruff check'
    )
    cmd = ['ruff', 'check', *target_paths]
    if fix:
        cmd.append('--fix')
    _run_command(cmd, description)


@click.command()
@click.argument('paths', nargs=-1)
def type_check(paths: tuple[str, ...]) -> None:
    """Run mypy to perform static type checking on the package."""
    cmd = ['mypy']
    if paths:
        cmd.extend(paths)
    else:
        cmd.extend(['-p', 'quarryforge'])
    _run_command(cmd, 'Type-checking with mypy')


@click.command()
@click.pass_context
def quality(ctx: click.Context) -> None:
    """Run all quality checks in sequence: format-check, lint, and type-check."""
    click.echo(
        click.style('--- Running all quality checks ---', bold=True, fg='blue')
    )
    ctx.invoke(format_code, check=True, paths=())
    ctx.invoke(lint, fix=False, paths=())
    ctx.invoke(type_check, paths=())
    click.echo(
        click.style(
            '--- 🎉 All quality checks passed! ---', bold=True, fg='green'
        )
    )
