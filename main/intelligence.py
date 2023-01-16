
"""
Class to control the computer player intelligence levels.

Author: Musa Naji
"""

# Import random class.
import random
# Import difficulty class from enums module.
from pig.main.enums_module import Difficulty


class Intelligence():
    """Class to creat an intelligence object."""

    # Average between 2-6.
    AVG = 4
    # The ratio limit for high difficulty.
    RATIO_LIMIT_HIGH = 5
    # The ratio limit for mid difficulty.
    RATIO_LIMIT_MID = 4
    # The ratio limit for low level difficulty.
    RATIO_LIMIT_LOW = 3

    # All time max random play allowed.
    start = 1
    end = 10
    # High level max random play times allowd out of end
    HIGH_MAX = 3
    # Mid level max random play times allowd ou of end
    MID_MAX = 4
    # Low level max random play times allowd out of end
    LOW_MAX = 6

    def __init__(self, difficulty):
        """Set difficulty Enum and odd_ratio."""
        self.difficulty = difficulty
        self.odd_ratio = 0

    def will_roll(self, score):
        """Return true or false as an indicator of whether to roll or not."""
        return self._will_roll_impl(score) or self._random_play()

    def _will_roll_impl(self, score):
        """Return true or false based on calculated oddratio and difficulty."""
        # Calculate the odd ratio according to current score and the AVG(4)
        self.odd_ratio = score / self.AVG

        if self.difficulty == Difficulty.HIGH:
            # Return turn in HIGH diff if score is 90+ (i.e. in range of 100)
            return (self.odd_ratio < self.RATIO_LIMIT_HIGH) or (score >= 90)
        elif self.difficulty == Difficulty.MID:
            return self.odd_ratio < self.RATIO_LIMIT_MID
        return self.odd_ratio < self.RATIO_LIMIT_LOW

    def _random_play(self):
        """
        Randomising will_roll decision further.

        Based on random_value and difficulty value and return True or False
        based on that.
        """
        # All time min times random play allowed.
        # Random values (1,10) for random play allowed.
        random_value = random.randint(self.start, self.end)

        if self.difficulty == Difficulty.HIGH:
            return self.start <= random_value <= self.HIGH_MAX
        elif self.difficulty == Difficulty.MID:
            return self.start <= random_value <= self.MID_MAX
        return self.start <= random_value <= self.LOW_MAX

    def _set_start(self, start):
        """Private method to set the max random play allowed for each level."""
        self.start = start

    def _set_end(self, end):
        """Private method to set the max random play allowed for each level."""
        self.end = end

    def _get_willroll_test_limits(self):
        """
        Calculate testscore ceiling and returns two values from it.

        The first, satisfies a True condition for _will_roll_impl and the
        second a False. For example:
        testscore =  RATIO_LIMIT * AVG, subtract 1 to meet lower limit
        E.g. for HIGH, RATIO_LIMIT = 5, ceiling = 5 * AVG = 5 * 4 = 20
        """
        ceiling = ceiling = self.RATIO_LIMIT_LOW * self.AVG
        if self.difficulty == Difficulty.HIGH:
            ceiling = self.RATIO_LIMIT_HIGH * self.AVG
        elif self.difficulty == Difficulty.MID:
            ceiling = self.RATIO_LIMIT_MID * self.AVG
        return ceiling - 1, ceiling
