"""Unit tests: quarryforge.config.exception_conf.model_exception_config module."""

import pytest

from quarryforge.config import model_config, root
from quarryforge.config.exception_conf import base_exception_config as bec
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.config.exception_conf import model_exception_config as moec


class TestModelExceptionConfigModule:
    """Tests for module-level constants in model_exception_config."""

    def test_module_dunder_all(self):
        expected = [
            'FossilRepoErrorBuilder',
            'FossilCommitErrorBuilder',
            'FossilTimelineErrorBuilder',
        ]
        assert sorted(moec.__all__) == sorted(expected)

    def test_model_error_path_enum(self):
        """Test ModelErrorPath attributes for correct path construction."""
        commit_root = bec.get_full_error_code(
            bec.BaseErrorPath.MODEL, root.Model.FOSSIL_COMMIT
        )
        repo_root = bec.get_full_error_code(
            bec.BaseErrorPath.MODEL, root.Model.FOSSIL_REPO
        )
        timeline_root = bec.get_full_error_code(
            bec.BaseErrorPath.MODEL, root.Model.FOSSIL_TIMELINE
        )
        assert moec.ModelErrorPath._FOSSIL_COMMIT_ROOT == commit_root
        assert moec.ModelErrorPath._FOSSIL_REPO_ROOT == repo_root
        assert moec.ModelErrorPath._FOSSIL_TIMELINE_ROOT == timeline_root

        assert moec.ModelErrorPath.FOSSIL_REPO_INIT == f'{repo_root}.__init__'
        assert moec.ModelErrorPath.FOSSIL_COMMIT_INIT == (
            f'{commit_root}.__init__'
        )
        assert moec.ModelErrorPath.FOSSIL_COMMIT_PARSE == (
            f'{commit_root}.parse'
        )
        assert moec.ModelErrorPath.FOSSIL_TIMELINE_INIT == (
            f'{timeline_root}.__init__'
        )
        assert moec.ModelErrorPath.FOSSIL_TIMELINE_PARSE == (
            f'{timeline_root}.parse'
        )
        assert moec.ModelErrorPath.FOSSIL_TIMELINE_NO_COMMITS == (
            f'{timeline_root}.no_commits_data'
        )


class TestFossilRepoErrorBuilder:
    """Tests for the FossilRepoErrorBuilder."""

    def test_inheritance(self):
        assert issubclass(moec.FossilRepoErrorBuilder, bec.BaseErrorBuilder)

    @pytest.mark.parametrize(
        'error_code, arg, info, extra_details, expected_message',
        [
            (   # === StringError cases ===
                ec.StringError.EMPTY_STRING_ERROR,
                '',
                'a non-empty string',
                None,
                (
                    'Error in `ctx.repo` (Code: EMPTY_STRING_ERROR). String '
                    'argument is empty or only whitespace. Expected: a '
                    'non-empty string.'
                ),
            ),
            (   # === PathError cases ===
                ec.StringError.INVALID_CHARS_ERROR,
                'bad!',
                '/[a-z]+/',
                None,
                (
                    'Error in `ctx.repo` (Code: INVALID_CHARS_ERROR). '
                    'String \'bad!\' contains invalid characters or patterns. '
                    'Expected pattern: /[a-z]+/.'
                ),
            ),
            (
                ec.PathError.NON_PATH_OBJECT_ERROR,
                123,
                None,
                None,
                'Error in `ctx.repo` (Code: NON_PATH_OBJECT_ERROR). Argument '
                '123 is not a valid path or  convertible to one.'
            ),
            (
                ec.PathError.INVALID_PATH_STRING_ERROR,
                'invalid:path',
                None,
                None,
                (
                    'Error in `ctx.repo` (Code: INVALID_PATH_STRING_ERROR). '
                    'The provided string \'invalid:path\' cannot be  interpreted '
                    'as a valid system path.'
                ),
            ),
            (
                ec.PathError.PATH_RESOLUTION_ERROR,
                '~/../a/b',
                None,
                {'reason': 'Symbolic link loop detected'},
                (
                    'Error in `ctx.repo` (Code: PATH_RESOLUTION_ERROR). '
                    'Path resolution failed for \'~/../a/b\'.  Reason: '
                    'Symbolic link loop detected.'
                ),
            ),
            (
                ec.PathError.PATH_NONEXISTENT_ERROR,
                '/no/such/path',
                None,
                None,
                (
                    'Error in `ctx.repo` (Code: PATH_NONEXISTENT_ERROR). Path '
                    '\'/no/such/path\' is expected to exist, but does not.'
                ),
            ),
            (
                ec.PathError.PATH_EXISTING_ERROR,
                '/already/exists',
                None,
                None,
                (
                    'Error in `ctx.repo` (Code: PATH_EXISTING_ERROR). Path '
                    '\'/already/exists\' is expected not to exist (for '
                    'creation), but already does.'
                ),
            ),
            (
                ec.PathError.PATH_NOT_A_FILE_ERROR,
                '/path/is/dir',
                None,
                None,
                (
                    'Error in `ctx.repo` (Code: PATH_NOT_A_FILE_ERROR). Path '
                    '\'/path/is/dir\' is expected to be a file, but it is a '
                    'directory.'
                ),
            ),
            (
                ec.PathError.PATH_NOT_A_DIRECTORY_ERROR,
                '/path/is/file.txt',
                None,
                None,
                (
                    'Error in `ctx.repo` (Code: PATH_NOT_A_DIRECTORY_ERROR). '
                    'Path \'/path/is/file.txt\' is expected to be a directory, '
                    'but it is a file.'
                ),
            ),
            (
                ec.PathError.PATH_NOT_READABLE_ERROR,
                '/no/read/perms',
                None,
                None,
                (
                    'Error in `ctx.repo` (Code: PATH_NOT_READABLE_ERROR). Path '
                    '\'/no/read/perms\' lacks read permissions.'
                )
            ),
            (
                ec.PathError.PATH_NOT_WRITABLE_ERROR,
                '/no/write/perms',
                None,
                None,
                (
                    'Error in `ctx.repo` (Code: PATH_NOT_WRITABLE_ERROR). Path '
                    '\'/no/write/perms\' lacks write permissions.'
                ),
            ),
            (
                ec.PathError.PATH_NOT_EXECUTABLE_ERROR,
                '/no/exec/perms',
                None,
                None,
                (
                    'Error in `ctx.repo` (Code: PATH_NOT_EXECUTABLE_ERROR). Path '
                    '\'/no/exec/perms\' lacks execute permissions.'
                ),
            ),
            (
                ec.PathError.SAME_REPO_DIR_AND_WORK_DIR,
                None,
                None,
                None,
                (
                    'Error in `ctx.repo` (Code: SAME_REPO_DIR_AND_WORK_DIR). '
                    'Fossil repository directory matches the working directory.'
                ),
            ),
            (   # === Fallback to BaseErrorBuilder case ===
                ec.GenericError.VALUE_ERROR,
                'bad_value',
                'good_value',
                None,
                (
                    'Error in `ctx.repo` (Code: VALUE_ERROR). Value '
                    '\'bad_value\' is invalid. Expected value: good_value.'
                ),
            ),
        ],
    )
    def test_message_mcdc(self, error_code, arg, info, extra_details, expected_message):
        """Test the message() method for all defined error codes."""
        builder = moec.FossilRepoErrorBuilder(
            error_context='ctx.repo',
            error_code=error_code,
            arg=arg,
            info=info,
            extra_details=extra_details,
        )
        assert builder.message() == expected_message

    @pytest.mark.parametrize(
        'error_code, expected_user_message',
        [
            (
                ec.PathError.PATH_NONEXISTENT_ERROR,
                'A required file or directory was not found.',
            ),
            (
                ec.PathError.SAME_REPO_DIR_AND_WORK_DIR,
                (
                    'The fossil repository parent directory is the '
                    'same directory as the workdir.'
                ),
            ),
            (ec.StringError.EMPTY_STRING_ERROR, 'A required text input was left empty.'),
            (
                ec.GenericError.CONFIGURATION_ERROR,
                'There is an issue with the configuration.',
            ),  # Fallback
        ],
    )
    def test_user_message_mcdc(self, error_code, expected_user_message):
        builder = moec.FossilRepoErrorBuilder(
            error_context='ctx', error_code=error_code
        )
        assert builder.user_message() == expected_user_message


class TestFossilCommitErrorBuilder:
    """Tests for the FossilCommitErrorBuilder."""

    @pytest.mark.parametrize(
        'error_context, error_code, field, arg, info, expected_message',
        [
            (   # Test case for the specific INVALID_CHARS_ERROR on a UUID field
                moec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                ec.StringError.INVALID_CHARS_ERROR,
                model_config.fossil_commit_config().uuid,
                'bad-uuid',
                'a valid string',
                (
                    'Error in `quarryforge.model.FossilCommit.__init__` '
                    "(Code: INVALID_CHARS_ERROR). Commit UUID 'bad-uuid' is "
                    'not a valid format. Expected: a valid string '
                    '(e.g., 40-char SHA-3 hex).'
                ),
            ),
            (   # Test case for a generic INVALID_CHARS_ERROR (fallback path)
                moec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                ec.StringError.INVALID_CHARS_ERROR,
                'author',
                'bad author!',
                None,
                (
                    'Error in `quarryforge.model.FossilCommit.__init__` (Code: '
                    'INVALID_CHARS_ERROR). Error code INVALID_CHARS_ERROR '
                    'unhandled is an unexpected error.'
                ),
            ),
            (   # Test case for VALUE_ERROR during parsing
                moec.ModelErrorPath.FOSSIL_COMMIT_PARSE,
                ec.GenericError.VALUE_ERROR,
                None,
                'bad data',
                None,
                (
                    'Error in `quarryforge.model.FossilCommit.parse` (Code: '
                    'VALUE_ERROR). Failed to parse commit data from \'bad '
                    'data\'. Reason: unknown.'
                ),
            ),
            (   # Test case for INVALID_STATE_ERROR on a specific field
                moec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                ec.GenericError.INVALID_STATE_ERROR,
                'author',
                'some commit',
                None,
                (
                    'Error in `quarryforge.model.FossilCommit.__init__` (Code: '
                    'INVALID_STATE_ERROR). Required field "author" is missing or '
                    'empty in commit data for \'some commit\'.'
                ),
            ),
            (   # Fallback
                moec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                ec.GenericError.TYPE_ERROR,
                None,
                123,
                'a valid string',
                (
                    'Error in `quarryforge.model.FossilCommit.__init__` '
                    '(Code: TYPE_ERROR). Expected type: a valid string. Got '
                    'type int with value 123 instead.'
                ),
            ),
        ],
    )
    def test_message_mcdc(
        self,
        error_context,
        error_code,
        field,
        arg,
        info,
        expected_message,
    ):
        builder = moec.FossilCommitErrorBuilder(
            error_context=error_context,
            error_code=error_code,
            field=field,
            arg=arg,
            info=info
        )
        assert builder.message() == expected_message

    @pytest.mark.parametrize(
        'error_context, error_code, field, expected_user_message',
        [
            (
                moec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                ec.StringError.INVALID_CHARS_ERROR,
                model_config.fossil_commit_config().uuid,
                'The commit identifier (UUID) is in an invalid format.',
            ),
            (
                moec.ModelErrorPath.FOSSIL_COMMIT_PARSE,
                ec.GenericError.VALUE_ERROR,
                None,
                'Could not understand the commit information provided.',
            ),
            (
                moec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                ec.GenericError.INVALID_STATE_ERROR,
                'comment',
                'A required piece of commit information (comment) was missing.',
            ),
            (   # Fallback
                moec.ModelErrorPath.FOSSIL_COMMIT_INIT,
                ec.GenericError.NOT_IMPLEMENTED_ERROR,
                None,
                'This feature is not available.',
            ),
        ],
    )
    def test_user_message_mcdc(
        self, error_context, error_code, field, expected_user_message
    ):
        builder = moec.FossilCommitErrorBuilder(
            error_context=error_context, error_code=error_code, field=field
        )
        assert builder.user_message() == expected_user_message


class TestFossilTimelineErrorBuilder:
    """Tests for the FossilTimelineErrorBuilder."""

    @pytest.mark.parametrize(
        'error_context, error_code, arg, expected_message',
        [
            (   # Test case for VALUE_ERROR during parsing
                moec.ModelErrorPath.FOSSIL_TIMELINE_PARSE,
                ec.GenericError.VALUE_ERROR,
                'bad data',
                (
                    'Error in `quarryforge.model.FossilTimeline.parse` '
                    '(Code: VALUE_ERROR). Failed to parse timeline data '
                    "from 'bad data'. Reason: unknown."
                ),
            ),
            (   # Test case for NO_COMMITS_DATA
                moec.ModelErrorPath.FOSSIL_TIMELINE_NO_COMMITS,
                ec.GenericError.INVALID_STATE_ERROR,
                'empty output',
                (
                    'Error in '
                    '`quarryforge.model.FossilTimeline.no_commits_data` '
                    '(Code: INVALID_STATE_ERROR). No commit data found in '
                    "the timeline output for 'empty output'. The timeline "
                    'might be empty or in an unexpected format.'
                ),
            ),
            (
                moec.ModelErrorPath.FOSSIL_TIMELINE_INIT,
                ec.GenericError.TYPE_ERROR,
                123,
                (
                    'Error in `quarryforge.model.FossilTimeline.__init__` '
                    '(Code: TYPE_ERROR). Expected type: unknown. Got type int '
                    'with value 123 instead.'
                ),
            ),
        ],
    )
    def test_message_mcdc(
        self, error_context, error_code, arg, expected_message
    ):
        builder = moec.FossilTimelineErrorBuilder(
            error_context=error_context, error_code=error_code, arg=arg
        )
        assert builder.message() == expected_message

    @pytest.mark.parametrize(
        'error_context, error_code, expected_user_message',
        [
            (
                moec.ModelErrorPath.FOSSIL_TIMELINE_PARSE,
                ec.GenericError.VALUE_ERROR,
                'Could not use the timeline information provided.',
            ),
            (
                moec.ModelErrorPath.FOSSIL_TIMELINE_PARSE,
                ec.GenericError.INVALID_STATE_ERROR,
                'An operation attempted in an invalid application state.',
            ),
            (
                moec.ModelErrorPath.FOSSIL_TIMELINE_NO_COMMITS,
                ec.GenericError.INVALID_STATE_ERROR,
                'No commit history could be found for the repository.',
            ),
        ],
    )
    def test_user_message_mcdc(
        self, error_context, error_code, expected_user_message
    ):
        builder = moec.FossilTimelineErrorBuilder(
            error_context=error_context, error_code=error_code
        )
        assert builder.user_message() == expected_user_message
