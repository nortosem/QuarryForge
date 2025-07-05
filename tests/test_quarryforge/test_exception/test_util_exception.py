"""Unit tests for the quarryforge.exception.model_exception module.

This suite provides comprehensive coverage for the FossilRepoError,
FossilCommitError, and FossilTimelineError exception classes.
"""

import logging

import pytest

from quarryforge.exception import base_exception, model_exception

BASE_ERROR_ARGS = {
    'code': 'MODEL_TEST_CODE',
    'message': 'A test technical message for a model error.',
    'user_message': 'A test user message for a model error.',
    'details': {'source': 'test_suite'},
}


class TestModelExceptions:
    """Tests all exception classes within the model_exception module."""

    @pytest.mark.parametrize(
        "exception_class",
        [
            model_exception.FossilRepoError,
            model_exception.FossilCommitError,
            model_exception.FossilTimelineError,
        ],
    )
    def test_exception_instantiation_and_inheritance(
        self, exception_class: type[base_exception.ModelError]
    ) -> None:
        """Tests initialization, attribute correctness, and inheritance for each
        model exception class. This single test covers all MC/DC paths for
        these simple classes.
        """
        class_name = exception_class.__name__
        logging.info("Testing exception class: %s", class_name)

        error_instance = exception_class(**BASE_ERROR_ARGS)

        assert isinstance(error_instance, base_exception.ModelError)
        assert isinstance(error_instance, base_exception.QuarryForgeError)
        assert isinstance(error_instance, Exception)
        assert issubclass(exception_class, base_exception.ModelError)

        assert error_instance.code == BASE_ERROR_ARGS['code']
        assert str(error_instance.args[0]) == BASE_ERROR_ARGS['message']
        assert error_instance.user_message == BASE_ERROR_ARGS['user_message']
        assert error_instance.details == BASE_ERROR_ARGS['details']

    @pytest.mark.parametrize(
        "exception_class",
        [
            model_exception.FossilRepoError,
            model_exception.FossilCommitError,
            model_exception.FossilTimelineError,
        ],
    )
    def test_exception_is_catchable(
        self, exception_class: type[base_exception.ModelError]
    ) -> None:
        """Functional test to ensure each exception can be raised and caught
        by its own type and by its parent types.
        """
        logging.info(
            'Testing catchability of exception class: %s',
            exception_class
        )

        try:
            raise exception_class(**BASE_ERROR_ARGS)
        except exception_class as e:
            assert e.code == BASE_ERROR_ARGS["code"]
        except Exception as e:
            pytest.fail(
                f'Did not catch {class_name} correctly. Caught '
                f'{type(e)} instead.'
            )

        try:
            raise exception_class(**BASE_ERROR_ARGS)
        except base_exception.ModelError as e:
            assert e.code == BASE_ERROR_ARGS["code"]
        except Exception as e:
            pytest.fail(
                f'Did not catch {class_name} as a ModelError. Caught '
                f'{type(e)} instead.'
            )
