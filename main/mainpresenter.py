
"""Contains: MainPresenter."""

import random
from pig.main.dice import Dice
from pig.main.player import Player
from pig.main.fileops import FileOps
from pig.main.intelligence import Intelligence
from pig.main.enums_module import PlayMode
from pig.main.enums_module import PlayerObj
from pig.main.enums_module import FirstMover
from pig.main.enums_module import Difficulty
from pig.main.enums_module import DataKey
from pig.main.enums_module import FileMode
from pig.main.highscore import Highscore


class MainPresenter:
    """
    Presenter helper class for Plain old Python methods.

    Class takes a MainView implementing object and assigns it locally.
    """

    RULES = """
    The objective of the game is to be the first player to reach 100 points,

    however, highscores are allocated based on the highest scores over 100.

      - If during a turn a player rolls a value other than 1, it
        is added to turn total and rolling may continue.

      - If a player rolls 1 during a turn, no points are awarded and
         the turn toggled to the opponent player.

      - If a player holds, the sum of dice rolls during that turn is
        added to their running total, and the turn toggled.

        """

    def __init__(self, main_view):
        """Initialise objects."""
        self.main_view = main_view
        self.die = Dice()
        self.current_player = None
        self.player1 = Player(PlayerObj.P1)
        self.player2 = Player(PlayerObj.P2)
        self.fileops = FileOps()
        self.intel = None
        self.force_exit = False
        # Dictionarys
        self._settings_dict = dict()
        self._highscore = Highscore()

    def assign_first_mover(self, mover: FirstMover):
        """Determine, assign and return FirstMover."""
        if mover == FirstMover.RAND:
            self.current_player = random.choice([self.player1, self.player2])
        elif mover == FirstMover.P1:
            self.current_player = self.player1
        else:
            self.current_player = self.player2
        return self.current_player

    def manage_turn(self):
        """
        Manage a turn and the decision as to whether a player wishes to roll.

        After a roll, if '1' is not rolled, roll decision is posed again. If a
        player decides to stop rolling, a pair of values, tallied score and
        rolls_made are returned to caller.

        If '1' is rolled, zero is returned for score along with rolls_made.
        """
        # current_player, Takes Player and Dice to aid testability.
        score = 0
        num = 0
        # Enforce 0 rolls_made at beginning of turn
        self.die.reset_rolls_count()
        while True:
            # Determine if computer AI wishes to roll, if 2 players mode
            # get value from current user on console. If false, break.
            # Also if num = 1, player rolled 1 at last itr, break
            # None will_roll indicates user wishes to exit before game end
            will_roll = self.main_view.will_roll(score)
            if not will_roll:
                break
            num = self.die.roll()
            # Add num to score if between 2 to 6 (inclusive)
            if num >= 2 and num <= 6:
                score += num
            # If a 1, assign 0 points and break so that turn is passed
            elif num == 1:
                score = 0
            else:
                raise ValueError("Die value is not within bound.")
            # Show value rolled in UI
            self.main_view.print_roll_stats(
                          self.current_player, str(score), str(num))
            if num == 1:
                break
        # Return turn statistics to caller
        return score, self.die.get_rolls_made()

    def toggle_current_player(self):
        """Toggles current player and returns new value."""
        if self.current_player is None:
            msg = """Variable, current_player, cannot be null. Initialise
            with call to assign_first_mover(mover)."""
            raise NotImplementedError(msg)
        elif self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
        return self.current_player

    def get_current_player(self):
        """Return the current player."""
        return self.current_player

    def update_currentplayer(self, turnscore, turnrolls):
        """Update the current player's score and rolls_made when turn ends."""
        self.current_player.add_score(turnscore)
        self.current_player.add_rolls_made(turnrolls)

    def update_player_name(self, player_id):
        """
        Update the Player name corresponding to the given Id with dict values.

        The dictionary value is as contained in settings dictionary, with
        player_id.name as key.
        @ param player_id is of type Player, either P1 or P2
        """
        player = self._get_player(player_id)
        if player is not None:
            player.set_name(self._settings_dict[player_id.name])

    def set_settings_dict(self, a_dict):
        """Adopt a copy of param a_dict as the new value of settings_dict."""
        self._settings_dict = a_dict.copy()

    def get_settings_dict(self):
        """Return a copy of the dictionary, not bound by reference."""
        return self._settings_dict.copy()

    def get_play_mode_and_diff(self):
        """Return current PlayMode and Difficulty values in setting_dict."""
        dic = self._settings_dict
        return dic[DataKey.MODE.name], dic[DataKey.DIFF.name]

    def update_setting(self, key, value):
        """Associates the value, if a valid dictionary key."""
        if key in DataKey.values_list():
            self._settings_dict[key] = value
            return True
        return False

    def apply_single_player_setting(self):
        """Flag player2 as Computer if in ONE_PLAYER mode."""
        mode = self._settings_dict[DataKey.MODE.name]
        flag = mode == PlayMode.ONE_PLAYER.value
        self.player2.set_computer(flag)
        # If flag is True, initialise an intelligence object with a Diffculty
        # Enum matching the current difficulty in settings_dict
        if flag:
            diff = Difficulty(self._settings_dict[DataKey.DIFF.name])
            self.intel = Intelligence(diff)
        return self.player2.is_computer()

    def init_high_score_data(self):
        """
        Create an empty highscore.txt if it does not exist, or read file.

        If the file exits, its content is read to to highscore dictionary.
        """
        ops = self.fileops
        file_obj = ops.get_file_object(Highscore.FILE_NAME, FileMode.READ)
        if file_obj is None:
            file_obj = ops.get_file_object(Highscore.FILE_NAME, FileMode.WRITE)
        else:
            hs_dict = ops.read_file_to_dict(file_obj)
            self.set_highscore_dict(hs_dict)
        ops.close_file_object(file_obj)

    def set_highscore_dict(self, a_dict):
        """Assign a_dict to highscore_dict."""
        self._highscore.set_dict(a_dict)

    def get_highscore_dict(self):
        """Return a copy of the dictionary, bound by reference."""
        return self._highscore.get_dict()

    def log_highscore(self, newname, newscore):
        """Register highscore from dictionary to highscore.txt file."""
        old_dict = self._highscore.get_dict().copy()
        new_dict = self._highscore.revise_highscore(newname, newscore)
        if old_dict == new_dict:
            return None
        fileops = self.fileops
        fobj = fileops.get_file_object(Highscore.FILE_NAME, FileMode.WRITE)
        # Returns true if no error encountered
        flag = fileops.write_dict_to_file(fobj, new_dict)
        fileops.close_file_object(fobj)
        return flag

    # Private test helper methods

    def _get_player(self, player_id):
        """Return the Player object corresponding with the given id."""
        if player_id == PlayerObj.P1:
            return self.player1
        elif player_id == PlayerObj.P2:
            return self.player2

    def __set_start_face(self, value):
        """Target at testing. Used for setting the start face of the dice."""
        self.die._Dice__set_start_face(value)

    def __set_end_face(self, value):
        """Target at testing. Used for setting the end face of the dice."""
        self.die._Dice__set_end_face(value)

    def _set_player_score(self, player_id, score):
        """
        For testing purposes!.

        Set the score of the Player object corresponding to the given Id.
        @ param player_id is of type Player with either P1 or P2 set
        """
        player = self._get_player(player_id)
        if player is not None:
            player._set_score(score)

    def _parse_cheat_test_scores(self, arg):
        """
        For testing purposes!.

        Inseminate test score values for player objects.
        @ param arg is a string, and should be a concatenation of keyword
        test and P1 and/or P2 test score values
        @ return 0 for either or both score if an error is raised.
        """
        arglist = arg.split()
        keyword = None
        p1_score, p2_score = 0, 0
        try:
            keyword = arglist[0].lower()
            if keyword != 'test':
                return p1_score, p2_score
            # Attempt to retrieve player 1 and 2 cheat scores
            p1_score = int(arglist[1])
            p2_score = int(arglist[2])
        except (IndexError, ValueError):
            pass
        return p1_score, p2_score
