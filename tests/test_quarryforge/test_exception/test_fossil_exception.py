"""Unit tests for the quarryforge.exception.fossil_exception module.

This suite provides comprehensive coverage for the custom Fossil-related
exception classes, ensuring correct inheritance, initialization logic,
and type validation.
"""

import logging
import subprocess
from typing import Any

import pytest

from quarryforge.config import fossil_config as config
from quarryforge.config.exception_conf import fossil_exception_config as _
from quarryforge.exception import base_exception, fossil_exception

BASE_ERROR_ARGS = {
    "code": "TEST_CODE",
    "message": "Test technical message",
    "user_message": "Test user message",
}


class TestFossilProcessError:
    """Tests for the FossilProcessError class."""

    def test_inheritance(self):
        """Verify that the class inherits from the correct base classes."""
        logging.info("Testing FossilProcessError: inheritance.")
        assert issubclass(fossil_exception.FossilProcessError, base_exception.FossilError)
        assert issubclass(fossil_exception.FossilProcessError, subprocess.CalledProcessError)

    def test_init_success_with_full_details(self):
        """Test successful initialization when all details are provided."""
        logging.info(
            "Testing FossilProcessError: initialization with full details."
        )
        details = {
            config.Fossil.CMD: ['fossil', 'status'],
            config.Fossil.RETURN_CODE: 1,
            config.Fossil.OUTPUT: b'stdout bytes',
            config.Fossil.STDERR: b'stderr bytes',
        }
        error = fossil_exception.FossilProcessError(**BASE_ERROR_ARGS, details=details)

        assert error.cmd == ['fossil', 'status']
        assert error.returncode == 1
        assert error.stdout == b'stdout bytes'
        assert error.stderr == b'stderr bytes'
        assert error.code == "TEST_CODE"
        assert str(error.args[0]) == "Test technical message"

    def test_init_uses_defaults_when_details_are_missing(self):
        """Test that the initializer falls back to default values correctly."""
        logging.info("Testing FossilProcessError: fallback to default details.")
        error = fossil_exception.FossilProcessError(**BASE_ERROR_ARGS, details={})

        assert error.cmd == _.FossilMessage.NO_CMD
        assert error.returncode == int(config.Fossil.DEFAULT_RETURN_CODE)

        logging.info(
            f'FossilProcessError defaults check: stderr="{error.stderr}", '
            f' stdout="{error.output}"'
        )
        assert error.output == _.FossilMessage.NO_OUTPUT
        assert error.stderr == _.FossilMessage.NO_STDERR

    @pytest.mark.parametrize(
        "key, invalid_value, expected_type_str",
        [
            (config.Fossil.CMD, 123, "str or list"),
            (config.Fossil.RETURN_CODE, "1", "int"),
            (config.Fossil.OUTPUT, 123, "str or None"),
            (config.Fossil.STDERR, 123, "str or None"),
        ]
    )
    def test_init_raises_type_error_for_invalid_detail_types(
        self, key: str, invalid_value: Any, expected_type_str: str
    ):
        """Verify that __init__ raises TypeError for incorrectly typed details."""
        logging.info(
            "Testing FossilProcessError: handling of invalid type for key '%s'.",
            key
        )
        details = {key: invalid_value}
        with pytest.raises(TypeError, match=f"Expected {expected_type_str}"):
            fossil_exception.FossilProcessError(**BASE_ERROR_ARGS, details=details)


class TestFossilTimeoutError:
    """Tests for the FossilTimeoutError class."""

    def test_inheritance(self):
        """Verify that the class inherits from the correct base classes."""
        logging.info("Testing FossilTimeoutError: inheritance.")
        assert issubclass(fossil_exception.FossilTimeoutError, base_exception.FossilError)
        assert issubclass(fossil_exception.FossilTimeoutError, subprocess.TimeoutExpired)

    def test_init_success_with_full_details(self):
        """Test successful initialization when all details are provided."""
        logging.info(
            "Testing FossilTimeoutError: initialization with full details."
        )
        details = {
            config.Fossil.CMD: ['fossil', 'pull'],
            config.Fossil.TIMEOUT: 60.0,
            config.Fossil.OUTPUT: b'stdout bytes',
            config.Fossil.STDERR: b'stderr bytes',
        }
        error = fossil_exception.FossilTimeoutError(**BASE_ERROR_ARGS, details=details)

        assert error.cmd == ['fossil', 'pull']
        assert error.timeout == 60.0
        assert error.stdout == b'stdout bytes'
        assert error.stderr == b'stderr bytes'

    def test_init_uses_defaults_when_details_are_missing(self):
        """Test that the initializer falls back to default values correctly."""
        logging.info("Testing FossilTimeoutError: fallback to default details.")
        error = fossil_exception.FossilTimeoutError(**BASE_ERROR_ARGS, details={})

        assert error.cmd == _.FossilMessage.NO_CMD
        assert error.timeout == int(config.Fossil.DEFAULT_TIMEOUT)
        assert error.output == _.FossilMessage.NO_OUTPUT
        assert error.stderr == _.FossilMessage.NO_STDERR


class TestFossilOperationError:
    """Tests for the FossilOperationError class."""

    def test_inheritance(self):
        """Verify that the class inherits from the correct base class."""
        logging.info("Testing FossilOperationError: inheritance.")
        assert issubclass(fossil_exception.FossilOperationError, base_exception.FossilError)

    def test_initialization(self):
        """Test successful initialization of the simple operation error."""
        logging.info("Testing FossilOperationError: initialization.")
        details = {"reason": "Parsing failed"}
        error = fossil_exception.FossilOperationError(**BASE_ERROR_ARGS, details=details)

        assert error.code == "TEST_CODE"
        assert error.details == details
        assert str(error.args[0]) == "Test technical message"
