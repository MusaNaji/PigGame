
"""Contains: TestHighscore."""

import unittest
from pig.main.highscore import Highscore


class TestHighscore(unittest.TestCase):
    """Test cases for Highscore methods with consequential side effects."""

    def setUp(self):
        """Testcases setup."""
        self.hs = Highscore()
        self.test_dict = {
            1: 'James#123',
            2: 'Anna#145',
            3: 'Boris#117'
        }

    def test_init_state(self):
        """Verify init state."""
        self.assertEqual(self.hs.get_dict(), dict())

    def test__get_dict__set_dict(self):
        """Get returns set value."""
        self.hs.set_dict(self.test_dict)
        self.assertEqual(self.test_dict, self.hs.get_dict())

    def test__tuplelist_to_numkeys_dict(self):
        """
        Parse the contents of a tuplelist into a dictionary as its value.

        Passing a tuple list returns a dict containing auto-incremented
        numerical values as key, starting from 1; and situates each tuple
        element as a value of the dict.
        """
        tuplelist = [('James', 123), ('Anna', 145), ('Boris', 117)]
        actual = self.hs._tuplelist_to_numkeys_dict(tuplelist)
        self.assertEqual(self.test_dict, actual)

    def test__sort_func(self):
        """Return int value, or Exceptions are raised when invalid data."""
        # A one element tuple is considered the type
        # contained in it, and will thus raise a ValueError too.
        expected = 121
        self.assertEqual(expected, self.hs._sort_func(('James', expected)))

        with self.assertRaises(ValueError):
            self.hs._sort_func(('James'))
        with self.assertRaises(ValueError):
            self.hs._sort_func(('James', 'James'))

    def test_vet_new_highscore(self):
        """
        Generate highscore tuplelist contains max of 5 elements.

        The elements are to be sorted in descending order of score.
        """
        # Setup - three more values to test_dict to bring its len to 6
        self.test_dict[4] = 'Issac#141'
        self.test_dict[5] = 'Joen#127'
        self.test_dict[6] = 'Mary#109'
        # Pass a newname, newscore along with the current dict state
        tuplelist = self.hs._vet_new_highscore(self.test_dict, 'Zoey', 116)

        # Return list contains only 5 elements
        self.assertEqual(5, len(tuplelist))

        # Each tuple element is in the right position according to score
        flag = tuplelist[0][1] >= tuplelist[1][1] and \
            tuplelist[1][1] >= tuplelist[2][1] and \
            tuplelist[2][1] >= tuplelist[3][1] and \
            tuplelist[3][1] >= tuplelist[4][1]
        self.assertTrue(flag)

    def test__revise_highscore__dict_unchanged(self):
        """
        Dictionary is not revised if revision conditions are not met.

        If score is not >= 100, or if score is not greater than any of the
        current scores in dict, dict remains unchanged.
        """
        # setUp
        self.hs._highscores_dict = self.test_dict.copy()

        self.hs.revise_highscore('testname', 99)
        self.assertEqual(self.test_dict, self.hs._highscores_dict)

        # Setup Adding a score lower than current 5 score: Add 2 more values to
        #  self.test_dict, recognising that the min score is Boris = 117
        #   - this brings dict len to 5
        self.test_dict[4] = 'Issac#141'
        self.test_dict[5] = 'Joen#127'
        # Try to add a score of 100
        self.hs.revise_highscore('testname', 100)
        flag = True
        for namescore in self.hs._highscores_dict.values():
            flag += namescore in ['Issac#141', 'Joen#127', 'James#123',
                                  'Anna#145', 'Boris#117']
        self.assertTrue(flag)

    def test__revise_highscore__dict_changed(self):
        """Add if score is >= 100 in a dictionary less than len 5."""
        # setUp
        self.hs._highscores_dict = self.test_dict.copy()

        self.hs.revise_highscore('testname', 100)
        self.assertNotEqual(self.test_dict, self.hs._highscores_dict)


if __name__ == '__main__':
    unittest.main()
