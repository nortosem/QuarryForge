"""tests/test_config/test_model_exception_config.py"""
import pytest

from quarryforge.config.exception_conf import model_exception_config as moec
from quarryforge.config.exception_conf import base_exception_config as bec
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.config import model_config, root


class TestModelExceptionConfigModule:
    """Tests for module-level constants in model_exception_config."""

    def test_module_dunder_all(self):
        expected = ['FossilRepoErrorBuilder', 'FossilCommitErrorBuilder', 'FossilTimelineErrorBuilder']
        assert sorted(moec.__all__) == sorted(expected)

    def test_model_error_path_attributes(self):
        """Test ModelErrorPath attributes for correct path construction."""
        base_path = f'{root.PACKAGE.name}.{root.MODULE.model}'
        assert moec.ModelErrorPath.FOSSIL_COMMIT == (
            f'{base_path}.{root.MODEL.fossil_commit}'
        )
        assert moec.ModelErrorPath.FOSSIL_REPO == (
            f'{base_path}.{root.MODEL.fossil_repo}'
        )
        assert moec.ModelErrorPath.FOSSIL_TIMELINE == (
            f'{base_path}.{root.MODEL.fossil_timeline}'
        )
    def test_fossil_repo_path_attributes(self):
        assert moec.FossilRepoPath.INIT == (
            f'{moec.ModelErrorPath.FOSSIL_REPO}.__init__'
        )
    def test_fossil_commit_path_attributes(self):
        assert moec.FossilCommitPath.INIT == (
            f'{moec.ModelErrorPath.FOSSIL_COMMIT}.__init__'
        )
        assert moec.FossilCommitPath.PARSE == (
            f'{moec.ModelErrorPath.FOSSIL_COMMIT}.parse'
        )
        assert moec.FossilCommitPath.VALIDATION == (
            f'{moec.ModelErrorPath.FOSSIL_COMMIT}.validation'
        )
    def test_fossil_timeline_path_attributes(self):
        assert moec.FossilTimelinePath.INIT == (
            f'{moec.ModelErrorPath.FOSSIL_TIMELINE}.__init__'
        )
        assert moec.FossilTimelinePath.PARSE == (
            f'{moec.ModelErrorPath.FOSSIL_TIMELINE}.parse'
        )
        assert moec.FossilTimelinePath.NO_COMMITS_DATA == (
            f'{moec.ModelErrorPath.FOSSIL_TIMELINE}.no_commits_data'
        )


class TestFossilRepoErrorBuilder:
    """Tests for the FossilRepoErrorBuilder."""

    def test_inheritance(self):
        assert issubclass(moec.FossilRepoErrorBuilder, bec.BaseErrorBuilder)

    @pytest.mark.parametrize(
        'error_code, arg, info, expected_message',
        [
            (
                ec.STRING_ERROR.empty,
                '',
                'a non-empty string',
                (
                    'Error in `quarryforge.model.FossilRepo.__init__` '
                    '(Code: EMPTY_STRING_ERROR). String argument is empty or '
                    'only whitespace. Expected: a non-empty string.'
                )
            ),
            (
                ec.PATH_ERROR.nonexistent,
                '/fake/path',
                None,
                (
                    'Error in `quarryforge.model.FossilRepo.__init__` '
                    '(Code: PATH_NONEXISTENT_ERROR). Path \'/fake/path\' is '
                    'expected to exist, but does not.'
                )
            ),
            (
                ec.PATH_ERROR.existing,
                '/real/path',
                None,
                (
                    'Error in `quarryforge.model.FossilRepo.__init__` '
                    '(Code: PATH_EXISTING_ERROR). Path \'/real/path\' is '
                    'expected not to exist (for creation), but already does.'
                )
            ),
            (
                ec.PATH_ERROR.file_error,
                '/path/is/dir',
                None,
                (
                    'Error in `quarryforge.model.FossilRepo.__init__` '
                    '(Code: PATH_NOT_A_FILE_ERROR). Path \'/path/is/dir\' is '
                    'expected to be a file, but it is a directory.'
                )
            ),
            (
                ec.PATH_ERROR.dir_error,
                '/path/is/file',
                None,
                (
                    'Error in `quarryforge.model.FossilRepo.__init__` '
                    '(Code: PATH_NOT_A_DIRECTORY_ERROR). Path '
                    '\'/path/is/file\' is expected to be a directory, but it '
                    'is a file.'
                )
            ),
            (
                ec.PATH_ERROR.same_dir,
                '/same/path',
                None,
                (
                    'Error in `quarryforge.model.FossilRepo.__init__` '
                    '(Code: SAME_REPO_DIR_AND_WORK_DIR). Fossil repository'
                    ' directory matches the working directory.'
                )
            ),
            # Fallback to base builder
            (
                ec.GENERIC_ERROR.value_error,
                'bad_value',
                'good_value',
                (
                    'Error in `quarryforge.model.FossilRepo.__init__` '
                    '(Code: VALUE_ERROR). Value \'bad_value\' is invalid. '
                    'Expected value: good_value.'
                )
            ),
        ]
    )
    def test_message_mcdc(
        self,
        error_code,
        arg,
        info,
        expected_message
    ):
        builder = moec.FossilRepoErrorBuilder(
            error_context=moec.FossilRepoPath.INIT, error_code=error_code,
            arg=arg, info=info,
        )
        assert builder.message() == expected_message


    @pytest.mark.parametrize(
        'error_code, expected_user_message',
        [
            (
                ec.PATH_ERROR.nonexistent,
                'A required file or directory was not found.'
            ),
            (
                ec.PATH_ERROR.same_dir,
                (
                    'The fossil repository parent directory is the '
                    'same directory as the workdir.'
                )
            ),
            (
                ec.STRING_ERROR.empty,
                'A required text input was left empty.'
            ),
            (
                ec.GENERIC_ERROR.configuration_error,
                'There is an issue with the configuration.'
            ), # Fallback
        ]
    )
    def test_user_message_mcdc(
            self,
            error_code,
            expected_user_message
    ):
        builder = moec.FossilRepoErrorBuilder(error_context='ctx', error_code=error_code)
        assert builder.user_message() == expected_user_message


class TestFossilCommitErrorBuilder:
    """Tests for the FossilCommitErrorBuilder."""

    @pytest.mark.parametrize(
        'error_context, error_code, field, arg, info, expected_message',
        [
            (
                moec.FossilCommitPath.VALIDATION,
                ec.STRING_ERROR.invalid_chars,
                model_config.FOSSIL_COMMIT.uuid,
                'bad-uuid',
                'a valid string (e.g., 40-char SHA-3 hex)',
                (
                    'Error in `quarryforge.model.FossilCommit.validation` '
                    '(Code: INVALID_CHARS_ERROR). Commit UUID \'bad-uuid\' is '
                    'not a valid format. Expected: a valid string '
                    '(e.g., 40-char SHA-3 hex).'
                ),
            ),
            (
                moec.FossilCommitPath.PARSE,
                ec.GENERIC_ERROR.type_error,
                None,
                'bad data',
                'a valid string',
                (
                    'Error in `quarryforge.model.FossilCommit.parse` '
                    '(Code: TYPE_ERROR). Failed to parse commit data from '
                    '\'bad data\'. Reason: unknown.'
                ),
            ),
            (
                moec.FossilCommitPath.VALIDATION,
                ec.GENERIC_ERROR.invalid_state,
                'author',
                'some commit',
                None,
                (
                    'Error in `quarryforge.model.FossilCommit.validation` '
                    '(Code: INVALID_STATE_ERROR). Required field '
                    '"author" is missing or empty in commit data for '
                    '\'some commit\'.'
                )
             ),
            # Fallback
            (
                moec.FossilCommitPath.INIT,
                ec.GENERIC_ERROR.type_error,
                None,
                123,
                'a valid string',
                (
                    'Error in `quarryforge.model.FossilCommit.__init__` '
                    '(Code: TYPE_ERROR). Expected type: a valid string. Got '
                    'type int with value 123 instead.'
                )
            ),
        ]
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
            error_context=error_context, error_code=error_code,
            field=field, arg=arg, info='a valid string' # for uuid test
        )
        assert builder.message() == expected_message

    @pytest.mark.parametrize(
        'error_context, error_code, field, expected_user_message',
        [
            (
                moec.FossilCommitPath.VALIDATION,
                ec.STRING_ERROR.invalid_chars,
                model_config.FOSSIL_COMMIT.uuid,
                'The commit identifier (UUID) is in an invalid format.'
            ),
            (
                moec.FossilCommitPath.PARSE,
                ec.GENERIC_ERROR.value_error,
                None,
                'Could not understand the commit information provided.'
            ),
            (
                moec.FossilCommitPath.VALIDATION,
                ec.GENERIC_ERROR.invalid_state,
                'comment',
                'A required piece of commit information (comment) was missing.'
            ),
            (
                moec.FossilCommitPath.INIT,
                ec.GENERIC_ERROR.not_implemented_error,
                None,
                'This feature is not available.'
            ), # Fallback
        ]
    )
    def test_user_message_mcdc(
            self,
        error_context,
        error_code,
        field,
        expected_user_message
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
            (
                moec.FossilTimelinePath.PARSE,
                ec.GENERIC_ERROR.value_error,
                'bad data',
                (
                    'Error in `quarryforge.model.FossilTimeline.parse` '
                     '(Code: VALUE_ERROR). Failed to parse timeline data '
                     'from \'bad data\'. Reason: unknown.'
                )
            ),
            (
                moec.FossilTimelinePath.NO_COMMITS_DATA,
                ec.GENERIC_ERROR.invalid_state,
                'empty output',
                (
                    'Error in '
                    '`quarryforge.model.FossilTimeline.no_commits_data` '
                    '(Code: INVALID_STATE_ERROR). No commit data found in '
                    'the timeline output for \'empty output\'. The timeline '
                    'might be empty or in an unexpected format.'
                )
            ),
            # Fallback
            (
                moec.FossilTimelinePath.INIT,
                ec.GENERIC_ERROR.type_error,
                123,
                (
                    'Error in `quarryforge.model.FossilTimeline.__init__` '
                    '(Code: TYPE_ERROR). Expected type: unknown. Got type int '
                     'with value 123 instead.'
                )
            ),
        ]
    )
    def test_message_mcdc(
            self,
            error_context,
            error_code,
            arg,
            expected_message
    ):
        builder = moec.FossilTimelineErrorBuilder(
            error_context=error_context, error_code=error_code, arg=arg
        )
        assert builder.message() == expected_message


    @pytest.mark.parametrize(
        'error_context, error_code, expected_user_message',
        [
            (
                moec.FossilTimelinePath.PARSE,
                ec.GENERIC_ERROR.value_error,
                'Could not use the timeline information provided.'
            ),
            (
                moec.FossilTimelinePath.NO_COMMITS_DATA,
                ec.GENERIC_ERROR.invalid_state,
                'No commit history could be found for the repository.'
            ),
            (
                moec.FossilTimelinePath.INIT,
                ec.GENERIC_ERROR.not_implemented_error,
                'This feature is not available.'
            ), # Fallback
        ]
    )
    def test_user_message_mcdc(
            self,
            error_context,
            error_code,
            expected_user_message
    ):
        builder = moec.FossilTimelineErrorBuilder(
            error_context=error_context, error_code=error_code
        )
        assert builder.user_message() == expected_user_message
