"""The QuarryForge Main module provides common usage ability via the CLI."""

import logging
import sys
import tomllib
from pathlib import Path

import click

from quarryforge import model
from quarryforge.fossil import rebuild
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.exception import base_exception

# A tuple of all keys that can be set via CLI or TOML
CONFIG_KEYS = (
    'source_repo', 'source_workdir', 'rebuilt_repo', 'rebuilt_project_dir',
    'new_username', 'new_email', 'project_name', 'project_desc'
)

def setup_logging(verbosity: int, quiet: bool) -> None:
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
    logging.debug('Attempting to load TOML config from: %s', config_path)
    try:
        with config_path.open('rb') as f:
            config_data = tomllib.load(f)
            logging.info('Loaded configuration from %s', config_path)
            return config_data
    except tomllib.TOMLDecodeError as e:
        logging.error('Error parsing TOML config file %s: %s', config_path, e)
        details = {'path': str(config_path), ec.DescMsg.REASON: str(e)}
        raise base_exception.QuarryForgeError(
            code='CONFIG_PARSE_ERROR', message='Invalid TOML format.',
            user_message=(
                'The configuration file is improperly formatted and cannot '
                'be read.'
            ),
            details=details,
        ) from e


def valid_config_data(config_data: dict) -> bool:
    required_keys = {
        'source_repo', 'source_workdir', 'rebuilt_repo',
        'rebuilt_project_dir', 'new_username', 'new_email',
    }
    missing_keys = required_keys - set(config_data.keys())
    if missing_keys:
        logging.error(
            'Final config missing required keys: %s',
            ', '.join(sorted(missing_keys)),
        )
        return False
    logging.debug('Configuration data validated successfully.')
    return True


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option(
    '-c', '--config', 'config_path',
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        path_type=Path
    ),
    help=(
        'Path to a TOML configuration file. CLI options override file '
        'settings.'
    )
)
@click.option(
    '--source-repo',
    type=click.Path(),
    help='Path to the source Fossil repository file.'
)
@click.option(
    '--source-workdir',
    type=click.Path(),
    help='Path to a working checkout of the source repository.'
)
@click.option(
    '--rebuilt-repo',
    type=click.Path(),
    help='Path where the new repository file will be created.'
)
@click.option(
    '--rebuilt-project-dir',
    type=click.Path(),
    help='Directory for the new repository checkout.'
)
@click.option(
    '--new-username',
    help='The new username for commits.'
)
@click.option(
    '--new-email',
    help='The new email address for commits.'
)
@click.option(
    '--project-name',
    help='Optional: The "Project Name" for the new repository.'
)
@click.option(
    '--project-desc',
    help='Optional: The "Project Description" for the new repository.'
)
@click.option(
    '-v', '--verbose', 'verbosity',
    count=True,
    help='Increase output verbosity: -v for INFO, -vv for DEBUG.'
)
@click.option(
    '-q', '--quiet',
    is_flag=True,
    help='Suppress all non-fatal outputs.'
)
@click.pass_context
def main(ctx: click.Context, verbosity: int, quiet: bool, **kwargs) -> None:
    """Rebuild a Fossil repository with an updated username and contact info."""
    setup_logging(verbosity, quiet)

    try:
        # 1. Initialize config, starting with the TOML file if provided
        config_data = {}
        if kwargs.get('config_path'):
            config_data = load_toml(kwargs['config_path'])

        # 2. Overlay any provided CLI arguments on top of the TOML config
        for key in CONFIG_KEYS:
            cli_value = kwargs.get(key)
            if cli_value is not None:
                logging.debug(
                    "Overriding config '%s' with CLI value: %s",
                    key,
                    cli_value
                )
                config_data[key] = cli_value

        # 3. Validate the final, merged configuration
        if not valid_config_data(config_data):
            click.secho(
                'Error: Missing one or more required configuration fields. '
                'Please provide them in a --config file or via CLI options.',
                fg='red',
                err=True
            )
            sys.exit(1)

        logging.info('Starting Fossil rebuild process...')
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
        rebuild.user_info(
            source_repo=source_repo,
            rebuilt_repo=rebuilt_repo,
            new_username=config_data['new_username'],
            new_email=config_data['new_email'],
            project_name=config_data.get('project_name'),
            project_desc=config_data.get('project_desc'),
        )
        logging.info('Rebuild process completed successfully.')
        click.secho('✅ Rebuild process completed successfully.', fg='green')

    except base_exception.QuarryForgeError as e:
        logging.error(
            'A critical application error occurred: %s',
            e.user_message
        )
        logging.debug('Details: %s', e, exc_info=True)
        click.secho(f'Error: {e.user_message}', fg='red', err=True)
        sys.exit(1)
    except Exception as e:
        logging.exception('An unexpected critical error occurred: %s', e)
        click.secho(
            'A critical unexpected error occurred. Check logs for details.',
            fg='red',
            err=True
        )
        sys.exit(1)


if __name__ == '__main__':
    main()
