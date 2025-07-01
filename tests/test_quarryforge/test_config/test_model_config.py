from quarryforge.config import model_config


class TestModelConfig:
    """Tests for quarryforge.config.model_config"""

    def test_module_dunder_all(self):
        """Test the __all__ variable."""
        expected_all = [
            'fossil_repo_config',
            'fossil_commit_config',
            'fossil_timeline_config',
            'validation_config',
        ]
        assert sorted(model_config.__all__) == sorted(expected_all)

    def test_fossil_repo_config(self):
        """Test attributes and methods of ConfigFossilRepo."""
        cfg = model_config.fossil_repo_config()
        assert isinstance(cfg, model_config.ConfigFossilRepo)
        assert cfg.file == '_file'
        assert cfg.is_new == '_is_new'
        assert cfg.workdir == '_workdir'
        assert sorted(cfg._fields) == sorted(['file', 'is_new', 'workdir'])
        assert cfg.slots() == ('_file', '_is_new', '_workdir')

    def test_config_fossil_commit_attributes(self):
        """Test attributes of ConfigFossilCommit."""
        cfg = model_config.fossil_commit_config()
        assert isinstance(cfg, model_config.ConfigFossilCommit)

        assert cfg.uuid == '_uuid'
        assert cfg.date == '_date'
        assert cfg.author == '_author'
        assert cfg.comment == '_comment'
        assert cfg.branch == '_branch'
        assert cfg.tags == '_tags'
        assert cfg.phase == '_phase'
        assert cfg.changes == '_changes'

        expected_fields = [
            'uuid',
            'date',
            'author',
            'comment',
            'branch',
            'tags',
            'phase',
            'changes',
        ]
        assert sorted(cfg._fields) == sorted(expected_fields)

        expected_slots = (
            '_uuid',
            '_date',
            '_author',
            '_comment',
            '_branch',
            '_tags',
            '_phase',
            '_changes',
        )
        assert cfg.slots() == expected_slots

    def test_config_fossil_timeline_attributes(self):
        """Test attributes of ConfigFossilTimeline."""
        cfg = model_config.fossil_timeline_config()
        assert isinstance(cfg, model_config.ConfigFossilTimeline)

        assert cfg.commits == 'commits'

        expected_fields = ['commits']
        assert sorted(cfg._fields) == sorted(expected_fields)

    def test_config_functions_return_types(self):
        """Test the return types of the configuration factory functions."""
        assert isinstance(
            model_config.fossil_repo_config(), model_config.ConfigFossilRepo
        )
        assert isinstance(
            model_config.fossil_commit_config(), model_config.ConfigFossilCommit
        )
        assert isinstance(
            model_config.fossil_timeline_config(),
            model_config.ConfigFossilTimeline,
        )

    def test_validation_config(self):
        """Test attributes of ConfigValidation."""
        cfg = model_config.validation_config()
        assert isinstance(cfg, model_config.ConfigValidation)
        assert cfg.PAIR == 2
        assert cfg.KEY == 0
        assert cfg.VALUE == 1
