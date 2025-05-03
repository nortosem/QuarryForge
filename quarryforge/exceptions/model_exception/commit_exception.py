"""Commit Exception Module


"""
from quarryforge.config.exception_conf.models_exception \
    import commit_error_conf
from quarryforge.exceptions.model_exception.base_models_exception \
    import CommitError


class UuidTypeError(CommitError, TypeError):
    """Raise for invalid uuid/hash type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.invalid_commit_hash())


class UuidValueError(CommitError, ValueError):
    """Commit uuid/hash cannot be empty"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.empty_commit_hash())


class DateTypeError(CommitError, TypeError):
    """Raise for invalid date type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.invalid_commit_date())


class DateValueError(CommitError, ValueError):
    """Raise for empty date type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.empty_commit_date())


class AuthorTypeError(CommitError, TypeError):
    """Raise for invalid author type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.invalid_commit_author())


class AuthorValueError(CommitError, ValueError):
    """Raise for empty author type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.empty_commit_author())


class CommentTypeError(CommitError, TypeError):
    """Raise for invalid comment type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.invalid_commit_comment())


class CommentValueError(CommitError, ValueError):
    """Raise for empty comment type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.empty_commit_comment())


class BranchTypeError(CommitError, TypeError):
    """Raise for invalid branch type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.invalid_commit_branch())

class BranchValueError(CommitError, ValueError):
    """Raise for empty branch type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.empty_commit_branch())

class TagsCommitError(CommitError):
    """General Commit Tages exception"""
    pass


class TagsListError(TagsCommitError, TypeError):
    """Raise for invalid tags argument type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.invalid_commit_tags())


class TagTypeError(TagsCommitError, TypeError):
    """Raise for invalid tag type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.invalid_commit_tag_type())


class TagValueError(TagsCommitError, ValueError):
    """Raise for invalid version type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.empty_commit_tags())

class PhaseTypeError(CommitError, TypeError):
    """Raise for invalid version type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.invalid_info_version())

class PhaseValueError(CommitError, ValueError):
    """Raise for invalid version type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.invalid_info_version())


class ChangesCommitError(CommitError):
    pass


class ChangesTypeError(CommitError, TypeError):
    """Raise for invalid version type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.invalid_info_version())


class ChangeTypeError(ChangesCommitError, TypeError):
    """Raise for invalid version type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.invalid_info_version())


class ChangeValueError(ChangesCommitError, ValueError):
    """Raise for invalid version type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.invalid_info_version())


class ImmutableCommitError(CommitError, TypeError):
    """Raise for invalid version type"""
    def __init__(self, message=None):
        super().__init__(
            message or commit_error_conf.invalid_info_version())
