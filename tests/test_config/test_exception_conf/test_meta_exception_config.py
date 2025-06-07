"""tests/test_config/test_meta_exception_config.py"""
import pytest

from quarryforge.config import root
from quarryforge.config.exception_conf import meta_exception_config as mec
from quarryforge.config.exception_conf import base_exception_config as bec
from quarryforge.config.exception_conf import exception_config as ec


class TestDummyClass: pass
class TestDummyInstance: pass


class TestMetaExceptionConfigModule:
    """Tests for module-level content in meta_exception_config."""

    def test_module_dunder_all(self):
        """Test the __all__ variable for completeness."""
        expected_all = ['MetaErrorBuilder']
        assert sorted(mec.__all__) == sorted(expected_all)

    def test_meta_error_code_attributes(self):
        """Test attributes of MetaErrorCode."""
        assert mec.META_ERROR_CODE.ASSEMBLER_ERROR == (
            'ASSEMBLER_ERROR'
        )
        assert mec.META_ERROR_CODE.IMMUTABILITY_VIOLATION == (
            'IMMUTABILITY_VIOLATION'
        )

    def test_meta_error_messages_attributes(self):
        """Test attributes of MetaErrorMessages."""
        assert mec.META_MSG.immutable_violation_user == (
            'Attempted to modify an immutable object.'
        )
        assert mec.META_MSG.assembler_error_user == (
            'A fatal error occured while assembling an error message.'
        )
        assert mec.META_MSG.default_meta_user == (
            'An error occurred in the meta subpackage.'
        )

    def test_meta_error_path_attributes(self):
        """Test MetaErrorPath attributes for correct path construction."""
        root_path = f'{root.PACKAGE.name}.{root.SUB_PACKAGE.meta}'
        assert mec.MetaErrorPath.META_ROOT_CONTEXT == root_path

        immutable_path = f'{root_path}.{root.META_MODULE.immutable}'
        assert mec.MetaErrorPath.IMMUTABLE_CONTEXT == immutable_path
        assert mec.MetaErrorPath.IMMUTABLE_NAMESPACE == (
            f'{immutable_path}.Namespace'
        )
        assert mec.MetaErrorPath.IMMUTABLE_INSTANCE == (
            f'{immutable_path}.Instance'
        )

        assembler_path = f'{root_path}.{root.META_MODULE.assembler}'
        assert mec.MetaErrorPath.ASSEMBLER_CONTEXT == assembler_path


class TestMetaErrorBuilder:
    """Tests for MetaErrorBuilder class."""

    def test_inheritance(self):
        """Verify that MetaErrorBuilder inherits from BaseErrorBuilder."""
        assert issubclass(mec.MetaErrorBuilder, bec.BaseErrorBuilder)

    @pytest.mark.parametrize(
        'error_code, error_context, arg, field, info, expected_message',
        [   # === IMMUTABILITY_VIOLATION Tests ===
            (
                mec.META_ERROR_CODE.IMMUTABILITY_VIOLATION,
                mec.MetaErrorPath.IMMUTABLE_INSTANCE,
                TestDummyInstance(),
                'attr1',
                'set value',
                (
                    'Error in `quarryforge.meta.immutable.Instance` (Code:'
                    ' IMMUTABILITY_VIOLATION): Cannot set value on immutable'
                    ' object "TestDummyInstance". Attempted to modify'
                    ' attribute: attr1.'
                ),
            ),
            (
                mec.META_ERROR_CODE.IMMUTABILITY_VIOLATION,
                mec.MetaErrorPath.IMMUTABLE_NAMESPACE,
                TestDummyClass,
                'attr2',
                'delete attribute',
                (
                    'Error in `quarryforge.meta.immutable.Namespace` (Code:'
                    ' IMMUTABILITY_VIOLATION): Cannot delete attribute on'
                    ' immutable object "TestDummyClass". Attempted to modify'
                    ' attribute: attr2.'
                ),
            ),
            (   # === ASSEMBLER_ERROR Tests ===
                mec.META_ERROR_CODE.ASSEMBLER_ERROR,
                mec.MetaErrorPath.ASSEMBLER_CONTEXT,
                None,
                'field1',
                'bad data provided',
                (
                    'Error in `quarryforge.meta.assembler` (Code: '
                    'ASSEMBLER_ERROR): Error builder assembly failure: bad '
                    'data provided. Issue with field: field1.'
                ),
            ),
            (   # === Fallback to BaseErrorBuilder Tests ===
                ec.GENERIC_ERROR.type_error,
                mec.MetaErrorPath.META_ROOT_CONTEXT,
                123,
                None,
                'a string',
                (
                    'Error in `quarryforge.meta` (Code: TYPE_ERROR): Expected'
                    ' type: a string. Got type int with value "123" instead.'                ),
            ),
            (
                ec.GENERIC_ERROR.value_error,
                mec.MetaErrorPath.ASSEMBLER_CONTEXT,
                'bad',
                None,
                'good',
                (
                    'Error in `quarryforge.meta.assembler` (Code: VALUE_ERROR):'
                    ' Value "\'bad\'" is invalid. Expected value: good.'
                )
            ),
        ]
    )
    def test_message_mcdc(
            self,
            error_code,
            error_context,
            arg, field,
            info,
            expected_message
    ):
        """Test the message() method with MC/DC approach."""
        builder = mec.MetaErrorBuilder(
            error_context=error_context, error_code=error_code,
            arg=arg, field=field, info=info
        )
        print(
            (
                'built message: \n'
                f'\t{builder.message()}\n'
                'expected: \n'
                f'\t{expected_message}'
            )
        )
        assert builder.message() == expected_message

    @pytest.mark.parametrize(
        'error_code, expected_message',
        [
            (   # Test specific meta error codes
                mec.META_ERROR_CODE.IMMUTABILITY_VIOLATION,
                mec.META_MSG.immutable_violation_user
            ),
            (
                mec.META_ERROR_CODE.ASSEMBLER_ERROR,
                mec.META_MSG.assembler_error_user
            ),
            (   # Test fallback to BaseErrorBuilder for generic codes
                ec.GENERIC_ERROR.value_error,
                'An input value is not valid for this operation.'
            ),
            (
                ec.GENERIC_ERROR.configuration_error,
                'There is an issue with the configuration.'
            ),
            (   # Test the final default case for unknown meta-specific codes
                'UNKNOWN_META_CODE',
                mec.META_MSG.default_meta_user
            ),
        ]
    )
    def test_user_message_mcdc(self, error_code, expected_message):
        """Test the user_message() method with MC/DC approach."""
        builder = mec.MetaErrorBuilder(error_context='any.meta.context', error_code=error_code)
        assert builder.user_message() == expected_message
