
"""Unit testing."""

import unittest
from pig.main import enums_module


class TestEnumModule(unittest.TestCase):
    """Test the class."""

    def test_play_mode_enum_object(self):
        """Instantiate an object and check its properties."""
        play_mode = enums_module.PlayMode.ONE_PLAYER

        self.assertIsInstance(play_mode, enums_module.PlayMode)

        actual = play_mode.value
        expected = 'one'
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
