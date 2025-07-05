"""Tests of the quarryforge.config.exception_conf.fossil_exception_config module."""

import pytest

from quarryforge.config import fossil_config as fc
from quarryforge.config.exception_conf import base_exception_config as bec
from quarryforge.config.exception_conf import exception_config as ec
from quarryforge.config.exception_conf import fossil_exception_config as fec


class TestFossilExceptionConfigModule:
    """Tests for module-level content in fossil_exception_config."""

    def test_module_dunder_all(self):
        """Verify the module's public API."""
        assert sorted(fec.__all__) == sorted(['FossilErrorBuilder'])

    def test_fossil_message_enum(self):
        """Test attributes of the FossilMessage enum."""
        fm = fec.FossilMessage
        assert fm.NO_CMD == f'{fc.Fossil.CMD}: {ec.DescMsg.NONE}'
        assert fm.NO_OUTPUT == (
            f'{fc.Fossil.OUTPUT}: {ec.DescMsg.NONE}'
        )
        assert fm.NO_STDERR == (
            f'{fc.Fossil.STDERR}: {ec.DescMsg.NONE}'
        )
        assert fm.EXPECTED_STR_LIST == 'Expected str or list, got'
        assert fm.EXPECTED_INT == 'Expected int, got'
        assert fm.EXPECTED_STR_OR_NONE == 'Expected str or None, got'
        assert fm.TIMELINE_DETAIL == 'while processing Fossil timeline.'
        assert fm.TIMELINE_USER == (
            'Could not retrieve or parse the Fossil repository timeline.'
        )
        assert fm.SETUP_DETAIL == 'during Fossil repository setup'
        assert fm.SETUP_USER == (
            'There was a problem setting up the Fossil repository.'
        )
        assert fm.INFO_DETAIL == 'while fetching Fossil artifact information.'
        assert fm.INFO_USER == (
            'Could not get details for the specified Fossil artifact.'
        )
        assert fm.DIFF_DETAIL == 'during Fossil diff operation.'
        assert fm.DIFF_USER == (
            'Could not generate or process differences for the Fossil '
            'repository.'
        )
        assert (
            fm.CAT_DETAIL == 'while retrieving file content using Fossil cat.'
        )
        assert fm.CAT_USER == (
            'Could not retrieve file content from the Fossil repository.'
        )
        assert fm.BRANCH_DETAIL == 'during Fossil branch operation.'
        assert fm.BRANCH_USER == (
            'There was a problem with a Fossil branch operation.'
        )
        assert fm.ADD_DETAIL == 'while adding files using Fossil add.'
        assert fm.ADD_USER == (
            'Could not add the specified file(s) to the Fossil repository.'
        )
        assert fm.COMMIT_DETAIL == 'during Fossil commit operation.'
        assert fm.COMMIT_USER == (
            'Could not commit changes to the Fossil repository.'
        )

    def test_fossil_error_path_enum(self):
        """Test FossilErrorPath attributes for correct path construction."""
        assert fec.FossilErrorPath.FOSSIL_PROCESS == (
            'quarryforge.fossil.FOSSIL_PROCESS_ERROR'
        )
        assert fec.FossilErrorPath.FOSSIL_TIMEOUT == (
            'quarryforge.fossil.FOSSIL_TIMEOUT_ERROR'
        )
        assert fec.FossilErrorPath.FOSSIL_TIMELINE == (
            'quarryforge.fossil.Timeline'
        )
        assert fec.FossilErrorPath.FOSSIL_SETUP == 'quarryforge.fossil.Setup'
        assert fec.FossilErrorPath.FOSSIL_INFO == 'quarryforge.fossil.Info'
        assert fec.FossilErrorPath.FOSSIL_DIFF == 'quarryforge.fossil.Diff'
        assert fec.FossilErrorPath.FOSSIL_CAT == 'quarryforge.fossil.Cat'
        assert fec.FossilErrorPath.FOSSIL_BRANCH == 'quarryforge.fossil.Branch'
        assert fec.FossilErrorPath.FOSSIL_ADD == 'quarryforge.fossil.Add'
        assert fec.FossilErrorPath.FOSSIL_COMMIT == 'quarryforge.fossil.Commit'
        assert fec.FossilErrorPath.FOSSIL_CONTROL == 'quarryforge.fossil.Control'
        assert len(fec.FossilErrorPath) == 11


class TestFossilErrorBuilder:
    """Tests for FossilErrorBuilder methods."""

    def test_inheritance(self):
        assert issubclass(fec.FossilErrorBuilder, bec.BaseErrorBuilder)

    @pytest.mark.parametrize(
        'error_context, error_code, extra_details, expected_message',
        [
            (  # FOSSIL_PROCESS
                fec.FossilErrorPath.FOSSIL_PROCESS,
                'PROC_ERR',
                {
                    'cmd': 'fossil version',
                    'return_code': 1,
                    'output': 'out',
                    'stderr': 'err',
                },
                (
                    'Error in `quarryforge.fossil.FOSSIL_PROCESS_ERROR` '
                    '(Code: PROC_ERR). Fossil command failed. Command: '
                    '"fossil version". Return Code: 1. STDOUT: "out". '
                    'STDERR: "err".'
                ),
            ),
            (
                fec.FossilErrorPath.FOSSIL_PROCESS,
                'PROC_ERR',
                {},  # Missing details
                (
                    'Error in `quarryforge.fossil.FOSSIL_PROCESS_ERROR` '
                    '(Code: PROC_ERR). Fossil command failed. Command: '
                    '"cmd: None". Return Code: 1. STDOUT: "output: None". '
                    'STDERR: "stderr: None".'
                ),
            ),
            (  # FOSSIL_TIMEOUT
                fec.FossilErrorPath.FOSSIL_TIMEOUT,
                'TIME_ERR',
                {
                    'cmd': 'fossil pull',
                    'timeout': 60,
                    'output': 'out',
                    'stderr': 'err',
                },
                (
                    'Error in `quarryforge.fossil.FOSSIL_TIMEOUT_ERROR` '
                    '(Code: TIME_ERR). Fossil command timed out after 60 '
                    'seconds. Command: "fossil pull". STDOUT: "out". '
                    'STDERR: "err".'
                ),
            ),
            (
                fec.FossilErrorPath.FOSSIL_TIMEOUT,
                'TIME_ERR',
                {},  # Missing details
                (
                    'Error in `quarryforge.fossil.FOSSIL_TIMEOUT_ERROR` '
                    '(Code: TIME_ERR). Fossil command timed out after '
                    f'{fc.Fossil.DEFAULT_TIMEOUT} seconds. Command: '
                    '"cmd: None". STDOUT: "output: None". STDERR: '
                    '"stderr: None".'
                ),
            ),
            (  # FOSSIL_TIMELINE
                fec.FossilErrorPath.FOSSIL_TIMELINE,
                'PARSE_FAIL',
                {ec.DescMsg.REASON: 'bad format'},
                (
                    'Error in `quarryforge.fossil.Timeline` '
                    '(Code: PARSE_FAIL). Failure while processing Fossil '
                    'timeline. Reason: bad format.'
                ),
            ),
            (
                fec.FossilErrorPath.FOSSIL_TIMELINE,
                'PARSE_FAIL',
                None,  # No reason
                (
                    'Error in `quarryforge.fossil.Timeline` '
                    '(Code: PARSE_FAIL). Failure while processing Fossil '
                    'timeline.'
                ),
            ),
            (  # FOSSIL_SETUP
                fec.FossilErrorPath.FOSSIL_SETUP,
                'SETUP_FAIL',
                {ec.DescMsg.REASON: 'no admin', 'step': 'user creation'},
                (
                    'Error in `quarryforge.fossil.Setup` '
                    '(Code: SETUP_FAIL). Failure during Fossil repository '
                    'setup during user creation. Reason: no admin.'
                ),
            ),
            (
                fec.FossilErrorPath.FOSSIL_SETUP,
                'SETUP_FAIL',
                {ec.DescMsg.REASON: 'no admin'},  # No step
                (
                    'Error in `quarryforge.fossil.Setup` '
                    '(Code: SETUP_FAIL). Failure during Fossil '
                    'repository setup. Reason: no admin.'
                ),
            ),
            (
                fec.FossilErrorPath.FOSSIL_SETUP,
                'SETUP_FAIL',
                {'step': 'user creation'},  # No reason
                (
                    'Error in `quarryforge.fossil.Setup` '
                    '(Code: SETUP_FAIL). Failure during Fossil '
                    'repository setup during user creation.'
                ),
            ),
            (  # FOSSIL_INFO
                fec.FossilErrorPath.FOSSIL_INFO,
                'FETCH_FAIL',
                {ec.DescMsg.REASON: 'not found'},
                (
                    'Error in `quarryforge.fossil.Info` '
                    '(Code: FETCH_FAIL). Failure while fetching Fossil '
                    'artifact information. Reason: not found.'
                ),
            ),
            (  # FOSSIL_DIFF
                fec.FossilErrorPath.FOSSIL_DIFF,
                'GEN_FAIL',
                {ec.DescMsg.REASON: 'too large'},
                (
                    'Error in `quarryforge.fossil.Diff` '
                    '(Code: GEN_FAIL). Failure during Fossil diff operation. '
                    'Reason: too large.'
                ),
            ),
            (  # FOSSIL_CAT
                fec.FossilErrorPath.FOSSIL_CAT,
                'READ_FAIL',
                {ec.DescMsg.REASON: 'permission denied'},
                (
                    'Error in `quarryforge.fossil.Cat` '
                    '(Code: READ_FAIL). Failure while retrieving file content'
                    ' using Fossil cat. Reason: permission denied.'
                ),
            ),
            (  # FOSSIL_BRANCH
                fec.FossilErrorPath.FOSSIL_BRANCH,
                'OP_FAIL',
                {ec.DescMsg.REASON: 'conflict'},
                (
                    'Error in `quarryforge.fossil.Branch` '
                    '(Code: OP_FAIL). Failure during Fossil branch operation'
                    '. Reason: conflict.'
                ),
            ),
            (  # FOSSIL_ADD
                fec.FossilErrorPath.FOSSIL_ADD,
                'ADD_FAIL',
                {ec.DescMsg.REASON: 'file locked'},
                (
                    'Error in `quarryforge.fossil.Add` '
                    '(Code: ADD_FAIL). Failure while adding files using '
                    'Fossil add. Reason: file locked.'
                ),
            ),
            (  # FOSSIL_COMMIT
                fec.FossilErrorPath.FOSSIL_COMMIT,
                'COMMIT_FAIL',
                {ec.DescMsg.REASON: 'check-in failed'},
                (
                    'Error in `quarryforge.fossil.Commit` '
                    '(Code: COMMIT_FAIL). Failure during Fossil commit '
                    'operation. Reason: check-in failed.'
                ),
            ),
            (   # FOSSIL_CONTROL
                fec.FossilErrorPath.FOSSIL_CONTROL,
                'CONTROL_FAIL',
                {ec.DescMsg.REASON: 'control action failure'},
                (
                    'Error in `quarryforge.fossil.Control` '
                    '(Code: CONTROL_FAIL). Failure during Fossil control '
                    'operation (e.g., open, close). Reason: control action '
                    'failure.'
                )
            ),
            (  # Default case (Fossil specific) - uses generic error code
                'quarryforge.fossil.Unknown',
                ec.GenericError.TYPE_ERROR,
                {
                    ec.DescMsg.REASON: 'bad type given',
                    'arg': None,
                },  # Should fall to BaseErrorBuilder.message()
                (
                    'Error in `quarryforge.fossil.Unknown` '
                    '(Code: TYPE_ERROR). Expected type: unknown. '
                    'Got type NoneType with value None instead.'
                ),
            ),
            (  # Default case (Fossil specific) - uses specific error code
                'quarryforge.fossil.Unknown',
                'SPECIFIC_FOSSIL_ERR',
                {ec.DescMsg.REASON: 'custom issue'},
                (
                    'Error in `quarryforge.fossil.Unknown` '
                    '(Code: SPECIFIC_FOSSIL_ERR). An unspecified Fossil '
                    'operation failed Reason: custom issue.'
                ),
            ),
            (  # Default case - fallback to BaseErrorBuilder generic error codes
                'some.other.context.outside.fossil',
                ec.GenericError.VALUE_ERROR,
                {
                    'info': 'test info',
                    'arg': None,
                },
                (
                    'Error in `some.other.context.outside.fossil` '
                    '(Code: VALUE_ERROR). Value None is invalid. '
                    'Expected value: test info.'
                ),
            ),
        ],
    )
    def test_fossil_error_builder_message_mcdc(
        self, error_context, error_code, extra_details, expected_message
    ):
        """Test the message() method for all defined error contexts."""
        builder = fec.FossilErrorBuilder(
            error_context=error_context,
            error_code=error_code,
            extra_details=extra_details,
            arg=extra_details.get('arg') if extra_details else None,
            info=extra_details.get('info') if extra_details else None,
        )
        assert builder.message() == expected_message

    # MC/DC for user_message()
    @pytest.mark.parametrize(
        'error_context, error_code, expected_message',
        [
            (
                fec.FossilErrorPath.FOSSIL_PROCESS,
                'ERR',
                'An issue occurred while running a Fossil command. Please check logs for details.',
            ),
            (
                fec.FossilErrorPath.FOSSIL_TIMEOUT,
                'ERR',
                'A Fossil command took too long to complete and was stopped.',
            ),
            (
                fec.FossilErrorPath.FOSSIL_TIMELINE,
                'ERR',
                fec.FossilMessage.TIMELINE_USER,
            ),
            (
                fec.FossilErrorPath.FOSSIL_SETUP,
                'ERR',
                fec.FossilMessage.SETUP_USER,
            ),
            (fec.FossilErrorPath.FOSSIL_INFO, 'ERR', fec.FossilMessage.INFO_USER),
            (fec.FossilErrorPath.FOSSIL_DIFF, 'ERR', fec.FossilMessage.DIFF_USER),
            (fec.FossilErrorPath.FOSSIL_CAT, 'ERR', fec.FossilMessage.CAT_USER),
            (
                fec.FossilErrorPath.FOSSIL_BRANCH,
                'ERR',
                fec.FossilMessage.BRANCH_USER,
            ),
            (fec.FossilErrorPath.FOSSIL_ADD, 'ERR', fec.FossilMessage.ADD_USER),
            (
                fec.FossilErrorPath.FOSSIL_COMMIT,
                'ERR',
                fec.FossilMessage.COMMIT_USER,
            ),  # Default case - uses generic error code
            (  # fallback to BaseErrorBuilder
                'quarryforge.fossil.Unknown',
                ec.GenericError.VALUE_ERROR,
                'An input value is not valid for this operation.',
            ),  # Default case - uses specific error code
            (  # fallback to BaseErrorBuilder default user message
                'quarryforge.fossil.Unknown',
                'SPECIFIC_FOSSIL_ERR',
                bec.base_error_message().default_user_message,
            ),
            (  # Default case for non-fossil context
                'some.other.context',
                ec.GenericError.NOT_IMPLEMENTED_ERROR,
                'This feature is not available.',
            ),
        ],
    )
    def test_fossil_error_builder_user_message_mcdc(
        self, error_context, error_code, expected_message
    ):
        """Test the user_message() method for all defined error contexts."""
        builder = fec.FossilErrorBuilder(
            error_context=error_context, error_code=error_code
        )
        assert builder.user_message() == expected_message
