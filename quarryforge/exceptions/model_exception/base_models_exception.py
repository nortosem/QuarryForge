"""Model Exceptions

#TODO
"""
from quarryforge.exceptions.base_exception import QuarryForgeException


class ModelError(QuarryForgeException):
    """Models Error

    Base exception class for all exceptions in the models module.
    """
    pass


class RepoConfigError(ModelError):
    """RepoConfig Error

    Base exception for the RepoConfig class.
    """
    pass


class InfoArgsError(ModelError):
    """InfoArgs Error

    Base exception for the InfoArgs class.
    """
    pass


class DiffArgsError(ModelError):
    """DiffArgs Error

    Base exception for the DiffArgs class.
    """
    pass


class CatArgsError(ModelError):
    """CatArgs Error

    Base exception for the CatArgs class.
    """
    pass


class GetTimelineError(ModelError):
    """GetTimeline Error

    Base exception for the GetTimelineArg class.
    """
    pass


class CommitError(ModelError):
    """Commit Error

    Base exception for the Commit class.
    """
    pass


class TimelineError(ModelError):
    """Timeline Parsing Error

    Raised when there is an error parsing the output of the `fossil timeline`
    command.  This might occur if the output format is unexpected or if
    there are issues extracting data from the timeline text.
    """
    pass
