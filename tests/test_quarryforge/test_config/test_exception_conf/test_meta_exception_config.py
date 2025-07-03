"""Unit test quarryforge.config.exception_conf.meta_exception_config module."""

import pytest

from quarryforge.config import root
from quarryforge.config.exception_conf import base_exception_config as bec
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.config.exception_conf import meta_exception_config as mec


class TestDummyClass:
    pass


class TestDummyInstance:
    pass


class TestMetaExceptionConfigModule:
    """Tests for module-level content in meta_exception_config."""

    def test_module_dunder_all(self):
        """Verify the module's public API."""
        assert mec.__all__ == ['MetaErrorBuilder']

    def test_MetaErrorCode_enum(self):
        """Test attributes of MetaErrorCode enum."""
        assert mec.MetaErrorCode.ASSEMBLER_ERROR == 'ASSEMBLER_ERROR'
        assert mec.MetaErrorCode.IMMUTABILITY_VIOLATION == (
            'IMMUTABILITY_VIOLATION')

    def test_meta_error_messages_factory(self):
        """Test the meta_error_message factory and its NamedTuple."""
        cfg = mec.meta_error_message()
        assert isinstance(cfg, mec.MetaErrorMessages)
        assert cfg.immutable_violation_user == (
            'Attempted to modify an immutable object.')
        assert cfg.assembler_error_user == (
            'A fatal error occured while assembling an error message.'
        )
        assert cfg.default_meta_user == (
            'An error occurred in the meta subpackage.'
        )

    def test_meta_error_path_enum(self):
        """Test MetaErrorPath attributes for correct path construction."""
        root_path = bec.build_path(root.SubPackage.META)
        assert mec.MetaErrorPath.META_ROOT_CONTEXT == root_path

        immutable_path = bec.get_full_error_code(
            root_path, root.MetaModule.IMMUTABLE)
        assert mec.MetaErrorPath.IMMUTABLE_CONTEXT == immutable_path
        assert mec.MetaErrorPath.IMMUTABLE_NAMESPACE == (
            f'{immutable_path}.Namespace'
        )
        assert mec.MetaErrorPath.IMMUTABLE_INSTANCE == (
            f'{immutable_path}.Instance'
        )

        assembler_path = bec.get_full_error_code(
            root_path, root.MetaModule.ASSEMBLER)
        assert mec.MetaErrorPath.ASSEMBLER_CONTEXT == assembler_path


class TestMetaErrorBuilder:
    """Tests for MetaErrorBuilder class."""

    def test_inheritance(self):
        """Verify that MetaErrorBuilder inherits from BaseErrorBuilder."""
        assert issubclass(mec.MetaErrorBuilder, bec.BaseErrorBuilder)

    @pytest.mark.parametrize(
        'error_code, error_context, arg, field, info, expected_message',
        [  # === IMMUTABILITY_VIOLATION Tests ===
            (
                mec.MetaErrorCode.IMMUTABILITY_VIOLATION,
                mec.MetaErrorPath.IMMUTABLE_INSTANCE,
                TestDummyInstance(),
                'attr1',
                'set value',
                (
                    'Error in `quarryforge.meta.immutable.Instance` (Code:'
                    ' IMMUTABILITY_VIOLATION). Cannot set value on immutable'
                    ' object "TestDummyInstance". Attempted to modify'
                    ' attribute: attr1.'
                ),
            ),
            (
                mec.MetaErrorCode.IMMUTABILITY_VIOLATION,
                mec.MetaErrorPath.IMMUTABLE_NAMESPACE,
                TestDummyClass,
                'attr2',
                'delete attribute',
                (
                    'Error in `quarryforge.meta.immutable.Namespace` (Code:'
                    ' IMMUTABILITY_VIOLATION). Cannot delete attribute on'
                    ' immutable object "TestDummyClass". Attempted to modify'
                    ' attribute: attr2.'
                ),
            ),
            (  # === ASSEMBLER_ERROR Tests ===
                mec.MetaErrorCode.ASSEMBLER_ERROR,
                mec.MetaErrorPath.ASSEMBLER_CONTEXT,
                None,
                'field1',
                'bad data provided',
                (
                    'Error in `quarryforge.meta.assembler` (Code: '
                    'ASSEMBLER_ERROR). Error builder assembly failure: bad '
                    'data provided. Issue with field: field1.'
                ),
            ),
            (  # === Fallback to BaseErrorBuilder Tests ===
                ec.GenericError.TYPE_ERROR,
                mec.MetaErrorPath.META_ROOT_CONTEXT,
                123,
                None,
                'a string',
                (
                    'Error in `quarryforge.meta` (Code: TYPE_ERROR). Expected'
                    ' type: a string. Got type int with value 123 instead.'
                ),
            ),
            (
                ec.GenericError.VALUE_ERROR,
                mec.MetaErrorPath.ASSEMBLER_CONTEXT,
                'bad',
                None,
                'good',
                (
                    'Error in `quarryforge.meta.assembler` (Code: VALUE_ERROR).'
                    ' Value \'bad\' is invalid. Expected value: good.'
                ),
            ),
        ],
    )
    def test_message_mcdc(
        self, error_code, error_context, arg, field, info, expected_message
    ):
        """Test the message() method with MC/DC approach."""
        builder = mec.MetaErrorBuilder(
            error_context=error_context,
            error_code=error_code,
            arg=arg,
            field=field,
            info=info,
        )
        print(
            'built message: \n'
            f'\t{builder.message()}\n'
            'expected: \n'
            f'\t{expected_message}'
        )
        assert builder.message() == expected_message

    @pytest.mark.parametrize(
        'error_code, expected_message',
        [
            (  # Test specific meta error codes
                mec.MetaErrorCode.IMMUTABILITY_VIOLATION,
                mec.meta_error_message().immutable_violation_user,
            ),
            (
                mec.MetaErrorCode.ASSEMBLER_ERROR,
                mec.meta_error_message().assembler_error_user,
            ),
            (  # Test fallback to BaseErrorBuilder for generic codes
                ec.GenericError.VALUE_ERROR,
                'An input value is not valid for this operation.',
            ),
            (
                ec.GenericError.CONFIGURATION_ERROR,
                'There is an issue with the configuration.',
            ),
            (  # Test the final default case for unknown meta-specific codes
                'UNKNOWN_META_CODE',
                mec.meta_error_message().default_meta_user,
            ),
        ],
    )
    def test_user_message_mcdc(self, error_code, expected_message):
        """Test the user_message() method with MC/DC approach."""
        builder = mec.MetaErrorBuilder(
            error_context='any.meta.context', error_code=error_code
        )
        assert builder.user_message() == expected_message
