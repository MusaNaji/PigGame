#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module is a derivate of Mikael Roos', our lecturer, class example."""

import random


class Dice():
    """
    Dice class with a reset_rolls method for rolls taken.

    The reset function allows the same object to reused.
    """

    end_face = 6

    def __init__(self):
        """Initialise values."""
        random.seed()
        self.start_face = 1
        self.rolls_made = 0

    def roll(self):
        """Roll a dice once and return the value."""
        self.rolls_made += 1
        return random.randint(self.start_face, self.end_face)

    def get_rolls_made(self):
        """Get number of rolls made."""
        return self.rolls_made

    def reset_rolls_count(self):
        """Reset number of rolls made to 0."""
        self.rolls_made = 0

    def __set_start_face(self, value):
        # Private class intended for unittesting only.
        self.start_face = value

    def __set_end_face(self, value):
        # Private class intended for unittesting only.
        self.end_face = value

    def __get_start_face(self):
        # Private class intended for unittesting only.
        return self.start_face

    def __get_end_face(self):
        # Private class intended for unittesting only.
        return self.end_face
