#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Unit testing."""

import unittest
from pig.main import dice


class TestDiceClass(unittest.TestCase):
    """Test the class."""

    def test__init_default_object(self):
        """Instantiate an object and check its properties."""
        die = dice.Dice()
        self.assertIsInstance(die, dice.Dice)

        result = die.end_face
        expected = 6
        self.assertEqual(result, expected)

    def test__roll_a_dice(self):
        """Roll a dice and check value is in bounds."""
        die = dice.Dice()

        result = die.roll()
        expected = 1 <= result <= die.end_face
        self.assertTrue(expected)

    def test__get_rolls_made(self):
        """Roll dice twice and then check return value == 2."""
        # Create an instance of dice,
        die = dice.Dice()
        # Roll twice
        die.roll()
        die.roll()
        # Check the return value
        result = die.get_rolls_made()
        expected = 2
        self.assertEqual(result, expected)

    def test__reset_rolls_count(self):
        """Call reset_rolls and check if expected value == 0."""
        die = dice.Dice()
        # Roll twice
        die.roll()
        die.roll()
        # Check the return value
        expected = 0
        die.reset_rolls_count()
        self.assertEqual(expected, die.get_rolls_made())

    def test__set_start_face(self):
        """Call set_start_face and check if expected value(1)."""
        die = dice.Dice()
        die._Dice__set_start_face(1)
        self.assertEqual(1, die._Dice__get_start_face())

    def test__set_end_face(self):
        """Call set_end_face and check if expected value(6)."""
        die = dice.Dice()
        die._Dice__set_end_face(6)
        self.assertEqual(6, die._Dice__get_end_face())


if __name__ == '__main__':
    unittest.main()
