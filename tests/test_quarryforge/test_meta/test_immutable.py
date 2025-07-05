"""Unit tests for the quarryforge.meta.immutable module.

This suite provides comprehensive coverage for the immutability enforcement
classes: ImmutableMetaClass, Namespace, and ImmutableInstance.
"""

import logging

import pytest

from quarryforge.meta import immutable


class TestImmutableMetaClass:
    """Test the ImmutableMetaClass for class-level immutability."""

    def test_class_attribute_immutability(self):
        """Verify that class attributes cannot be set or deleted."""
        logging.info(
            'Testing ImmutableMetaClass: preventing attribute '
            'setting/deletion.'
        )

        class DummyImmutableClass(metaclass=immutable.ImmutableMetaClass):
            X = 5

        assert DummyImmutableClass.X == 5

        with pytest.raises(AttributeError, match='Immutable'):
            DummyImmutableClass.X = 10

        with pytest.raises(AttributeError, match='Immutable'):
            del DummyImmutableClass.X


class TestNamespace:
    """Tests the Namespace metaclass for uninstantiable, immutable namespaces."""

    def test_class_is_uninstantiable(self):
        """Verify that classes using Namespace cannot be instantiated."""
        logging.info(
            'Testing Namespace: ensuring class is uninstantiable.'
        )

        class UninstantiableNamespace(metaclass=immutable.Namespace):
            CONSTANT = 'value'

        with pytest.raises(TypeError, match='Class has no instances.'):
            UninstantiableNamespace()

    def test_class_is_immutable(self):
        """Verify that Namespace inherits class-level immutability."""
        logging.info('Testing Namespace: verifying inherited immutability.')

        class UninstantiableNamespace(metaclass=immutable.Namespace):
            CONSTANT = 'value'

        assert UninstantiableNamespace.CONSTANT == 'value'

        with pytest.raises(AttributeError, match='Immutable'):
            UninstantiableNamespace.CONSTANT = 'new_value'

        with pytest.raises(AttributeError, match='Immutable'):
            del UninstantiableNamespace.CONSTANT

    def test_slots_are_set(self):
        """Verify that __slots__ is set to an empty tuple."""
        logging.info('Testing Namespace: confirming __slots__ is set.')

        class UninstantiableNamespace(metaclass=immutable.Namespace):
            pass

        assert hasattr(UninstantiableNamespace, '__slots__')
        assert UninstantiableNamespace.__slots__ == ()


class TestImmutableInstance:
    """Tests the ImmutableInstance mixin for instance-level immutability."""

    @pytest.fixture
    def dummy_instance(self) -> 'DummyMutableClass':
        """Provide instance of a class that uses the ImmutableInstance mixin."""
        class DummyMutableClass(immutable.ImmutableInstance):
            __slots__ = ['x']
            def __init__(self, x_val: int):
                object.__setattr__(self, 'x', x_val)

        return DummyMutableClass(x_val=10)

    def test_instance_attribute_immutability(self, dummy_instance):
        """Verify that instance attributes cannot be set after initialization."""
        logging.info('Testing ImmutableInstance: preventing attribute setting.')
        with pytest.raises(TypeError, match='Immutable'):
            dummy_instance.x = 20

    def test_instance_attribute_deletion_immutability(self, dummy_instance):
        """Verify that instance attributes cannot be deleted."""
        logging.info(
            'Testing ImmutableInstance: preventing attribute deletion.'
        )
        with pytest.raises(TypeError, match='Immutable'):
            del dummy_instance.x

    def test_init_and_read_attributes(self, dummy_instance):
        """Functional test to ensure initialization and reading are unaffected."""
        logging.info(
            'Testing ImmutableInstance: verifying read access is allowed.'
        )
        assert dummy_instance.x == 10
