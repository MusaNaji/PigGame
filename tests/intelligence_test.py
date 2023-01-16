
"""
Test class.

Author: Musa Naji.
"""

# Import unittest.
import unittest
# Import difficulty class from enums module.
from pig.main.enums_module import Difficulty
# Import Intelligence class.
from pig.main.intelligence import Intelligence


class TestIntelligence(unittest.TestCase):
    """Testing intelligence class."""

    def test__init(self):
        """Diffculty variable is an instance of the class Diffculty."""
        difficulty = Difficulty.HIGH
        # Test if the intelligence1 is an instance of the class intellgence.
        self.assertIsInstance(difficulty, Difficulty)

    def test__will_roll_impl__high(self):
        """Return true if difficuly is HIGH and score < 20, otherwise false."""
        # Init the difficulty level as high.
        diff_high = Difficulty.HIGH
        # Create an object of intelligence with high level of difficulty.
        intel = Intelligence(diff_high)
        truescore, falsescore = intel._get_willroll_test_limits()

        self.assertTrue(intel._will_roll_impl(truescore))
        self.assertFalse(intel._will_roll_impl(falsescore))

    def test__will_roll_impl__mid(self):
        """Return true if difficuly is MID and score < 32, otherwise false."""
        # Init the difficulty level as mid.
        diff_mid = Difficulty.MID
        # Create an object of intelligence with mid level of difficulty.
        intel = Intelligence(diff_mid)
        truescore, falsescore = intel._get_willroll_test_limits()

        self.assertTrue(intel._will_roll_impl(truescore))
        self.assertFalse(intel._will_roll_impl(falsescore))

    def test__will_roll_impl__low(self):
        """Return true if difficuly is LOW and score < 48, otherwise false."""
        # Init the difficulty level as low.
        diff_low = Difficulty.LOW
        # Create an object of intelligence with low level of difficulty.
        intel = Intelligence(diff_low)
        truescore, falsescore = intel._get_willroll_test_limits()

        self.assertTrue(intel._will_roll_impl(truescore))
        self.assertFalse(intel._will_roll_impl(falsescore))

    def test__random_play__high(self):
        """
        Return true if HIGH difficulty and random number is in range.

        The range is determined by START and END limits.
        """
        # Create an object of intelligence with high intelligence.
        intel = Intelligence(Difficulty.HIGH)
        # Set random END
        intel._set_end(intel.HIGH_MAX)
        # Assert true if the return value from andom_play() is true.
        self.assertTrue(intel._random_play())

        # Set random START and END out of range.
        intel._set_start(intel.HIGH_MAX + 1)
        intel._set_end(intel.HIGH_MAX + 3)
        self.assertFalse(intel._random_play())

    def test__random_play__mid(self):
        """
        Return true if MID difficulty and random number is in range.

        The range is determined by START and END limits.
        """
        # Create an object of intelligence with MID intelligence.
        intel = Intelligence(Difficulty.MID)
        # Set random END.
        intel._set_end(intel.MID_MAX)
        # Assert true if the return value from andom_play() is true.
        self.assertTrue(intel._random_play())

        # Set random START and END out of range.
        intel._set_start(intel.MID_MAX + 1)
        intel._set_end(intel.MID_MAX + 3)
        self.assertFalse(intel._random_play())

    def test__random_play__low(self):
        """
        Return true if LOW difficulty and random number is in range.

        The range is determined by START and END limits.
        """
        # Create an object of intelligence with low intelligence.
        intel = Intelligence(Difficulty.LOW)
        # Set random END.
        intel._set_end(intel.LOW_MAX)
        # Assert true if the return value from andom_play() is true.
        self.assertTrue(intel._random_play())

        # Set random START and END out of range.
        intel._set_start(intel.LOW_MAX + 1)
        intel._set_end(intel.LOW_MAX + 3)
        self.assertFalse(intel._random_play())


if __name__ == '__main__':
    unittest.main()
