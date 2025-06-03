import pytest
from typing import NamedTuple

from quarryforge.config import root

def get_namedtuple_fields(nt_class):
    """Get all fields from a NamedTuple class"""
    return nt_class._fields


class TestRootConfig:
    """Tests for quarryforge.config.root"""

    def test_module_dunder_all(self):
        """Test the __all__ variable."""
        expected_all = [
            'PACKAGE', 'MODULE', 'SUB_PACKAGE', 'META_MODULE',
            'MODEL', 'FOSSIL', 'UTIL_MODULE'
        ]
        assert sorted(root.__all__) == sorted(expected_all)

    def test_package_attributes(self):
        """Test attributes of Package."""
        pkg = root.PACKAGE
        assert isinstance(pkg, root.Package)
        assert pkg.name == 'quarryforge'
        assert get_namedtuple_fields(root.Package) == ('name',)

    def test_module_attributes(self):
        """Test attributes of Module."""
        mod = root.MODULE
        assert isinstance(mod, root.Module)
        assert mod.fossil == 'fossil'
        assert mod.main == 'main'
        assert mod.model == 'model'
        assert get_namedtuple_fields(root.Module) == ('fossil', 'main', 'model')

    def test_sub_package_attributes(self):
        """Test attributes of SubPackage."""
        sub_pkg = root.SUB_PACKAGE
        assert isinstance(sub_pkg, root.SubPackage)
        assert sub_pkg.config == 'config'
        assert sub_pkg.exception == 'exception'
        assert sub_pkg.meta == 'meta'
        assert sub_pkg.util == 'util'
        assert get_namedtuple_fields(root.SubPackage) == ('config', 'exception', 'meta', 'util')

    def test_meta_module_attributes(self):
        """Test attributes of MetaModule."""
        meta_mod = root.META_MODULE
        assert isinstance(meta_mod, root.MetaModule)
        assert meta_mod.assembler == 'assembler'
        assert meta_mod.immutable == 'immutable'
        assert get_namedtuple_fields(root.MetaModule) == ('assembler', 'immutable')

    def test_model_attributes(self):
        """Test attributes of Model."""
        mdl = root.MODEL
        assert isinstance(mdl, root.Model)
        assert mdl.fossil_commit == 'FossilCommit'
        assert mdl.fossil_repo == 'FossilRepo'
        assert mdl.fossil_timeline == 'FossilTimeline'
        assert get_namedtuple_fields(root.Model) == ('fossil_commit', 'fossil_repo', 'fossil_timeline')

    def test_fossil_command_attributes(self):
        """Test attributes of FossilCommand."""
        fos_cmd = root.FOSSIL # Global constant is FOSSIL
        assert isinstance(fos_cmd, root.FossilCommand)
        assert fos_cmd.process == 'FossilProcess'
        assert fos_cmd.timeout == 'FossilTimeoutExpired'
        assert fos_cmd.timeline == 'Timeline'
        assert fos_cmd.setup == 'Setup'
        assert fos_cmd.info == 'Info'
        assert fos_cmd.diff == 'Diff'
        assert fos_cmd.cat == 'Cat'
        assert fos_cmd.branch == 'Branch'
        assert fos_cmd.add == 'Add'
        assert fos_cmd.commit == 'Commit'
        expected_fields = (
            'process', 'timeout', 'timeline', 'setup', 'info', 'diff',
            'cat', 'branch', 'add', 'commit'
        )
        assert get_namedtuple_fields(root.FossilCommand) == expected_fields

    def test_util_module_attributes(self):
        """Test attributes of UtilModule."""
        util_mod = root.UTIL_MODULE
        assert isinstance(util_mod, root.UtilModule)
        assert util_mod.fossil_util == 'fossil_util'
        assert util_mod.main_util == 'main_util'
        assert util_mod.model_util == 'model_util'
        expected_fields = ('fossil_util', 'main_util', 'model_util')
        assert get_namedtuple_fields(root.UtilModule) == expected_fields

    def test_global_constants_types(self):
        """Test types of global constants."""
        assert isinstance(root.PACKAGE, root.Package)
        assert isinstance(root.MODULE, root.Module)
        assert isinstance(root.SUB_PACKAGE, root.SubPackage)
        assert isinstance(root.META_MODULE, root.MetaModule)
        assert isinstance(root.MODEL, root.Model)
        assert isinstance(root.FOSSIL, root.FossilCommand)
        assert isinstance(root.UTIL_MODULE, root.UtilModule)
