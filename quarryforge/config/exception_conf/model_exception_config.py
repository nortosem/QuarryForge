"""Model Exception Configuration

Configures and provides builders for FossilRepo, FossilCommit, & Fossil
Timeline exceptions.
"""
from enum import StrEnum
from typing import List

from quarryforge.config import model_config
from quarryforge.config import root
from quarryforge.config.exception_conf import base_exception_config as base_config
from quarryforge.config.exception_conf import exception_config as config


__all__: List[str] = [
    'FossilRepoErrorBuilder',
    'FossilCommitErrorBuilder',
    'FossilTimelineErrorBuilder',
]


class ModelErrorPath(StrEnum):
    """Create Path strings for the Model module expcetions.

    These represent the path context for differnt module error types.

    Attributes:
        _FOSSIL_COMMIT: Full base path for a FossilCommit exception code.
        _FOSSIL_REPO: Full base path for a FossilRepo exception code.
        _FOSSIL_TIMELINE: Full base path for FossilTimeline exception code.
        INIT: Full model error path with `__init__` context.
        PARSE: Context for errors during commit data parsing.
        INIT: Full model error path with `__init__` context.
        PARSE: Context for errors during timeline data parsing.
        NO_COMMITS_DATA: Context when timeline parsing yields no commit data.
    """
    # path roots
    _FOSSIL_COMMIT_ROOT = base_config.get_full_error_code(
        base_config.BaseErrorPath.MODEL, root.Model.FOSSIL_COMMIT
    )
    _FOSSIL_REPO_ROOT = base_config.get_full_error_code(
        base_config.BaseErrorPath.MODEL, root.Model.FOSSIL_REPO
    )
    _FOSSIL_TIMELINE_ROOT = base_config.get_full_error_code(
        base_config.BaseErrorPath.MODEL, root.Model.FOSSIL_TIMELINE
    )
    # FossilRepo Path
    FOSSIL_REPO_INIT = f'{_FOSSIL_REPO_ROOT}.__init__'

    # FossilCommit Path
    FOSSIL_COMMIT_INIT = f'{_FOSSIL_COMMIT_ROOT}.__init__'
    FOSSIL_COMMIT_PARSE = f'{_FOSSIL_COMMIT_ROOT}.parse'

    # FossilTimeline Path
    FOSSIL_TIMELINE_INIT = f'{_FOSSIL_TIMELINE_ROOT}.__init__'
    FOSSIL_TIMELINE_PARSE = f'{_FOSSIL_TIMELINE_ROOT}.parse'
    FOSSIL_TIMELINE_NO_COMMITS = f'{_FOSSIL_TIMELINE_ROOT}.no_commits_data'


class FossilRepoErrorBuilder(base_config.BaseErrorBuilder):
    """Builder for constructing error data specific to FossilRepo operations.

    This builder extends BaseErrorBuilder to provide detailed and user-friendly
    messages for FossilRepo-related exceptions, including path-specific and
    string-specific validations.
    """
    def _string_error_message(self) -> str:
        """Generates a message for string errors specific to FossilRepo."""
        base_msg = self._base_message()
        match self.error_code:
            case config.StringError.EMPTY_STRING_ERROR:
                return (
                    f'{base_msg} String argument is empty or only whitespace. '
                    'Expected: '
                    f'{self.info or config.DescMsg.A_NON_EMPTY_STRING}.'
                )
            case config.StringError.INVALID_CHARS_ERROR:
                return (
                    f'{base_msg} String {self.arg!r} contains invalid '
                    f'characters or patterns. '
                    f'Expected pattern: {self.info or config.DescMsg.UNKNOWN}.'
                )
            case _:
                return (
                    f'{base_msg} An unexpected string validation error '
                    f'occurred for {self.arg!r}.'
                )

    def _path_error_message(self) -> str:
        """Generates a message for errors with FossilRepo file paths."""
        base_msg = self._base_message()
        path_info = self.info or config.DescMsg.A_VALID_PATH
        details = self.extra_details or {}
        reason: str = details.get(
            config.DescMsg.REASON, config.DescMsg.UNKNOWN
        )

        match self.error_code:
            case config.PathError.NON_PATH_OBJECT_ERROR:
                return (
                    f'{base_msg} Argument {self.arg!r} is not {path_info} or '
                    f' convertible to one.'
                )
            case config.PathError.INVALID_PATH_STRING_ERROR:
                return (
                    f'{base_msg} The provided string {self.arg!r} cannot be '
                    f' interpreted as a valid system path.'
                )
            case config.PathError.PATH_RESOLUTION_ERROR:
                return (
                    f'{base_msg} Path resolution failed for {self.arg!r}. '
                    f' Reason: {reason}.'
                )
            case config.PathError.PATH_NONEXISTENT_ERROR:
                return (
                    f'{base_msg} Path {self.arg!r} is expected to exist, '
                    f'but does not.'
                )
            case config.PathError.PATH_EXISTING_ERROR:
                return (
                    f'{base_msg} Path {self.arg!r} is expected not to exist '
                    f'(for creation), but already does.'
                )
            case config.PathError.PATH_NOT_A_FILE_ERROR:
                return (
                    f'{base_msg} Path {self.arg!r} is expected to be a file,'
                    f' but it is a directory.'
                )
            case config.PathError.PATH_NOT_A_DIRECTORY_ERROR:
                return (
                    f'{base_msg} Path {self.arg!r} is expected to be a'
                    ' directory, but it is a file.'
                )
            case config.PathError.PATH_NOT_READABLE_ERROR:
                return (
                    f'{base_msg} Path {self.arg!r} lacks read permissions.'
                )
            case config.PathError.PATH_NOT_WRITABLE_ERROR:
                return (
                    f'{base_msg} Path {self.arg!r} lacks write permissions.'
                )
            case config.PathError.PATH_NOT_EXECUTABLE_ERROR:
                return (
                    f'{base_msg} Path {self.arg!r} lacks execute permissions.'
                )
            case config.PathError.SAME_REPO_DIR_AND_WORK_DIR:
                return (
                    f'{base_msg} Fossil repository directory matches the '
                    f'working directory.'
                )

            case _:
                return (
                    f'{base_msg} An unhandled path error for {self.arg!r}. '
                    f'Details: {self.info or config.DescMsg.UNKNOWN}.'
                )


    def message(self) -> str:
        """Builds a detailed, technical error message for FossilRepo exceptions.

        Overrides BaseErrorBuilder's message to provide specific details for
        string and path related errors common in FossilRepo, then falls back
        to generic messages.
        """
        match self.error_code:
            case (
                config.StringError.EMPTY_STRING_ERROR |
                config.StringError.INVALID_CHARS_ERROR
            ):
                return self._string_error_message()

            case (
                config.PathError.NON_PATH_OBJECT_ERROR |
                config.PathError.INVALID_PATH_STRING_ERROR |
                config.PathError.PATH_RESOLUTION_ERROR |
                config.PathError.PATH_EXISTING_ERROR |
                config.PathError.PATH_NONEXISTENT_ERROR |
                config.PathError.PATH_NOT_A_FILE_ERROR |
                config.PathError.PATH_NOT_A_DIRECTORY_ERROR |
                config.PathError.PATH_NOT_READABLE_ERROR |
                config.PathError.PATH_NOT_WRITABLE_ERROR |
                config.PathError.PATH_NOT_EXECUTABLE_ERROR |
                config.PathError.SAME_REPO_DIR_AND_WORK_DIR
            ):
                return self._path_error_message()

            case _:
                return super().message()

    def user_message(self) -> str:
        """Builds a user-friendly error message for FossilRepo exceptions.

        Overrides the base implementation to provide more specific user messages
        where applicable, then falls back to generic messages.
        """
        match self.error_code:
            case config.StringError.EMPTY_STRING_ERROR:
                return 'A required text input was left empty.'
            case config.StringError.INVALID_CHARS_ERROR:
                return (
                    'A text input contains unsupported characters '
                    'or is not in the expected format.'
                    )
            case config.PathError.NON_PATH_OBJECT_ERROR:
                return 'The file path is in an incorrect format or type.'
            case config.PathError.INVALID_PATH_STRING_ERROR:
                return 'The provided path string is not a valid file path.'
            case config.PathError.PATH_RESOLUTION_ERROR:
                return 'The path provided could not be resolved.'
            case config.PathError.PATH_NONEXISTENT_ERROR:
                return 'A required file or directory was not found.'
            case config.PathError.PATH_EXISTING_ERROR:
                return 'A file or directory that should be new already exists.'
            case config.PathError.PATH_NOT_A_FILE_ERROR:
                return (
                    'Expected a file at the path, but found a directory or '
                    ' something else.'
                )
            case config.PathError.PATH_NOT_A_DIRECTORY_ERROR:
                return (
                    'Expected a directory at the path, but found a file or '
                    'something else.'
                )
            case config.PathError.PATH_NOT_READABLE_ERROR:
                return (
                    'Permission denied: Cannot read from the specified '
                    'file or directory.'
                )
            case config.PathError.PATH_NOT_WRITABLE_ERROR:
                return (
                    'Permission denied: Cannot write to the specified '
                    'file or directory.'
                )
            case config.PathError.PATH_NOT_EXECUTABLE_ERROR:
                return 'Permission denied: Cannot execute the specified file.'
            case config.PathError.SAME_REPO_DIR_AND_WORK_DIR:
                return (
                    'The fossil repository parent directory is the same '
                    'directory as the workdir.'
                )
            case _:
                return super().user_message()


class FossilCommitErrorBuilder(base_config.BaseErrorBuilder):
    """Builder for constructing error data specific to FossilCommit operations.

    This builder extends BaseErrorBuilder to provide detailed and user-friendly
    messages for FossilCommit-related exceptions.
    """
    def _invalid_uuid_message(self) -> str:
        """Generates a message for invalid UUID format errors."""
        base_msg = self._base_message()
        info = self.info or config.DescMsg.A_VALID_STRING
        return (
            f'{base_msg} Commit UUID {self.arg!r} is not a valid format. '
            f'Expected: {info} (e.g., 40-char SHA-3 hex).'
        )

    def _parse_error_message(self) -> str:
        """Generates a message for commit data parsing errors."""
        base_msg = self._base_message()
        details = self.extra_details or {}
        reason: str = details.get(
            config.DescMsg.REASON, config.DescMsg.UNKNOWN
        )
        return (
            f'{base_msg} Failed to parse commit data from {self.arg!r}. '
            f'Reason: {reason}.'
        )

    def _missing_field_message(self) -> str:
        """Generates a message for missing required fields in commit data."""
        base_msg = self._base_message()
        return (
            f'{base_msg} Required field "{self.field}" is missing or empty '
            f'in commit data for {self.arg!r}.'
        )

    def message(self) -> str:
        """Builds a detailed, technical message for FossilCommit exceptions."""
        match self.error_code:
            case config.StringError.INVALID_CHARS_ERROR if (
                self.field == model_config.fossil_commit_config().uuid
            ):
                return self._invalid_uuid_message()
            case config.GenericError.VALUE_ERROR if (
                self.error_context == ModelErrorPath.FOSSIL_COMMIT_PARSE
            ):
                return self._parse_error_message()
            case config.GenericError.TYPE_ERROR if (
                self.error_context == ModelErrorPath.FOSSIL_COMMIT_PARSE
            ):
                return self._parse_error_message()
            case config.GenericError.INVALID_STATE_ERROR if self.field:
                return self._missing_field_message()
            case _:
                return super().message()

    def user_message(self) -> str:
        """Builds a user-friendly error message for FossilCommit exceptions."""
        match self.error_code:
            case config.StringError.INVALID_CHARS_ERROR if (
                self.field == model_config.fossil_commit_config().uuid
            ):
                return 'The commit identifier (UUID) is in an invalid format.'
            case config.GenericError.VALUE_ERROR if (
                self.error_context == ModelErrorPath.FOSSIL_COMMIT_PARSE
            ):
                return 'Could not understand the commit information provided.'
            case config.GenericError.TYPE_ERROR if (
                self.error_context == ModelErrorPath.FOSSIL_COMMIT_PARSE
            ):
                return 'Commit information is in an unexpected format.'
            case config.GenericError.INVALID_STATE_ERROR if self.field:
                return (
                    f'A required piece of commit information ({self.field}) '
                    f'was missing.'
                )
            case _:
                return super().user_message()


class FossilTimelineErrorBuilder(base_config.BaseErrorBuilder):
    """Builder for error data specific to FossilTimeline operations.

    This builder extends BaseErrorBuilder to provide detailed and user-friendly
    messages for FossilTimeline-related exceptions.
    """
    def _parse_error_message(self) -> str:
        """Generates a message for timeline data parsing errors."""
        base_msg = self._base_message()
        details = self.extra_details or {}
        reason: str = details.get(
            config.DescMsg.REASON, config.DescMsg.UNKNOWN
        )
        return (
            f'{base_msg} Failed to parse timeline data from {self.arg!r}. '
            f'Reason: {reason}.'
        )

    def _no_commits_data_message(self) -> str:
        """Generates a message when no commit data is found in timeline."""
        base_msg = self._base_message()
        return (
            f'{base_msg} No commit data found in the timeline output for '
            f'{self.arg!r}. '
            f'The timeline might be empty or in an unexpected format.'
        )

    def message(self) -> str:
        """Builds detailed, technical message for FossilTimeline exceptions."""
        match self.error_code:
            case config.GenericError.VALUE_ERROR if (
                self.error_context == ModelErrorPath.FOSSIL_TIMELINE_PARSE
            ):
                return self._parse_error_message()
            case config.GenericError.TYPE_ERROR if (
                self.error_context == ModelErrorPath.FOSSIL_TIMELINE_PARSE
            ):
                return self._parse_error_message()
            case config.GenericError.INVALID_STATE_ERROR if (
                self.error_context == ModelErrorPath.FOSSIL_TIMELINE_NO_COMMITS
            ):
                return self._no_commits_data_message()
            case _:
                return super().message()

    def user_message(self) -> str:
        """Builds a user-friendly message for FossilTimeline exceptions."""
        match self.error_code:
            case config.GenericError.VALUE_ERROR if (
                self.error_context == ModelErrorPath.FOSSIL_TIMELINE_PARSE
            ):
                return 'Could not use the timeline information provided.'
            case config.GenericError.TYPE_ERROR if (
                self.error_context == ModelErrorPath.FOSSIL_TIMELINE_PARSE
            ):
                return 'Timeline information is in an unexpected format.'
            case config.GenericError.INVALID_STATE_ERROR if (
                self.error_context == ModelErrorPath.FOSSIL_TIMELINE_NO_COMMITS
            ):
                return 'No commit history could be found for the repository.'
            case _:
                return super().user_message()
