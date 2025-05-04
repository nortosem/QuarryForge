"""Main

The QuarryForge Main module provides common usage ability via the CLI.
"""
import argparse
import logging
from pathlib import Path
import sys
import tomllib
from typing import Dict

from quarryforge import fossil
from quarryforge.exceptions.main_exception import base_main_exception
from quarryforge.exceptions.main_exception. import ArgumentError


DEFAULT_CONFIG = {
    'verbosity': 0,
    'quiet': False,
}

def setup_logging(verbosity: int = 0, quiet: bool = False):
    """Setup Logging

    #todo
    """
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
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.debug('Logging level set to %s', logging.getLevelName(level))


def load_toml(config_path: Path) -> Dict:
    """Load TOML

    Loads the configuration from a TOML file.

    Args:
        config_path (Path): The pathlib.Path to the configuration file.
    """
    if not config_path.is_file():
        logging.warning('Config file not found: %s', config_path)
        return {}

    try:
        with open(config_path, 'rb') as f:
            config_data = tomllib.load(f)
            logging.info('Loaded configuration from %s', config_path)

            return config_data
    except base_main_exception.ArgumentError as e:
        logging.error('Error loading config file %s: %s', config_path, e)
        return {}


def parse_arguments(argv=None) -> argparse.Namespace:
    """Parses Arguments

    Define and parse the command line arguments.

    Args:
        argv (List): The arguments passed to the program from the commandline.
    """
    parser = argparse.ArgumentParser(
        description='Rebuilds a Fossil repository with updated username and '+
        'contact info.  All commits, comments, and timestamps are preserved.'+
        'Only solo developer repositories are supported currently.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-v', '--verbose',
        action='count',
        default=DEFAULT_CONFIG.get('verbosity', 0),
        help='Increase output verbosity: -v for INFO, -vv for DEBUG.'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        default=DEFAULT_CONFIG.get('quiet', False),
        help='Suppress all non-fatal outputs.'
    )

    args = parser.parse_args(argv)

    args.verbosity = args.verbose
    del args.verbose

    return args


def valid_config_data(config_data: dict) -> bool:
    """Valid Config Data

    Checks if the loaded config dictionary has required keys.

    Args:
        config_data (dict):
            The configuration dictionary laoded from the provided TOML file.
    """
    required_keys = {
        'source_repo',
        'rebuilt_repo',
        'rebuilt_project_dir',
    }
    missing_keys = required_keys - config_data.keys()
    if missing_keys:
        logging.error('TOML config missing required keys: %s,',
                      ', '.join(sorted(missing_keys)))
        return False

    logging.debug('Valid Configuration data found.')
    return True


def reforge_process(argv=None):
    """Reforge Process

    The application argument processor.

    Args:
        argv (list): The list of arguments passed from the command line.
    """
    if argv is None:
        argv = sys.argv[1:]

    args = parse_arguments(argv)

    setup_logging(args.verbosity, args.quiet)

    logging.debug('Parsed arguments: %s', args)
    logging.info('Starting Fossil rebuild process...')

    try:
        fossil.rebuild_repository_logic(
            source_repo=args.source_repo,
            rebuilt_repo=args.rebuilt_repo,
            rebuilt_checkout_dir=args.rebuilt_project_dir,
        )
        logging.info('Rebuild process completed successfully.')
    except base_main_exception.MainError as e:
        logging.exception('An error occurred during the rebuild process: %s', e)
        sys.exit(1)

if __name__ == '__main__':
    reforge_process()
