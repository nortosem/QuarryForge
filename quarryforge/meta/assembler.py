"""Assembler Module


"""
from quarryforge.config.exception_conf import exception_data as error


class BuildError(ABC):
    """Build Error Abstract Base Class.


    """
    def __init__(self, error_module: str, error_config: Any = None):
        self.error_module = error_module
        self.error_config = error_config


    @abstractmethod
    def config(self, conf: Optional[root.Config] = None) -> None:
        """Get the configuration dictionary for a specific module
        component.
        """
        ...


    @abstractmethod
    def code(self, : context: Optional[root.Config], field: str) -> str:
        """Generate a Module level unique code for the field context."""
        ...


    @abstractmethod
    def message(self, context: Optional[root.Config], field: str) -> str:
        """Generate and return message in context of the module used."""
        ...

    @abstractmethod
    def user_message(self, context: Optional[root.Config], field: str) -> str:
        """Generarte and return a user_message in context of the module used.
        """
        ...

    @abstractmethod
    def details(self, conf: Optional[root.Config], field: str) -> List[str]:
        """"""
        ...


    def data(
        self,
        context: str,
        field: str,
        error_type: str,
        message: str = None,
        user_message: str = None,
        input_value: Any = None,
        expected_desc: Optional[str] = None,
        extra_details: Optional[Dict[str, Any]] = None
    ) -> ValidErrorData:
        """Create a valid error data object."""
        code = ()

        details = {
            error.BUILDER_FIELD.context: context,
            error.BUILDER_FIELD.field: field,
            error.BUILDER_FIELD.error_type: error_type,
            error.BUILDER_FIELD.message: message,
            error.BUILDER_FIELD.input_value: input_value
        }
        if expected_input:
            details[error.BUILDER_FIELD.expected_desc] = expected_desc

        if extra_details:
            details[error.BUILDER_FIELD.extra_details] = extra_details

        return error.ValidErrorData(
            code=code
            message=message
            user_message=user_message
            details=details
        )
