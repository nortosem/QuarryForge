"""Meta Exception Module."""

from typing import Any

from quarryforge.config.exception_conf.exception_data import builder_config
from quarryforge.exception import base_exception


class ImmutableError(base_exception.MetaError, AttributeError):
    """Error raised when an immutable class or instance modification occurs."""

    def __init__(
        self,
        code: str,
        message: str,
        user_message: str,
        details: dict[str, Any] | None = None,
    ):
        name: str | None = None
        obj: Any | None = None

        if details is not None:
            name = details.get(builder_config().field)
            obj = details.get(builder_config().arg)

        AttributeError.__init__(self, name=name, obj=obj)

        base_exception.MetaError.__init__(
            self,
            message=message,
            code=code,
            details=details,
            user_message=user_message,
        )
