"""Tests for quarryforge.config.exception_conf.base_exception_config module.

This suite provides comprehensive, MC/DC-focused coverage for the configuration
of base exception classes, error paths, and the BaseErrorBuilder.
"""

import pytest

from quarryforge.config import root
from quarryforge.config.exception_conf import base_exception_config as bec
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.meta import assembler


class TestBaseExceptionConfigModule:
    """Tests for module-level constants and classes."""

    def test_module_dunder_all(self):
        expected_all = ['BaseErrorBuilder']
        assert sorted(bec.__all__) == sorted(expected_all)

    def test_build_path(self):
        """Test the build_path helper function."""
        assert bec.build_path('test_suffix') == 'quarryforge.test_suffix'
        with pytest.raises(TypeError):
            bec.build_path(123)
        with pytest.raises(ValueError):
            bec.build_path('')

    def test_get_full_error_code(self):
        """Test the get_full_error_code helper function."""
        # Success case
        full_code = bec.get_full_error_code('ctx.path', 'CODE')
        assert full_code == 'ctx.path.CODE'
        # Failure cases handled by decorator
        with pytest.raises(TypeError):
            bec.get_full_error_code(123, 'CODE')
        with pytest.raises(TypeError):
            bec.get_full_error_code('ctx.path', None)
        with pytest.raises(ValueError):
            bec.get_full_error_code('', 'CODE')

    def test_base_error_path_enum(self):
        """Test the BaseErrorPath StrEnum attributes."""
        assert bec.BaseErrorPath.MODEL == 'quarryforge.model'
        assert bec.BaseErrorPath.FOSSIL == 'quarryforge.fossil'
        assert bec.BaseErrorPath.MAIN == 'quarryforge.main'
        assert bec.BaseErrorPath.META == 'quarryforge.meta'
        assert bec.BaseErrorPath.UTIL == 'quarryforge.util'

    def test_base_error_message_factory(self):
        """Test the base_error_message factory and its config object."""
        cfg = bec.base_error_message()
        assert isinstance(cfg, bec.BaseErrorMessageConfig)
        assert cfg.unexpected_error_suffix == ec.GenericError.UNEXPECTED_ERROR
        assert cfg.default_user_message == (
            'An internal application error occurred.'
        )


class TestBaseErrorBuilder:
    """Tests for the BaseErrorBuilder class."""

    def test_inheritance(self):
        """Verify that BaseErrorBuilder inherits from the correct ABC."""
        assert issubclass(bec.BaseErrorBuilder, assembler.ErrorBuilder)

    def test_code_generation(self):
        """Test the standard code generation format."""
        builder = bec.BaseErrorBuilder(
            error_context='my.context', error_code='MY_CODE'
        )
        assert builder.code() == 'my.context.MY_CODE'

    # parameterized test covers all paths for the message() method
    @pytest.mark.parametrize(
        'error_context, error_code, arg, info, extra_details, expected_message',
        [
            (  # TYPE_ERROR
                'ctx.type',
                ec.GenericError.TYPE_ERROR,
                123,
                'a string',
                None,
                (
                    'Error in `ctx.type` (Code: TYPE_ERROR). Expected type: a'
                    ' string. Got type int with value 123 instead.'
                ),
            ),
            (
                'ctx.type',
                ec.GenericError.TYPE_ERROR,
                'abc',
                None,
                None,
                (
                    'Error in `ctx.type` (Code: TYPE_ERROR). Expected type:'
                    " unknown. Got type str with value 'abc' instead."
                ),
            ),
            (  # VALUE_ERROR
                'ctx.value',
                ec.GenericError.VALUE_ERROR,
                'bad_val',
                'a good value',
                None,
                (
                    'Error in `ctx.value` (Code: VALUE_ERROR). Value '
                    "'bad_val' is invalid. Expected value: a good value."
                ),
            ),
            (
                'ctx.value',
                ec.GenericError.VALUE_ERROR,
                10,
                None,
                None,
                (
                    'Error in `ctx.value` (Code: VALUE_ERROR). Value 10 is'
                    ' invalid. Expected value: unknown.'
                ),
            ),
            (  # INVALID_STATE_ERROR
                'ctx.state',
                ec.GenericError.INVALID_STATE_ERROR,
                None,
                None,
                {'action': 'commit', 'current_state': 'test_state'},
                (
                    'Error in `ctx.state` (Code: INVALID_STATE_ERROR). '
                    'Attempted commit in test_state. This state is invalid'
                    ' for this operation.'
                ),
            ),
            (
                'ctx.state',
                ec.GenericError.INVALID_STATE_ERROR,
                None,
                None,
                None,
                (
                    'Error in `ctx.state` (Code: INVALID_STATE_ERROR). '
                    'Attempted an operation in an unknown state.'
                    ' This state is invalid for this operation.'
                ),
            ),
            (  # CONFIGURATION_ERROR
                'ctx.config',
                ec.GenericError.CONFIGURATION_ERROR,
                None,
                None,
                {'config_key': 'API_KEY', ec.DescMsg.REASON: 'missing'},
                (
                    'Error in `ctx.config` (Code: CONFIGURATION_ERROR). Missing'
                    ' or invalid configuration for API_KEY. Reason: missing.'
                ),
            ),
            (
                'ctx.config',
                ec.GenericError.CONFIGURATION_ERROR,
                None,
                None,
                None,
                (
                    'Error in `ctx.config` (Code: CONFIGURATION_ERROR). Missing'
                    ' or invalid configuration for required configuration.'
                    ' Reason: with unknown reason.'
                ),
            ),  # DEPENDENCY_ERROR
            (
                'ctx.dependency',
                ec.GenericError.EXTERNAL_DEPENDENCY_ERROR,
                None,
                None,
                {
                    'dependency': 'fossil',
                    ec.DescMsg.REASON: 'package not installed',
                },
                (
                    'Error in `ctx.dependency` (Code: '
                    'EXTERNAL_DEPENDENCY_ERROR).'
                    ' `fossil` failed due to: package not installed.'
                ),
            ),
            (
                'ctx.dependency',
                ec.GenericError.EXTERNAL_DEPENDENCY_ERROR,
                None,
                None,
                None,
                (
                    'Error in `ctx.dependency` (Code: '
                    'EXTERNAL_DEPENDENCY_ERROR).'
                    ' `unknown dependency` failed due to: unknown reason.'
                ),
            ),
            (  # NOT_IMPLEMENTED_ERROR
                'ctx.ni',
                ec.GenericError.NOT_IMPLEMENTED_ERROR,
                None,
                'Special Feature',
                None,
                (
                    'Error in `ctx.ni` (Code: NOT_IMPLEMENTED_ERROR). '
                    'Special Feature is not implemented.'
                ),
            ),
            (
                'ctx.ni',
                ec.GenericError.NOT_IMPLEMENTED_ERROR,
                None,
                None,
                None,
                (
                    'Error in `ctx.ni` (Code: NOT_IMPLEMENTED_ERROR). '
                    f'{ec.DescMsg.UNKNOWN} feature is not implemented.'
                ),
            ),
            (  # UNEXPECTED_ERROR (package context)
                root.Package.NAME,
                ec.GenericError.UNEXPECTED_ERROR,
                None,
                None,
                None,
                (
                    f'An unexpected error occurred within `{root.Package.NAME}`'
                    ' package.'
                ),
            ),
            (  # UNEXPECTED_ERROR (subpackage context)
                f'{root.Package.NAME}.{root.SubPackage.UTIL}',
                ec.GenericError.UNEXPECTED_ERROR,
                None,
                None,
                None,
                (
                    'An unexpected error occurred within '
                    f'`{root.Package.NAME}.util` subpackage.'
                ),
            ),
            (  # UNEXPECTED_ERROR (module context)
                f'{root.Package.NAME}.{root.Module.MODEL}.FossilRepo',
                ec.GenericError.UNEXPECTED_ERROR,
                None,
                None,
                None,
                (
                    'An unexpected error occurred within '
                    f'`{root.Package.NAME}.model.FossilRepo` module.'
                ),
            ),
            (  # Default case for unknown error_code
                'ctx.default',
                'UNKNOWN_CODE',
                None,
                None,
                None,
                (
                    'Error in `ctx.default` (Code: UNKNOWN_CODE).'
                    ' Error code UNKNOWN_CODE unhandled is an unexpected'
                    ' error.'
                ),
            ),
        ],
    )
    def test_message_mcdc(
        self,
        error_context,
        error_code,
        arg,
        info,
        extra_details,
        expected_message,
    ):
        """Test the message() method for all defined error codes."""
        builder = bec.BaseErrorBuilder(
            error_context=error_context, error_code=error_code,
            arg=arg, info=info, extra_details=extra_details
        )
        assert builder.message() == expected_message


    # MC/DC parameterized test covers all paths for the user_message() method
    @pytest.mark.parametrize(
        'error_code, expected_message',
        [
            (
                ec.GenericError.TYPE_ERROR,
                'An input was provided in an incorrect format.',
            ),
            (
                ec.GenericError.VALUE_ERROR,
                'An input value is not valid for this operation.',
            ),
            (
                ec.GenericError.INVALID_STATE_ERROR,
                'An operation attempted in an invalid application state.',
            ),
            (
                ec.GenericError.CONFIGURATION_ERROR,
                'There is an issue with the configuration.',
            ),
            (
                ec.GenericError.EXTERNAL_DEPENDENCY_ERROR,
                'An required tool or service encountered an issue.',
            ),
            (
                ec.GenericError.NOT_IMPLEMENTED_ERROR,
                'This feature is not available.',
            ),
            (
                ec.GenericError.UNEXPECTED_ERROR,
                bec.base_error_message().default_user_message,
            ),
            (  # Default case
                'UNKNOWN_CODE',
                bec.base_error_message().default_user_message,
            ),
        ],
    )
    def test_user_message_mcdc(self, error_code, expected_message):
        builder = bec.BaseErrorBuilder(
            error_context='some.context', error_code=error_code
        )
        assert builder.user_message() == expected_message
