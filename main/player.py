
"""Contains: Player class."""


class Player:
    """
    Holds player attributes: names, total score and total rolls_made.

    The constructor's player_id param is an Enum of type PlayerObj's, P1 or P2,
    from which a 'Player1' or 'Player2' name value is derived.
    """

    # Global variables
    COMPUTER_NAME = "Computer"

    def __init__(self, player_id):
        """Initialise values."""
        self.player_id = player_id
        self.name = player_id.name
        self.score = 0
        self.rolls_made = 0
        self.set_computer(False)

    def is_computer(self):
        """Getter the current state of computer, true or false."""
        return self.m_is_computer

    def set_computer(self, value):
        """
        Assign the boolean, value, to is_computer_state.

        Set name to self.COMPUTER_NAME if value is true.
        """
        self.m_is_computer = value
        if value:
            self.name = self.COMPUTER_NAME

    def get_score(self):
        """Get the current score."""
        return self.score

    def add_score(self, score):
        """Add the value of the parameter to score."""
        self.score += score

    def get_rolls_made(self):
        """Get the current rolls made."""
        return self.rolls_made

    def add_rolls_made(self, rolls_made):
        """Add the current value of rolls to the attribute."""
        self.rolls_made += rolls_made

    def set_name(self, name):
        """
        Assign name parameter to the instance attribute.

        Enforces name as 'Computer' if the instances is_computer is True.
        """
        self.name = self.COMPUTER_NAME if self.m_is_computer else name

    def get_name(self):
        """Get the current name."""
        return self.name

    def get_id(self):
        """Return the player id."""
        return self.player_id

    def reset_stats(self):
        """Reset the values of score and rolls made to 0."""
        self.score = 0
        self.rolls_made = 0

    def _set_score(self, score):
        """Intended for test purposes only!."""
        self.score = score
