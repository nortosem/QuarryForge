"""Tests for the root configuration module.

This test suite uses a parameterized approach to ensure that all StrEnum
classes in quarryforge.config.root are correctly defined, have the
expected members, and that their values (whether explicit or from auto())
are correct.
"""

import pytest

from quarryforge.config import root


ENUM_TEST_CASES = [
    (
        root.Package,
        1,
        [('NAME', 'quarryforge')],
    ),
    (
        root.Module,
        2,
        [
            ('MAIN', 'main'),
            ('MODEL', 'model'),
        ],
    ),
    (
        root.SubPackage,
        5,
        [
            ('CONFIG', 'config'),
            ('EXCEPTION', 'exception'),
            ('FOSSIL', 'fossil'),
            ('META', 'meta'),
            ('UTIL', 'util'),
        ],
    ),
    (
        root.MetaModule,
        2,
        [
            ('ASSEMBLER', 'assembler'),
            ('IMMUTABLE', 'immutable'),
        ],
    ),
    (
        root.Model,
        3,
        [
            ('FOSSIL_COMMIT', 'FossilCommit'),
            ('FOSSIL_REPO', 'FossilRepo'),
            ('FOSSIL_TIMELINE', 'FossilTimeline'),
        ],
    ),
    (
        root.FossilModule,
        9,
        [
            ('TIMELINE', 'Timeline'),
            ('SETUP', 'Setup'),
            ('INFO', 'Info'),
            ('DIFF', 'Diff'),
            ('CAT', 'Cat'),
            ('BRANCH', 'Branch'),
            ('ADD', 'Add'),
            ('COMMIT', 'Commit'),
            ('CONTROL', 'Control'),
        ],
    ),
    (
        root.UtilModule,
        5,
        [
            ('DECORATOR', 'decorator'),
            ('FOSSIL_UTIL', 'fossil_util'),
            ('MAIN_UTIL', 'main_util'),
            ('MODEL_UTIL', 'model_util'),
            ('VALIDATION_UTIL', 'validation_util'),
        ],
    ),
]


class TestRootConfig:
    """Tests for the configuration constants in quarryforge.config.root."""

    def test_module_dunder_all(self) -> None:
        """Test the __all__ variable to ensure it exports all enums."""
        expected_all = [
            'Package',
            'Module',
            'SubPackage',
            'MetaModule',
            'Model',
            'FossilModule',
            'UtilModule',
        ]
        assert sorted(root.__all__) == sorted(expected_all)

    @pytest.mark.parametrize(
        'enum_class, expected_count, expected_members', ENUM_TEST_CASES
    )
    def test_str_enum_definitions(
        self,
        enum_class: type[root.StrEnum],
        expected_count: int,
        expected_members: list[tuple[str, str]],
    ) -> None:
        """Verify enum members, values, and total count for all enums.

        This single parameterized test covers all StrEnum classes defined in
        the ENUM_TEST_CASES list, ensuring:
        1. The total number of members in the enum is correct.
        2. Every expected member exists.
        3. The string value of each member is correct.
        """
        assert (
            len(enum_class) == expected_count
        ), f'Mismatch in member count for {enum_class.__name__}'

        for member_name, expected_value in expected_members:
            assert hasattr(
                enum_class, member_name
            ), f'{enum_class.__name__} is missing member {member_name}'

            member = getattr(enum_class, member_name)
            assert member == expected_value, (
                f'Value mismatch for {enum_class.__name__}.{member_name}: '
                f'Expected "{expected_value}", got "{member}"'
            )
