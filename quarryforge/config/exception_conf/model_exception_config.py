"""Model Exception Configuration

Configures and provides builders for FossilRepo, FossilCommit, & Fossil
Timeline exceptions.
"""
from typing import List

from quarryforge.config import model_config
from quarryforge.config import root
from quarryforge.config.exception_conf import base_exception_config as base_config
from quarryforge.config.exception_conf import exception_config as config
from quarryforge.meta import immutable


__all__: List[str] = [
    'FossilRepoErrorBuilder',
    'FossilCommitErrorBuilder',
    'FossilTimelineErrorBuilder',
]


class ModelErrorPath(metaclass=immutable.Namespace):
    """Create Path strings for the Model module expcetions.

    These represent the path context for differnt module error types.

    Attributes:
        FOSSIL_COMMIT: Full base path for a FossilCommit exception code.
        FOSSIL_REPO: Full base path for a FossilRepo exception code.
        FOSSIL_TIMELINE: Full base path for FossilTimeline exception code.
    """
    FOSSIL_COMMIT: str = base_config.BaseErrorPath.get_full_error_code(
        base_config.BaseErrorPath.MODEL, root.MODEL.fossil_commit
    )
    FOSSIL_REPO: str = base_config.BaseErrorPath.get_full_error_code(
        base_config.BaseErrorPath.MODEL, root.MODEL.fossil_repo
    )
    FOSSIL_TIMELINE: str = base_config.BaseErrorPath.get_full_error_code(
        base_config.BaseErrorPath.MODEL, root.MODEL.fossil_timeline
    )


class FossilRepoPath(metaclass=immutable.Namespace):
    """Create the path context for a FossilRepo exception.

    These are the `error_context` values.

    Attributes:
        INIT: Full model error path with `__init__` context.
    """
    INIT: str = f'{ModelErrorPath.FOSSIL_REPO}.__init__'


class FossilCommitPath(metaclass=immutable.Namespace):
    """Create the path context for a FossilCommit exception.

    These are the `error_context` values.

    Attributes:
        INIT: Full model error path with `__init__` context.
        PARSE: Context for errors during commit data parsing.
        VALIDATION: Context for errors validating commit fields.
    """
    INIT: str = f'{ModelErrorPath.FOSSIL_COMMIT}.__init__'
    PARSE: str = f'{ModelErrorPath.FOSSIL_COMMIT}.parse'
    VALIDATION: str = f'{ModelErrorPath.FOSSIL_COMMIT}.validation'


class FossilTimelinePath(metaclass=immutable.Namespace):
    """Create the path context for a FossilTimeline exception.

    These are the `error_context` values.

    Attributes:
        INIT: Full model error path with `__init__` context.
        PARSE: Context for errors during timeline data parsing.
        NO_COMMITS_DATA: Context when timeline parsing yields no commit data.
    """
    INIT: str = f'{ModelErrorPath.FOSSIL_TIMELINE}.__init__'
    PARSE: str = f'{ModelErrorPath.FOSSIL_TIMELINE}.parse'
    NO_COMMITS_DATA: str = f'{ModelErrorPath.FOSSIL_TIMELINE}.no_commits_data'


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
            case config.STRING_ERROR.empty:
                return (
                    f'{base_msg} String argument is empty or only whitespace. '
                    f'Expected: {self.info or config.DESC_MSG.unempty}.'
                )
            case config.STRING_ERROR.invalid_chars:
                return (
                    f'{base_msg} String "{self.arg!r}" contains invalid '
                    f'characters or patterns. '
                    f'Expected pattern: {self.info or config.DESC_MSG.unknown}.'
                )
            case _:
                return (
                    f'{base_msg} An unexpected string validation error '
                    f'occurred for "{self.arg!r}".'
                )

    def _path_error_message(self) -> str:
        """Generates a message for errors with FossilRepo file paths."""
        base_msg = self._base_message()
        path_info = self.info or config.DESC_MSG.path

        match self.error_code:
            case config.PATH_ERROR.non_path_object:
                return (
                    f'{base_msg} Argument {self.arg!r} is not {path_info} or '
                    f' convertible to one.'
                )
            case config.PATH_ERROR.invalid_path_string:
                return (
                    f'{base_msg} The provided string "{self.arg!r}" cannot be '
                    f' interpreted as a valid system path.'
                )
            case config.PATH_ERROR.resolution:
                reason = config.DESC_MSG.unknown
                if self.extra_details:
                    reason = str(self.extra_details.get(
                        config.DESC_MSG.reason)
                    )
                return (
                    f'{base_msg} Path resolution failed for "{self.arg!r}". '
                    f' Reason: {reason}.'
                )
            case config.PATH_ERROR.nonexistent:
                return (
                    f'{base_msg} Path "{self.arg!r}" is expected to exist, '
                    f'but does not.'
                )
            case config.PATH_ERROR.existing:
                return (
                    f'{base_msg} Path "{self.arg!r}" is expected not to exist '
                    f'(for creation), but already does.'
                )
            case config.PATH_ERROR.file_error:
                return (
                    f'{base_msg} Path "{self.arg!r}" is expected to be a file,'
                    f' but it is a directory.'
                )
            case config.PATH_ERROR.dir_error:
                return (
                    f'{base_msg} Path "{self.arg!r}" is expected to be a '
                    f' directory, but it is a file.'
                )
            case config.PATH_ERROR.unreadable:
                return (
                    f'{base_msg} Path "{self.arg!r}" lacks read permissions.'
                )
            case config.PATH_ERROR.unwritable:
                return (
                    f'{base_msg} Path "{self.arg!r}" lacks write permissions.'
                )
            case config.PATH_ERROR.unexecutable:
                return (
                    f'{base_msg} Path "{self.arg!r}" lacks execute permissions.'
                )
            case _:
                return (
                    f'{base_msg} An unhandled path error for "{self.arg!r}". '
                    f'Details: {self.info or config.DESC_MSG.unknown}.'
                )


    def message(self) -> str:
        """Builds a detailed, technical error message for FossilRepo exceptions.

        Overrides BaseErrorBuilder's message to provide specific details for
        string and path related errors common in FossilRepo, then falls back
        to generic messages.
        """
        match self.error_code:
            case config.STRING_ERROR.empty | config.STRING_ERROR.invalid_chars:
                return self._string_error_message()

            case (
                config.PATH_ERROR.non_path_object |
                config.PATH_ERROR.invalid_path_string |
                config.PATH_ERROR.resolution |
                config.PATH_ERROR.existing |
                config.PATH_ERROR.nonexistent |
                config.PATH_ERROR.file_error |
                config.PATH_ERROR.dir_error |
                config.PATH_ERROR.unreadable |
                config.PATH_ERROR.unwritable |
                config.PATH_ERROR.unexecutable
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
            case config.STRING_ERROR.empty:
                return 'A required text input was left empty.'
            case config.STRING_ERROR.invalid_chars:
                return (
                    'A text input contains unsupported characters '
                    'or is not in the expected format.'
                    )
            case config.PATH_ERROR.non_path_object:
                return 'The file path is in an incorrect format or type.'
            case config.PATH_ERROR.invalid_path_string:
                return 'The provided path string is not a valid file path.'
            case config.PATH_ERROR.resolution:
                return 'The path provided could not be resolved.'
            case config.PATH_ERROR.nonexistent:
                return 'A required file or directory was not found.'
            case config.PATH_ERROR.existing:
                return 'A file or directory that should be new already exists.'
            case config.PATH_ERROR.file_error:
                return (
                    'Expected a file at the path, but found a directory or '
                    ' something else.'
                )
            case config.PATH_ERROR.dir_error:
                return (
                    'Expected a directory at the path, but found a file or '
                    'something else.'
                )
            case config.PATH_ERROR.unreadable:
                return (
                    'Permission denied: Cannot read from the specified '
                    'file or directory.'
                )
            case config.PATH_ERROR.unwritable:
                return (
                    'Permission denied: Cannot write to the specified '
                    'file or directory.'
                )
            case config.PATH_ERROR.unexecutable:
                return 'Permission denied: Cannot execute the specified file.'
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
        info = self.info or config.DESC_MSG.string
        return (
            f'{base_msg} Commit UUID "{self.arg!r}" is not a valid format. '
            f'Expected: {info} (e.g., 40-char SHA-3 hex).'
        )

    def _parse_error_message(self) -> str:
        """Generates a message for commit data parsing errors."""
        base_msg = self._base_message()
        reason = config.DESC_MSG.unknown
        if self.extra_details:
            reason = str(self.extra_details.get(
                config.DESC_MSG.reason)
            )
        return (
            f'{base_msg} Failed to parse commit data from "{self.arg!r}". '
            f'Reason: {reason}.'
        )

    def _missing_field_message(self) -> str:
        """Generates a message for missing required fields in commit data."""
        base_msg = self._base_message()
        return (
            f'{base_msg} Required field "{self.field}" is missing or empty '
            f'in commit data for "{self.arg!r}".'
        )

    def message(self) -> str:
        """Builds a detailed, technical message for FossilCommit exceptions."""
        match self.error_code:
            case config.STRING_ERROR.invalid_chars if (
                self.field == model_config.FOSSIL_COMMIT.uuid
            ):
                return self._invalid_uuid_message()
            case config.GENERIC_ERROR.value_error if (
                self.error_context == FossilCommitPath.PARSE
            ):
                return self._parse_error_message()
            case config.GENERIC_ERROR.type_error if (
                self.error_context == FossilCommitPath.PARSE
            ):
                return self._parse_error_message()
            case config.GENERIC_ERROR.invalid_state if self.field:
                return self._missing_field_message()
            case _:
                return super().message()

    def user_message(self) -> str:
        """Builds a user-friendly error message for FossilCommit exceptions."""
        match self.error_code:
            case config.STRING_ERROR.invalid_chars if (
                self.field == model_config.FOSSIL_COMMIT.uuid
            ):
                return 'The commit identifier (UUID) is in an invalid format.'
            case config.GENERIC_ERROR.value_error if (
                self.error_context == FossilCommitPath.PARSE
            ):
                return 'Could not understand the commit information provided.'
            case config.GENERIC_ERROR.type_error if (
                self.error_context == FossilCommitPath.PARSE
            ):
                return 'Commit information is in an unexpected format.'
            case config.GENERIC_ERROR.invalid_state if self.field:
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
        reason = config.DESC_MSG.unknown
        if self.extra_details:
            reason = str(self.extra_details.get(
                config.DESC_MSG.reason)
            )
        return (
            f'{base_msg} Failed to parse timeline data from "{self.arg!r}". '
            f'Reason: {reason}.'
        )

    def _no_commits_data_message(self) -> str:
        """Generates a message when no commit data is found in timeline."""
        base_msg = self._base_message()
        return (
            f'{base_msg} No commit data found in the timeline output for '
            f'"{self.arg!r}". '
            f'The timeline might be empty or in an unexpected format.'
        )

    def message(self) -> str:
        """Builds detailed, technical message for FossilTimeline exceptions."""
        match self.error_code:
            case config.GENERIC_ERROR.value_error if (
                self.error_context == FossilTimelinePath.PARSE
            ):
                return self._parse_error_message()
            case config.GENERIC_ERROR.type_error if (
                self.error_context == FossilTimelinePath.PARSE
            ):
                return self._parse_error_message()
            case config.GENERIC_ERROR.invalid_state if (
                self.error_context == FossilTimelinePath.NO_COMMITS_DATA
            ):
                return self._no_commits_data_message()
            case _:
                return super().message()

    def user_message(self) -> str:
        """Builds a user-friendly message for FossilTimeline exceptions."""
        match self.error_code:
            case config.GENERIC_ERROR.value_error if (
                self.error_context == FossilTimelinePath.PARSE
            ):
                return 'Could not use the timeline information provided.'
            case config.GENERIC_ERROR.type_error if (
                self.error_context == FossilTimelinePath.PARSE
            ):
                return 'Timeline information is in an unexpected format.'
            case config.GENERIC_ERROR.invalid_state if (
                self.error_context == FossilTimelinePath.NO_COMMITS_DATA
            ):
                return 'No commit history could be found for the repository.'
            case _:
                return super().user_message()
