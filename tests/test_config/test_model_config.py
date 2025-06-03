import pytest
from typing import NamedTuple

from quarryforge.config import model_config

from tests.test_config.test_root import get_namedtuple_fields


class TestModelConfig:
    """Tests for quarryforge.config.model_config"""

    def test_module_dunder_all(self):
        """Test the __all__ variable."""
        expected_all = ['FOSSIL_REPO', 'FOSSIL_COMMIT', 'FOSSIL_TIMELINE']
        assert sorted(model_config.__all__) == sorted(expected_all)

    def test_config_fossil_repo_attributes_and_method(self):
        """Test attributes and method of ConfigFossilRepo."""
        cfg = model_config.FOSSIL_REPO
        assert isinstance(cfg, model_config.ConfigFossilRepo)

        assert cfg.file == '_file'
        assert cfg.field_name() == 'file'

        expected_fields = ['file']
        assert sorted(get_namedtuple_fields(model_config.ConfigFossilRepo)) == sorted(expected_fields)


    def test_config_fossil_commit_attributes(self):
        """Test attributes of ConfigFossilCommit."""
        cfg = model_config.FOSSIL_COMMIT
        assert isinstance(cfg, model_config.ConfigFossilCommit)

        assert cfg.uuid == 'uuid'
        assert cfg.date == 'date'
        assert cfg.author == 'author'
        assert cfg.comment == 'comment'
        assert cfg.branch == 'branch'
        assert cfg.tags == 'tags'
        assert cfg.phase == 'phase'
        assert cfg.changes == 'changes'

        expected_fields = [
            'uuid', 'date', 'author', 'comment', 'branch', 'tags', 'phase', 'changes'
        ]
        assert sorted(get_namedtuple_fields(model_config.ConfigFossilCommit)) == sorted(expected_fields)

    def test_config_fossil_timeline_attributes(self):
        """Test attributes of ConfigFossilTimeline."""
        cfg = model_config.FOSSIL_TIMELINE
        assert isinstance(cfg, model_config.ConfigFossilTimeline)

        assert cfg.commits == 'commits'

        expected_fields = ['commits']
        assert sorted(get_namedtuple_fields(model_config.ConfigFossilTimeline)) == sorted(expected_fields)


    def test_global_constants_types(self):
        """Test types of global constants."""
        assert isinstance(model_config.FOSSIL_REPO, model_config.ConfigFossilRepo)
        assert isinstance(model_config.FOSSIL_COMMIT, model_config.ConfigFossilCommit)
        assert isinstance(model_config.FOSSIL_TIMELINE, model_config.ConfigFossilTimeline)
