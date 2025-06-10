import pytest

from quarryforge.config import fossil_config as fc
from quarryforge.config.exception_conf import fossil_exception_config as fec
from quarryforge.config.exception_conf import base_exception_config as bec
from quarryforge.config.exception_conf import exception_config as ec

class TestFossilExceptionConfigModule:
    """Tests for module-level content in fossil_exception_config."""

    def test_module_dunder_all(self):
        expected_all = ['FossilErrorBuilder']
        assert sorted(fec.__all__) == sorted(expected_all)

    def test_fossil_message_attributes(self):
        """Test attributes of FossilMessage."""
        fm = fec.FOSSIL_MSG
        assert isinstance(fm, fec.FossilMessage)
        assert fm.no_cmd == f'{fc.FOSSIL.cmd}: {ec.DESC_MSG.none}'
        assert fm.no_output == f'{fc.FOSSIL.output}: {ec.DESC_MSG.none}'
        assert fm.no_stderr ==  f'{fc.FOSSIL.stderr}: {ec.DESC_MSG.none}'
        assert fm.expected_str_list == 'Expected str or list, got'
        assert fm.expected_int == 'Expected int, got'
        assert fm.expected_str_or_none == 'Expected str or None, got'
        assert fm.timeline_detail == 'while processing Fossil timeline.'
        assert fm.timeline_user == (
            'Could not retrieve or parse the Fossil repository timeline.'
        )
        assert fm.setup_detail == 'during Fossil repository setup'
        assert fm.setup_user == (
            'There was a problem setting up the Fossil repository.'
        )
        assert fm.info_detail == 'while fetching Fossil artifact information.'
        assert fm.info_user == (
            'Could not get details for the specified Fossil artifact.'
        )
        assert fm.diff_detail == 'during Fossil diff operation.'
        assert fm.diff_user == (
            'Could not generate or process differences for the Fossil '
            'repository.'
        )
        assert fm.cat_detail == 'while retrieving file content using Fossil cat.'
        assert fm.cat_user == (
            'Could not retrieve file content from the Fossil repository.'
        )
        assert fm.branch_detail == 'during Fossil branch operation.'
        assert fm.branch_user == (
            'There was a problem with a Fossil branch operation.'
        )
        assert fm.add_detail == 'while adding files using Fossil add.'
        assert fm.add_user == (
            'Could not add the specified file(s) to the Fossil repository.'
        )
        assert fm.commit_detail == 'during Fossil commit operation.'
        assert fm.commit_user == (
            'Could not commit changes to the Fossil repository.'
        )

    def test_fossil_error_path_attributes(self):
        """Test FossilErrorPath attributes for correct path construction."""
        assert fec.FossilErrorPath.FOSSIL_PROCESS == (
            'quarryforge.fossil.FossilProcess'
        )
        assert fec.FossilErrorPath.FOSSIL_TIMEOUT == (
            'quarryforge.fossil.FossilTimeoutExpired'
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


class TestFossilErrorBuilder:
    """Tests for FossilErrorBuilder methods."""

    def test_inheritance(self):
        assert issubclass(fec.FossilErrorBuilder, bec.BaseErrorBuilder)

    # MC/DC for message()
    @pytest.mark.parametrize(
        'error_context, error_code, extra_details, expected_message',
        [
            (   # FOSSIL_PROCESS
                fec.FossilErrorPath.FOSSIL_PROCESS,
                'PROC_ERR',
                {
                    'cmd': 'fossil version',
                    'return_code': 1,
                    'output': 'out',
                    'stderr': 'err'
                },
                (
                    'Error in `quarryforge.fossil.FossilProcess` '
                    '(Code: PROC_ERR). Fossil command failed. Command: "fossil'
                    ' version". Return Code: 1. STDOUT: "out". STDERR: "err".'
                ),
            ),
            (
                fec.FossilErrorPath.FOSSIL_PROCESS,
                'PROC_ERR',
                {}, # Missing details
                (
                    'Error in `quarryforge.fossil.FossilProcess` '
                    '(Code: PROC_ERR). Fossil command failed. Command: '
                    '"cmd: None". Return Code: unknown. STDOUT: '
                    '"output: None". STDERR: "stderr: None".'
                ),
            ),
            (   # FOSSIL_TIMEOUT
                fec.FossilErrorPath.FOSSIL_TIMEOUT,
                'TIME_ERR',
                {
                    'cmd': 'fossil pull',
                    'timeout': 60,
                    'output': 'out',
                    'stderr': 'err'
                },
                (
                    'Error in `quarryforge.fossil.FossilTimeoutExpired` '
                    '(Code: TIME_ERR). Fossil command timed out after 60 '
                    'seconds. Command: "fossil pull". STDOUT: "out".'
                    ' STDERR: "err".'
                )
            ),
            (
                fec.FossilErrorPath.FOSSIL_TIMEOUT,
                'TIME_ERR',
                {}, # Missing details
                (
                    'Error in `quarryforge.fossil.FossilTimeoutExpired` '
                    '(Code: TIME_ERR). Fossil command timed out after unknown '
                    'seconds. Command: "cmd: None". STDOUT: "output: None".'
                    ' STDERR: "stderr: None".'
                )
            ),
            (   # FOSSIL_TIMELINE
                fec.FossilErrorPath.FOSSIL_TIMELINE,
                'PARSE_FAIL',
                {
                    ec.DESC_MSG.reason: 'bad format'
                },
                (
                    'Error in `quarryforge.fossil.Timeline` '
                    '(Code: PARSE_FAIL). Failure while processing Fossil '
                    'timeline. Reason: bad format.'
                )
            ),
            (
                fec.FossilErrorPath.FOSSIL_TIMELINE,
                'PARSE_FAIL',
                None, # No reason
                (
                    'Error in `quarryforge.fossil.Timeline` '
                    '(Code: PARSE_FAIL). Failure while processing Fossil '
                    'timeline.'
                )
            ),
            (   # FOSSIL_SETUP
                fec.FossilErrorPath.FOSSIL_SETUP,
                'SETUP_FAIL',
                {
                    ec.DESC_MSG.reason: 'no admin',
                    'step': 'user creation'
                },
                (
                    'Error in `quarryforge.fossil.Setup` '
                    '(Code: SETUP_FAIL). Failure during Fossil repository '
                    'setup during user creation. Reason: no admin.'
                )
            ),
            (
                fec.FossilErrorPath.FOSSIL_SETUP,
                'SETUP_FAIL',
                {
                    ec.DESC_MSG.reason: 'no admin'
                }, # No step
                (
                    'Error in `quarryforge.fossil.Setup` '
                    '(Code: SETUP_FAIL). Failure during Fossil '
                    'repository setup. Reason: no admin.'
                )
            ),
            (
                fec.FossilErrorPath.FOSSIL_SETUP,
                'SETUP_FAIL',
                {
                    'step': 'user creation'
                }, # No reason
                (
                    'Error in `quarryforge.fossil.Setup` '
                    '(Code: SETUP_FAIL). Failure during Fossil '
                    'repository setup during user creation.'
                )
            ),
            (   # FOSSIL_INFO
                fec.FossilErrorPath.FOSSIL_INFO,
                'FETCH_FAIL',
                {
                    ec.DESC_MSG.reason: 'not found'
                },
                (
                    'Error in `quarryforge.fossil.Info` '
                    '(Code: FETCH_FAIL). Failure while fetching Fossil '
                    'artifact information. Reason: not found.'
                )
            ),
            (   # FOSSIL_DIFF
                fec.FossilErrorPath.FOSSIL_DIFF,
                'GEN_FAIL',
                {
                    ec.DESC_MSG.reason: 'too large'
                },
                (
                    'Error in `quarryforge.fossil.Diff` '
                    '(Code: GEN_FAIL). Failure during Fossil diff operation. '
                    'Reason: too large.'
                )
            ),
            (   # FOSSIL_CAT
                fec.FossilErrorPath.FOSSIL_CAT,
                'READ_FAIL',
                {
                    ec.DESC_MSG.reason: 'permission denied'
                },
                (
                    'Error in `quarryforge.fossil.Cat` '
                    '(Code: READ_FAIL). Failure while retrieving file content'
                    ' using Fossil cat. Reason: permission denied.'
                )
            ),
            (   # FOSSIL_BRANCH
                fec.FossilErrorPath.FOSSIL_BRANCH,
                'OP_FAIL',
                {
                    ec.DESC_MSG.reason: 'conflict'
                },
                (
                    'Error in `quarryforge.fossil.Branch` '
                    '(Code: OP_FAIL). Failure during Fossil branch operation'
                    '. Reason: conflict.'
                )
            ),
            (   # FOSSIL_ADD
                fec.FossilErrorPath.FOSSIL_ADD,
                'ADD_FAIL',
                {
                    ec.DESC_MSG.reason: 'file locked'
                },
                (
                    'Error in `quarryforge.fossil.Add` '
                    '(Code: ADD_FAIL). Failure while adding files using '
                    'Fossil add. Reason: file locked.'
                )
            ),
            (   # FOSSIL_COMMIT
                fec.FossilErrorPath.FOSSIL_COMMIT,
                'COMMIT_FAIL',
                {
                    ec.DESC_MSG.reason: 'check-in failed'
                },
                (
                    'Error in `quarryforge.fossil.Commit` '
                    '(Code: COMMIT_FAIL). Failure during Fossil commit '
                    'operation. Reason: check-in failed.'
                )
            ),
            (   # Default case (Fossil specific) - uses generic error code
                'quarryforge.fossil.Unknown',
                ec.GENERIC_ERROR.type_error,
                {
                    ec.DESC_MSG.reason: 'bad type given',
                    'arg': None,
                },  # Should fall to BaseErrorBuilder.message()
                (
                    'Error in `quarryforge.fossil.Unknown` '
                    '(Code: TYPE_ERROR). Expected type: unknown. '
                    'Got type NoneType with value None instead.'
                ),
            ),
            (   # Default case (Fossil specific) - uses specific error code
                'quarryforge.fossil.Unknown',
                'SPECIFIC_FOSSIL_ERR',
                {
                    ec.DESC_MSG.reason: 'custom issue'
                },
                (
                    'Error in `quarryforge.fossil.Unknown` '
                    '(Code: SPECIFIC_FOSSIL_ERR). An unspecified Fossil '
                    'operation failed Reason: custom issue.'
                )
            ),
            (   # Default case - fallback to BaseErrorBuilder generic error codes
                'some.other.context.outside.fossil',
                ec.GENERIC_ERROR.value_error,
                {
                    'info': 'test info',
                    'arg': None,
                },
                (
                    'Error in `some.other.context.outside.fossil` '
                    '(Code: VALUE_ERROR). Value None is invalid. '
                    'Expected value: test info.'
                )
            ),
        ]
    )
    def test_fossil_error_builder_message_mcdc(
            self,
            error_context,
            error_code,
            extra_details,
            expected_message
    ):
        builder = fec.FossilErrorBuilder(
            error_context=error_context,
            error_code=error_code,
            extra_details=extra_details,
            arg=extra_details.get('arg') if extra_details else None,
            info=extra_details.get('info') if extra_details else None
        )
        assert builder.message() == expected_message


    # MC/DC for user_message()
    @pytest.mark.parametrize(
        'error_context, error_code, expected_message',
        [
            (
                fec.FossilErrorPath.FOSSIL_PROCESS,
                'ERR',
                'An issue occurred while running a Fossil command. Please check logs for details.'
            ),

            (fec.FossilErrorPath.FOSSIL_TIMEOUT,
             'ERR',
             'A Fossil command took too long to complete and was stopped.'
             ),
            (
                fec.FossilErrorPath.FOSSIL_TIMELINE,
                'ERR',
                fec.FOSSIL_MSG.timeline_user
            ),
            (
                fec.FossilErrorPath.FOSSIL_SETUP,
                'ERR',
                fec.FOSSIL_MSG.setup_user
            ),
            (
                fec.FossilErrorPath.FOSSIL_INFO,
                'ERR',
                fec.FOSSIL_MSG.info_user
            ),
            (
                fec.FossilErrorPath.FOSSIL_DIFF,
                'ERR',
                fec.FOSSIL_MSG.diff_user
            ),
            (
                fec.FossilErrorPath.FOSSIL_CAT,
                'ERR',
                fec.FOSSIL_MSG.cat_user
            ),
            (
                fec.FossilErrorPath.FOSSIL_BRANCH,
                'ERR',
                fec.FOSSIL_MSG.branch_user
            ),
            (
                fec.FossilErrorPath.FOSSIL_ADD,
                'ERR',
                fec.FOSSIL_MSG.add_user
            ),
            (
                fec.FossilErrorPath.FOSSIL_COMMIT,
                'ERR',
                fec.FOSSIL_MSG.commit_user
            ),  # Default case - uses generic error code
            (   # fallback to BaseErrorBuilder
                'quarryforge.fossil.Unknown',
                ec.GENERIC_ERROR.value_error,
                'An input value is not valid for this operation.'
            ),  # Default case - uses specific error code
            (   # fallback to BaseErrorBuilder default user message
                'quarryforge.fossil.Unknown',
                'SPECIFIC_FOSSIL_ERR',
                bec.BASE_ERROR_MSG.default_user_message
            ),
            (   # Default case for non-fossil context
                'some.other.context',
                ec.GENERIC_ERROR.not_implemented_error,
                'This feature is not available.'
            ),
        ]
    )
    def test_fossil_error_builder_user_message_mcdc(self, error_context, error_code, expected_message):
        builder = fec.FossilErrorBuilder(
            error_context=error_context,
            error_code=error_code
        )
        assert builder.user_message() == expected_message
