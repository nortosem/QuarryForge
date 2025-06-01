"""Meta Exception Module"""
from typing import Any, Dict, Optional

from quarryforge.config.exception_conf.exception_data import BUILDER_FIELD
from quarryforge.exception import base_exception


class ImmutableError(base_exception.MetaError, AttributeError):
    """Error raised when an immutable class or instance modification occurs."""
    def __init__(self,
                 code: str,
                 message: str,
                 user_message: str,
                 details: Optional[Dict[str, Any]] = None):

        name: Optional[str] = None
        obj: Optional[Any] = None

        if details is not None:
            name = details.get(BUILDER_FIELD.field)
            obj = details.get(BUILDER_FIELD.arg)

        AttributeError.__init__(self, name=name, obj=obj)

        base_exception.MetaError.__init__(self,
            message=message,
            code=code,
            details=details,
            user_message=user_message
        )
