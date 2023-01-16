
"""Contains: MainView."""

from interface import Interface


class MainView(Interface):
    """Interface for Main and MainPresenter."""

    def will_roll(self, current_turn_score):
        """Return boolean, true if player wishes to continue rolling."""
        pass

    def print_roll_stats(self, player, turntotal, rollednum):
        """
        Consume the param, likely printing it to screen.

        @ param player is the current player and of type Player
        @ param rollednum is of type int
        """
        pass
