from tests.test_config.test_root import get_namedtuple_fields
import pytest

from quarryforge.config import root
from quarryforge.config.exception_conf import base_exception_config as bec
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.meta import assembler


class TestBaseExceptionConfigModule:
    """Tests for module-level constants and classes in base_exception_config."""

    def test_module_dunder_all(self):
        expected_all = ['BaseErrorBuilder']
        assert sorted(bec.__all__) == sorted(expected_all)

    def test_base_config_path(self):
        """Test BaseConfig.path method."""
        assert bec.BaseConfig.path('test_module') == (
            f'{root.PACKAGE.name}.test_module'
        )
        with pytest.raises(TypeError): bec.BaseConfig.path(123)
        with pytest.raises(ValueError): bec.BaseConfig.path('')


    def test_base_error_path_attributes_and_method(self):
        """Test BaseErrorPath attributes and get_full_error_code method."""
        assert bec.BaseErrorPath.MODEL == (
            f'{root.PACKAGE.name}.{root.MODULE.model}'
        )
        assert bec.BaseErrorPath.FOSSIL == (
            f'{root.PACKAGE.name}.{root.MODULE.fossil}'
        )
        assert bec.BaseErrorPath.MAIN == (
            f'{root.PACKAGE.name}.{root.MODULE.main}'
        )
        assert bec.BaseErrorPath.META == (
            f'{root.PACKAGE.name}.{root.SUB_PACKAGE.meta}'
        )
        assert bec.BaseErrorPath.UTIL == (
            f'{root.PACKAGE.name}.{root.SUB_PACKAGE.util}'
        )
        full_code = bec.BaseErrorPath.get_full_error_code(
            'context.path', 'TYPE_SUFFIX'
        )
        assert full_code == 'context.path.TYPE_SUFFIX'

        with pytest.raises(TypeError):
            bec.BaseErrorPath.get_full_error_code(123, 'SUFFIX')
        with pytest.raises(TypeError):
            bec.BaseErrorPath.get_full_error_code('context.path', None)


    def test_base_error_message_config_attributes(self):
        """Test BaseErrorMessageConfig attributes."""
        cfg = bec.BASE_ERROR_MSG
        assert isinstance(cfg, bec.BaseErrorMessageConfig)
        assert cfg.unexpected_error_suffix == ec.GENERIC_ERROR.unexpected_error
        assert cfg.unexpected_error_prefix == (
            'An unexpected error occurred within'
        )
        assert cfg.default_module_suffix == 'module.'
        assert cfg.default_subpackage_suffix == 'subpackage.'
        assert cfg.default_package_suffix == 'package.'
        assert cfg.default_user_message == (
            'An internal application error occurred.'
        )

class TestBaseErrorBuilder:
    """Tests for the BaseErrorBuilder class."""

    def test_inheritance(self):
        assert issubclass(bec.BaseErrorBuilder, assembler.ErrorBuilder)

    def test_code_generation(self):
        builder = bec.BaseErrorBuilder(
            error_context='my.context',
            error_code='MY_CODE'
        )
        assert builder.code() == 'my.context.MY_CODE'

    # MC/DC for message()
    @pytest.mark.parametrize(
        'error_context, error_code, arg, info, extra_details, expected_message',
        [
            (   # TYPE_ERROR
                'ctx.type',
                ec.GENERIC_ERROR.type_error,
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
                ec.GENERIC_ERROR.type_error,
                'abc',
                None,
                None,
                (
                    'Error in `ctx.type` (Code: TYPE_ERROR). Expected type:'
                    ' unknown. Got type str with value \'abc\' instead.'
                ),
            ),
            (   # VALUE_ERROR
                'ctx.value',
                ec.GENERIC_ERROR.value_error,
                'bad_val',
                'a good value',
                None,
                (
                    'Error in `ctx.value` (Code: VALUE_ERROR). Value '
                    '\'bad_val\' is invalid. Expected value: a good value.'
                ),
            ),
            (
                'ctx.value',
                ec.GENERIC_ERROR.value_error,
                10,
                None,
                None,
                (
                    'Error in `ctx.value` (Code: VALUE_ERROR). Value 10 is'
                    ' invalid. Expected value: unknown.'
                ),
             ),
            (   # INVALID_STATE_ERROR
                'ctx.state',
                ec.GENERIC_ERROR.invalid_state,
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
                ec.GENERIC_ERROR.invalid_state,
                None,
                None,
                None,
                (
                    'Error in `ctx.state` (Code: INVALID_STATE_ERROR). '
                    'Attempted an operation in an unknown state.'
                    ' This state is invalid for this operation.'
                ),
            ),
            (   # CONFIGURATION_ERROR
                'ctx.config',
                ec.GENERIC_ERROR.configuration_error,
                None,
                None,
                {'config_key': 'API_KEY', ec.DESC_MSG.reason: 'missing'},
                (
                    'Error in `ctx.config` (Code: CONFIGURATION_ERROR). Missing'
                    ' or invalid configuration for API_KEY missing.'
                ),
            ),
            (
                'ctx.config',
                ec.GENERIC_ERROR.configuration_error,
                None,
                None,
                None,
                (
                    'Error in `ctx.config` (Code: CONFIGURATION_ERROR). Missing'
                    ' or invalid configuration for required configuration'
                    ' with unknown reason.'
                ),
            ),  # DEPENDENCY_ERROR
            (
                'ctx.dependency',
                ec.GENERIC_ERROR.external_dependency_error,
                None,
                None,
                {
                    'dependency': 'fossil',
                    ec.DESC_MSG.reason: 'package not installed'},
                (
                    'Error in `ctx.dependency` (Code: '
                    'EXTERNAL_DEPENDENCY_ERROR).'
                    ' `fossil` failed due to: package not installed.'
                ),
            ),
            (
                'ctx.dependency',
                ec.GENERIC_ERROR.external_dependency_error,
                None,
                None,
                None,
                (
                    'Error in `ctx.dependency` (Code: '
                    'EXTERNAL_DEPENDENCY_ERROR).'
                    ' `unknown dependency` failed due to: unknown reason.'
                ),
            ),
            (   # NOT_IMPLEMENTED_ERROR
                'ctx.ni',
                ec.GENERIC_ERROR.not_implemented_error,
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
                ec.GENERIC_ERROR.not_implemented_error,
                None,
                None,
                None,
                (
                    'Error in `ctx.ni` (Code: NOT_IMPLEMENTED_ERROR). '
                    f'{ec.DESC_MSG.unknown} feature is not implemented.'
                ),
            ),
            (   # UNEXPECTED_ERROR (package context)
                root.PACKAGE.name,
                ec.GENERIC_ERROR.unexpected_error,
                None,
                None,
                None,
                (
                    f'An unexpected error occurred within `{root.PACKAGE.name}`'
                    ' package.'
                ),
            ),
            (   # UNEXPECTED_ERROR (subpackage context)
                f'{root.PACKAGE.name}.{root.SUB_PACKAGE.util}',
                ec.GENERIC_ERROR.unexpected_error,
                None,
                None,
                None,
                (
                    'An unexpected error occurred within '
                    f'`{root.PACKAGE.name}.util` subpackage.'
                ),
            ),
            (   # UNEXPECTED_ERROR (module context)
                f'{root.PACKAGE.name}.model.FossilRepo',
                ec.GENERIC_ERROR.unexpected_error,
                None,
                None,
                None,
                (
                    'An unexpected error occurred within '
                    f'`{root.PACKAGE.name}.model.FossilRepo` module.'
                ),
            ),
            (   # Default case for unknown error_code
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
        ]
    )
    def test_message_mcdc(
            self,
            error_context,
            error_code,
            arg,
            info,
            extra_details,
            expected_message
    ):
        builder = bec.BaseErrorBuilder(
            error_context=error_context, error_code=error_code, arg=arg,
            info=info, extra_details=extra_details
        )
        assert builder.message() == expected_message


    # MC/DC for user_message()
    @pytest.mark.parametrize(
        'error_code, expected_message',
        [
            (
                ec.GENERIC_ERROR.type_error,
                'An input was provided in an incorrect format.'
            ),
            (
                ec.GENERIC_ERROR.value_error,
                'An input value is not valid for this operation.'
            ),
            (
                ec.GENERIC_ERROR.invalid_state,
                'An operation attempted in an invalid application state.'
            ),
            (
                ec.GENERIC_ERROR.configuration_error,
                'There is an issue with the configuration.'
            ),
            (
                ec.GENERIC_ERROR.external_dependency_error,
                'An required tool or service encountered an issue.'
            ),
            (
                ec.GENERIC_ERROR.not_implemented_error,
                'This feature is not available.'
            ),
            (
                ec.GENERIC_ERROR.unexpected_error,
                bec.BASE_ERROR_MSG.default_user_message
            ),
            (   # Default case
                'UNKNOWN_CODE',
                bec.BASE_ERROR_MSG.default_user_message
            ),
        ]
    )
    def test_user_message_mcdc(
            self,
            error_code,
            expected_message
    ):
        builder = bec.BaseErrorBuilder(error_context='some.context', error_code=error_code)
        assert builder.user_message() == expected_message
