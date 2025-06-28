"""Provide common scripts as a python module.

Allow integration with pyproject.toml for common ruff, mypy, and coverage
testing.
"""

import subprocess
import sys

# Color codes for better terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'


def _run_command(command: str):
    """Help function to run a shell command and print its output."""
    print(f'{YELLOW}---> Running command: {command}{RESET}')
    result = subprocess.run(
        command, shell=True, text=True, capture_output=True, check=False
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f'{RED}{result.stderr}{RESET}')

    if result.returncode == 0:
        print(f'{GREEN}---> Command finished successfully.{RESET}\n')
    else:
        print(
            f'{RED}---> Command failed with exit code '
            f'{result.returncode}.{RESET}\n'
        )
        sys.exit(result.returncode)


def format_code():
    """Run ruff to format code and automatically fix linting errors."""
    print('--- Formatting and auto-fixing with ruff ---')
    _run_command('ruff format src tests')
    _run_command('ruff check src tests --fix')


def lint():
    """Run ruff to check for errors and style issues."""
    print('--- Linting with ruff ---')
    _run_command('ruff check src --fix') # tests')


def type_check():
    """Run mypy to perform static type checking on the package."""
    print('--- Type-checking with mypy ---')
    _run_command('mypy -p src/quarryforge')


def quality_check():
    """Run all quality checks in sequence."""
    format_code()
    lint()
    type_check()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        task_name = sys.argv[1]
        scripts = {
            'format': format_code,
            'lint': lint,
            'type-check': type_check,
            'quality': quality_check,
        }
        task = scripts.get(task_name)
        if task:
            task()
        else:
            print(f"{RED}Error: Unknown task '{task_name}'{RESET}")
            sys.exit(1)
    else:
        print('Usage: python scripts.py [format|lint|type-check|quality]')
