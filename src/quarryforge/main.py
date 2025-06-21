"""The QuarryForge Main module provides common usage ability via the CLI."""

import argparse
import logging
import sys
from pathlib import Path

import tomllib

from quarryforge import fossil, model
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.exception import base_exception
from quarryforge.exception.main_exception import MainError


def setup_logging(verbosity: int = 0, quiet: bool = False) -> None:
    """Setup Logging for the application."""
    level = logging.WARNING
    if quiet:
        level = logging.ERROR
    elif verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logging.debug('Logging level set to %s', logging.getLevelName(level))


def load_toml(config_path: Path) -> dict:
    """Loads the configuration from a TOML file.

    Args:
        config_path (Path): The pathlib.Path to the configuration file.

    Raises:
        MainError: If the file is not found or if there is a parsing error.
    """
    if not config_path.is_file():
        logging.error('Config file not found: %s', config_path)
        # Creating a dictionary for the exception
        details = {
            'path': str(config_path),
            ec.DESC_MSG.reason: 'File does not exist or is not a regular file.',
        }
        raise MainError(
            code='CONFIG_NOT_FOUND',
            message='Configuration file not found.',
            user_message='The specified configuration file could not be found.',
            details=details,
        )

    try:
        with open(config_path, 'rb') as f:
            config_data = tomllib.load(f)
            logging.info('Loaded configuration from %s', config_path)
            return config_data
    except tomllib.TOMLDecodeError as e:
        logging.error('Error parsing TOML config file %s: %s', config_path, e)
        details = {'path': str(config_path), ec.DESC_MSG.reason: str(e)}
        raise MainError(
            code='CONFIG_PARSE_ERROR',
            message='Invalid TOML format.',
            user_message='The configuration file is improperly formatted and cannot be read.',
            details=details,
        ) from e


def parse_arguments(argv: list[str] | None) -> argparse.Namespace:
    """Define and parse the command line arguments."""
    parser = argparse.ArgumentParser(
        description='Rebuilds a Fossil repository with updated username and contact info.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-c',
        '--config',
        type=Path,
        required=True,
        help='Path to the TOML configuration file.',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help='Increase output verbosity: -v for INFO, -vv for DEBUG.',
    )
    parser.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        default=False,
        help='Suppress all non-fatal outputs.',
    )
    args = parser.parse_args(argv)
    args.verbosity = args.verbose
    del args.verbose
    return args


def valid_config_data(config_data: dict) -> bool:
    """Checks if the loaded config dictionary has required keys."""
    required_keys = {
        'source_repo',
        'source_workdir',
        'rebuilt_repo',
        'rebuilt_project_dir',
        'new_username',
        'new_email',
    }
    missing_keys = required_keys - config_data.keys()
    if missing_keys:
        logging.error(
            'TOML config missing required keys: %s',
            ', '.join(sorted(missing_keys)),
        )
        return False
    logging.debug('Valid Configuration data found.')
    return True


def reforge_process(argv: list[str] | None = None) -> None:
    """The application argument processor and main entry point."""
    if argv is None:
        argv = sys.argv[1:]

    args = parse_arguments(argv)
    setup_logging(args.verbosity, args.quiet)
    logging.debug('Parsed arguments: %s', args)

    try:
        config_data = load_toml(args.config)
        if not valid_config_data(config_data):
            sys.exit(1)

        logging.info('Starting Fossil rebuild process...')

        # Create model instances from config, ensuring paths are validated on creation.
        source_repo = model.FossilRepo(
            file=config_data['source_repo'],
            workdir=config_data['source_workdir'],
            is_new=False,
        )
        rebuilt_repo = model.FossilRepo(
            file=config_data['rebuilt_repo'],
            workdir=config_data['rebuilt_project_dir'],
            is_new=True,
        )

        # Call the main logic function, which is now in the fossil module.
        fossil.rebuild_repository_logic(
            source_repo=source_repo,
            rebuilt_repo=rebuilt_repo,
            new_username=config_data['new_username'],
            new_email=config_data['new_email'],
            project_name=config_data.get('project_name'),
            project_desc=config_data.get('project_desc'),
        )
        logging.info('Rebuild process completed successfully.')

    except base_exception.QuarryForgeError as e:
        logging.error(
            'A controlled application error occurred: %s', e.user_message
        )
        logging.debug('Details: %s', e, exc_info=True)
        sys.exit(1)
    except Exception as e:
        logging.exception('An unexpected critical error occurred: %s', e)
        sys.exit(1)


if __name__ == '__main__':
    reforge_process()
