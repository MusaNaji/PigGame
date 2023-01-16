
"""Contains: MockMainViewImpl, TestMainPresenter."""

import unittest
import random
from pig.main.mainpresenter import MainPresenter
from pig.main.interfaces import mainview
from interface import implements
from pig.main.enums_module import FirstMover
from pig.main.enums_module import PlayerObj
from pig.main.fileops import FileOps


class MockMainViewImpl(implements(mainview.MainView)):
    """Mock object to depict a class implementing MainView."""

    def __init__(self):
        """Initialise values."""
        self.count = -1
        random.seed()

    def will_roll(self, current_turn_score):
        """
        @ Override Provides control values to test MainPresenter side-effects.

        Also indirectly verifies that will_roll is not called back
        from caller after false is returned.
        """
        self.count += 1
        if self.count < 3:
            return True
        elif self.count == 3:
            return False
        else:
            raise ValueError("Value should not reach " + self.count)

    def print_roll_stats(self, player, turntotal, rollednum):
        """ignore."""
        pass


class TestMainPresenter(unittest.TestCase):
    """Verify that seperation of concern elements do not introduce bugs."""

    def setUp(self):
        """Set up test cases."""
        mock_main = MockMainViewImpl()
        self.presenter = MainPresenter(mock_main)

    def test__assign_first_mover__random(self):
        """After call to assign_first_mover(RAND), currentplayer is nonnull."""
        # Confirm initial currentplayer state is null
        self.assertIsNone(self.presenter.get_current_player())

        # Assign FirstMover randomly
        currentplayer = self.presenter.assign_first_mover(FirstMover.RAND)
        self.assertIsNotNone(currentplayer)

    def test__assign_first_mover__P1(self):
        """Correctly sets player1 as currentplayer."""
        # Enforce P1 as FirstMover
        currentplayer = self.presenter.assign_first_mover(FirstMover.P1)
        self.assertEqual(PlayerObj.P1, currentplayer.get_id())

    def test__assign_first_mover__P2(self):
        """Correctly sets player2 as currentplayer."""
        # Enforce P2 as FirstMover
        currentplayer = self.presenter.assign_first_mover(FirstMover.P2)
        self.assertEqual(PlayerObj.P2, currentplayer.get_id())

    def test__manage_turn__play_till_no_roll(self):
        """Play until false is returbed, tests score and rolls_made."""
        # Restrict the die roll to 2
        self.presenter._MainPresenter__set_start_face(2)
        self.presenter._MainPresenter__set_end_face(2)
        score, rolls_made = self.presenter.manage_turn()

        # Assert score
        self.assertEqual(6, score)
        # Assert rolls_made
        self.assertEqual(3, rolls_made)

    def test__manage_turn__stop_when_1_rolled(self):
        """Return score = '0' after '1' is rolled."""
        # Restrict the die roll to 0
        self.presenter._MainPresenter__set_start_face(1)
        self.presenter._MainPresenter__set_end_face(1)
        score, rolls_made = self.presenter.manage_turn()

        # Assert score
        self.assertEqual(0, score)
        # Assert rolls_made
        self.assertEqual(1, rolls_made)

    def test__manage_turn__ValueError(self):
        """Raise ValueError if dice value is not between 1 - 6 (inclusive)."""
        # Set the dice out of range
        self.presenter._MainPresenter__set_start_face(7)
        self.presenter._MainPresenter__set_end_face(10)
        with self.assertRaises(ValueError):
            self.presenter.manage_turn()

    def test__toggle_current__betweenP1andP2(self):
        """Assert a few toggles of currentplayer."""
        # Initialise currentplayer directly, to avoid side-effects, instead
        #  of calling assign_first_mover()
        self.presenter.current_player = self.presenter.player1
        self.assertEqual(self.presenter.current_player, self.presenter.player1)

        # toggle and assert currentplayer == player2 == result
        result = self.presenter.toggle_current_player()
        self.assertEqual(self.presenter.player2, result)
        result = self.presenter.current_player
        # Diversify the test for the same result
        self.assertNotEqual(self.presenter.player1, result)

        # Toggle again, for Good Luck...
        # Check successfully toggles back to currentplayer == player1 == result
        result = self.presenter.toggle_current_player()
        # Diversify the test for the same result
        self.assertNotEqual(self.presenter.player2, result)
        result = self.presenter.current_player
        self.assertEqual(self.presenter.player1, result)

    def test__toggle_current_player__NotImplementedError(self):
        """Raise NotImplementedError, if currentplayer is None."""
        # Toggle currentplayer without first calling assign_first_mover()
        with self.assertRaises(NotImplementedError):
            self.presenter.toggle_current_player()

    def test__apply_single_player_setting__False(self):
        """
        Validate single player attributes are correctly set.

        Player2's is_computer is set to False, and value returned, when
        called and DataKey.MODE, a key in settings_dict, has value TWO.
        """
        # Default key, value is  DataKey.MODE.name, TWO
        self.presenter._settings_dict = FileOps.default_setting_dict
        flag = self.presenter.apply_single_player_setting()
        self.assertFalse(flag)

    def test__parse_cheat_test_scores__no_keyword_or_no_params(self):
        """Return '0' if 'test' keyword is used incorrectly."""
        # Incorrect keyword, i.e. keyword != 'test'
        p1score, p2score = self.presenter._parse_cheat_test_scores('bad_kword')
        self.assertTrue(p1score == 0 and p2score == 0)

        # Keyword used, but with omitted values.
        p1score, p2score = self.presenter._parse_cheat_test_scores('test')
        self.assertTrue(p1score == 0 and p2score == 0)

    def test__parse_cheat_test_scores__keyword_with_params(self):
        """Return cheat scores for P1 (and P2), if test keyword used."""
        p1score, p2score = self.presenter._parse_cheat_test_scores('test 78')
        # Only P1 value intelligible
        self.assertEqual(p1score, 78)
        self.assertEqual(p2score, 0)

        # Both values intelligible
        p1score, p2score = \
            self.presenter._parse_cheat_test_scores('test 78 98')
        self.assertEqual(p1score, 78)
        self.assertEqual(p2score, 98)


if __name__ == '__main__':
    unittest.main()
