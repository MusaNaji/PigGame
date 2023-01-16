#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Unit testing."""

import unittest
from pig.main.player import Player
from pig.main.enums_module import FirstMover


class TestPlayerClass(unittest.TestCase):
    """Test the classes."""

    @classmethod
    def setUpClass(cls):
        """Set up class variable."""
        cls.test_integer = 10

    def setUp(self):
        """Set up test cases."""
        self.a_player = Player(FirstMover.P1)

    def test_init_default_object(self):
        """Instantiate an object and check its properties."""
        self.assertIsInstance(self.a_player, Player)

    def test__is_computer__is_default_false(self):
        """Testing false if its computer."""
        self.assertFalse(self.a_player.is_computer())

    def test__set_is_computer__True(self):
        """Name is 'computer' when value is set to True."""
        self.a_player.set_computer(True)
        self.assertTrue(self.a_player.is_computer())

        # test default name is correct
        self.assertEqual(Player.COMPUTER_NAME, self.a_player.get_name())

    def test__set_is_computer__False(self):
        """Name is set to 'Player2' (or 'Player1') when value is False."""
        player = Player(FirstMover.P2)
        player.set_computer(False)
        self.assertFalse(self.a_player.is_computer())

        # test default name is correct
        self.assertEqual(FirstMover.P2.name, player.get_name())

    def test__set_name__equals__get_name(self):
        """Testing if set name is equal to get name."""
        self.a_player.set_name("name")
        self.assertEqual(self.a_player.get_name(), "name")

    def test__add_score__correct_sum(self):
        """Calling get_score() returns the sum of all added scores."""
        expected = 2 * self.test_integer
        self.a_player.add_score(self.test_integer)
        self.a_player.add_score(self.test_integer)
        self.assertEqual(expected, self.a_player.get_score())

    def test__add_rolls_made(self):
        """Calling get_rolls_made returns the sum of all added rolls_made."""
        expected = 2 * self.test_integer
        self.a_player.add_rolls_made(self.test_integer)
        self.a_player.add_rolls_made(self.test_integer)
        self.assertEqual(expected, self.a_player.get_rolls_made())

    def test__reset_stats(self):
        """Testing resetting the stats to 0."""
        self.a_player.add_score(12)
        self.a_player.add_score(3)
        self.assertEqual(15, self.a_player.get_score())

        self.a_player.add_rolls_made(6)
        self.a_player.add_rolls_made(6)
        self.assertEqual(12, self.a_player.get_rolls_made())

        expected = 0

        # Test after setup player attributes diverge
        self.assertNotEqual(expected, self.a_player.get_score())
        self.assertNotEqual(expected, self.a_player.get_rolls_made())

        # Assert that reset reassigns '0' to score and rolls_made
        self.a_player.reset_stats()
        self.assertEqual(expected, self.a_player.get_score())
        self.assertEqual(expected, self.a_player.get_rolls_made())


if __name__ == '__main__':
    unittest.main()
