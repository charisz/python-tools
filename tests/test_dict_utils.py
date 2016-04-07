import unittest
from voidpp_tools.dict_utils import recursive_update

class TestDictUtils(unittest.TestCase):

    def test_recursive_update_simple(self):
        # Arrange
        target = dict(key1 = 42, key2 = dict(key21 = 10.5))
        source = dict(key2 = dict(key22 = 21))

        # Act
        recursive_update(target, source)

        # Assert
        self.assertDictEqual(target, dict(key1 = 42, key2 = dict(key21 = 10.5, key22 = 21)))

    def test_recursive_update_with_source_type_mismatch(self):
        # Arrange
        target = dict(key1 = 42, key2 = dict(key21 = 10.5))
        source = dict(key2 = 84)

        # Act
        recursive_update(target, source)

        # Assert
        self.assertDictEqual(target, dict(key1 = 42, key2 = 84))

    def test_recursive_update_with_target_type_mismatch(self):
        # Arrange
        target = dict(key1 = 42, key2 = 84)
        source = dict(key2 = dict(key21 = 10.5))

        # Act
        recursive_update(target, source)

        # Assert
        self.assertDictEqual(target, dict(key1 = 42, key2 = dict(key21 = 10.5)))

    def test_recursive_update_extend_lists(self):
        # Arrange
        target = dict(key1 = 42, key2 = dict(key21 = [1, 2]))
        source = dict(key2 = dict(key21 = [3]))

        # Act
        recursive_update(target, source)

        # Assert
        self.assertDictEqual(target, dict(key1 = 42, key2 = dict(key21 = [1,2,3])))

    def test_recursive_update_extend_lists_with_source_type_mismatch(self):
        # Arrange
        target = dict(key1 = 42, key2 = dict(key21 = [1, 2]))
        source = dict(key2 = dict(key21 = 84))

        # Act
        recursive_update(target, source)

        # Assert
        self.assertDictEqual(target, dict(key1 = 42, key2 = dict(key21 = 84)))

    def test_recursive_update_extend_lists_with_target_type_mismatch(self):
        # Arrange
        target = dict(key1 = 42, key2 = dict(key21 = 84))
        source = dict(key2 = dict(key21 = [1]))

        # Act
        recursive_update(target, source)

        # Assert
        self.assertDictEqual(target, dict(key1 = 42, key2 = dict(key21 = [1])))

    def test_recursive_update_create_list(self):
        # Arrange
        target = dict(key1 = 42, key2 = dict(key21 = 21))
        source = dict(key2 = dict(key22 = [3]))

        # Act
        recursive_update(target, source)

        # Assert
        self.assertDictEqual(target, dict(key1 = 42, key2 = dict(key21 = 21, key22 = [3])))
