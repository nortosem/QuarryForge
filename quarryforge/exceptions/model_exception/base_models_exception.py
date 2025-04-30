"""Model Exceptions

#TODO
"""
from quarryforge.exceptions.base_exception import QuarryForgeException


class ModelError(QuarryForgeException):
    """Models Error

    Base exception class for all exceptions in the models module.
    """
    pass


class RepoConfigError(ModelException):
    """RepoConfig Error

    Base exception for the RepoConfig class.
    """
    def __init__(self, message=None):
        super().__init__(message)


class TimelineError(ModelsException):
    """Timeline Parsing Error

    Raised when there is an error parsing the output of the `fossil timeline`
    command.  This might occur if the output format is unexpected or if
    there are issues extracting data from the timeline text.
    """
    def __init__(self, message: str = "Error parsing fossil timeline output"):
        super().__init__(message)
