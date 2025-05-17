"""Meta Exception Module


"""
from typing import Dict, Optional

from quarryforge.exception import base_exception


class ImmutableClassError(base_exception.MetaError, AttributeError):
    """Immutable Class Error


    """
    CODE = ''#get.ModelNames.FOSSIL_REPO.value + Message.Default.ERROR.value

    def __init__(self,
                 name: str,
                 obj: object,
                 message: Optional[str] = None,
                 code: Optional[str] = None,
                 details: Optional[Dict] = None,
                 user_message: Optional[str] = None):

        if message is None:
            ae = AttributeError(name, obj)
            message = str(ae)

        effective_code = code if code is not None else self.__class_.CODE

        super().__init__(
            message=message,
            code=effective_code,
            details=details,
            user_message=user_message
        )

        self.name = name
        self.obj = obj

        if self.details is None:
            self.details = {}
