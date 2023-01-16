# Main program

"""

Let's play the dice game of "Pig".

The objective of the game is to be the first player to reach 100 points.

  - If during a turn a player rolls a value other than 1, it
    is added to turn total and rolling may continue.

  - If a player rolls 1 during a turn, no points are awarded and
     the turn toggled to the opponent player.

  - If a player holds, the sum of dice rolls during that turn is
    added to their running total, and the turn toggled.

Highscores are allocated based on the highest scores over 100.

WHO DARES WIN! Good Luck!

"""

from cmd import Cmd
import time
from interface import implements
from pig.main.enums_module import PlayMode
from pig.main.enums_module import PlayerObj
from pig.main.enums_module import Difficulty
from pig.main.enums_module import FirstMover
from pig.main.enums_module import FileMode
from pig.main.enums_module import Change
from pig.main.enums_module import DataKey
from pig.main.interfaces.mainview import MainView
from pig.main.mainpresenter import MainPresenter
from pig.main.fileops import FileOps


# TODO: Deprecate TurnData, class is an overhead overcomplicating testing

class MainShell(Cmd, implements(MainView)):
    """Controller of all other classes, assited by MainPresenter."""

    intro = 'Type help or ? to list available commands.\n'
    prompt = '(pig menu) '

    abort_msg = '\nAborting, changes have not been saved.\n'

    command_unavailable = 'command_unavailable'

    SETTINGS_FILE_NAME = 'settings.txt'

    fileops = FileOps()
    in_game_mode = False

    # Flags if there is variation in settings data between settings_dict
    # and settings.txt. This method is adopted so that file objects are only
    # loaded after user has decided on final values. This way the file object
    # is not repeated opened and closed.
    has_settings_changed = False

    presenter = None

    # region CMD Overrides

    def preloop(self):
        """@ Override the CMD hook method."""
        # Initialise presenter object
        self.presenter = MainPresenter(self)
        self.load_or_sync_settings()
        self.presenter.init_high_score_data()

    def precmd(self, arg):
        """
        @ Override the CMD hook method.

        Restrict commands to 'roll', 'hold' when game ongoing, when game is not
        in play, disable theses commands
        """
        # Enforce lowercase so that COMMAND is equivalent to command
        arg = arg.lower().strip()
        # By returning an illegal str, call shortcircuits to default(self, arg)
        my_list = arg.split()
        do = my_list[0].lower()
        if self.in_game_mode and do not in ['roll', 'hold', 'exit']:
            return self.command_unavailable
        elif not self.in_game_mode and do in ['roll', 'hold']:
            return self.command_unavailable
        return arg

    def default(self, arg):
        """
        @ Override the CMD hook method.

        Shortcircuits from calling do_* if precmd() calls with arg =
        'command_unavailable'.
        """
        if arg == self.command_unavailable:
            print('*** Command unavailabe.')
        elif arg == 'roll' or arg == 'hold':
            # print("Calling handle_turn() from default(arg)")
            self.handle_turn()
        else:
            print('*** Unknown syntax: ' + arg)

    # endregion

    # region MainView Overrides

    def will_roll(self, current_turn_score):
        """
        @ Override implementation of MainView interface.

        Method takes roll decision from console and computer.
        @ user_input is a char value taken from UI and should be Entered
            when current_player is not computer
        @ returns false if roll accepted, otherwise false.
        """
        player = self.presenter.get_current_player()
        name = player.get_name()
        if player.is_computer():
            will_roll = self.presenter.intel.will_roll(current_turn_score)
            time.sleep(1.5)  # Wait 1.5 seconds
            # Intelligence class manages decision to roll or hold
            return will_roll
        else:
            while True:
                # Inputs taken here do not go through cmdloop!!!!!
                do = str(input('(game mode: ' + name + ') '))
                if do == 'roll':
                    return True
                elif do == 'hold':
                    # Return false to return from presenter.manage_turn()
                    return False
                elif do == 'exit':
                    # Return False to return from presenter.manage_turn()
                    # print(">>> main.will_roll: exit condition entered")
                    self.in_game_mode = False
                    # Update prompt to simulate a return to Main Menu
                    self.prompt = '(pig menu) '
                    self.presenter.force_exit = True
                    return False
                elif do in ['settings', 'play', 'highscore']:
                    # prints '*** Command unavailabe.'
                    self.default(self.command_unavailable)
                else:
                    # prints '*** Unknown syntax: ' + do
                    self.default(do)

    def print_roll_stats(self, player, turntotal, rollednum):
        """
        @ Override implementation of MainView interface.

        Print the value just rolled to screen.
        """
        print('  ' + player.name + ' rolled a ' + rollednum + '.')
        print('  Total turn score is ' + turntotal + ".\n")

    # endregion

    # region do_* Methods

    def do_play(self, arg):
        """Start a game with currently applied settings: 'PLAY'."""
        # Whilst in game mode, subsequent do commands - ROLL, HOLD, EXIT - are
        #  handled in the overridden hook method, default(arg).

        # Apply Cheat scores, if correct syntax provided
        p1score, p2score = self.presenter._parse_cheat_test_scores(arg)
        self.presenter._set_player_score(PlayerObj.P1, p1score)
        self.presenter._set_player_score(PlayerObj.P2, p2score)

        self.in_game_mode = True
        if self.has_settings_changed:
            self.load_or_sync_settings()
        currentplayer = self.presenter.assign_first_mover(FirstMover.RAND)
        self.show_turn_prompt(currentplayer)
        # From this point forward, app will loop in will_roll() and do commands
        #  will no longer register until 'exit' is entered via commandline
        self.handle_turn()

    def do_highscore(self, arg):
        """Print current highscore to console."""
        # False indicates that highscore is target, and not setting dict.
        self.print_dictdata_toconsole(False)

    def do_exit(self, arg):
        """Exit the game and close the console: 'EXIT'."""
        print('Thanks for playing. Enter PLAY to have another go.')
        return True

    def do_settings(self, arg):
        """
        Display the current game settings: 'SETTINGS'.

        Also use to make changes to values of player names, playermode
        and difficulty: SETTINGS + ([name | mode | diff])
        """
        msg = """
        Argument accompanying SETTINGS not recognised, Enter...
              SETTINGS display' to show current settings or
              SETTINGS name' to change names, or
              SETTINGS mode' to change player mode
              SETTINGS diff' to change computer difficulty
              """
        if arg == 'display':
            self.print_dictdata_toconsole(True)
            print('To change, Enter: SETTINGS + ([name | mode | diff])')
        elif arg == Change.NAME.value:
            # print('>>> do_change: Entered change name')
            self.change_name()
        elif arg == Change.MODE.value:
            print('>>> do_change: Entered change play mode')
            self.change_play_mode()
        elif arg == Change.DIFF.value:
            print('>>> do_change: Entered change difficulty')
            self.change_computer_difficulty()
        else:
            print(msg)
        if self.has_settings_changed:
            msg = """
            Your settings have been taken, to persist them play a game
            by entering: PLAY

            """
            print(msg)

    def do_rules(self, arg):
        """Print out the rules of the game to console."""
        print(self.presenter.RULES)

    # endregion

    # region Helper methods

    def change_name(self):
        """Change a player's name, helper method for do_settings."""
        msg = 'Current names are, P1 = ' + self.presenter.player1.get_name() \
              + ' and P2 = ' + self.presenter.player2.get_name() + '.'
        print(msg)
        # Breaks from loop in the inner loop after name change or EXIT passed
        while True:
            name = input("To change, use the format 'P1 Joe' or 'P2 Anna': ")
            if name == 'exit':
                print(self.abort_msg)
                break
            try:
                # Parse the user input ('P1 Joe') into identifier and value
                alist = name.split()
                identifier = alist[0].strip().upper()
                new_name = alist[1].strip()
                flag = identifier in [FirstMover.P1.name, FirstMover.P2.name]
                if (len(new_name) <= 0) or (not flag):
                    raise ValueError
                # Change name if correct identifier and name given
                if self.presenter.update_setting(identifier, new_name):
                    self.has_settings_changed = True
                    break
            except (IndexError, ValueError):
                print("\nUnrecognised input, please try again...")
                msg = """"
                Identify the player object you wish to change along
                with the new name. Name must be 1 or more characters
                      E.g. Enter: 'P1 Anna'

                      """
                print()
            continue

    def change_play_mode(self):
        """Change play mode, helper method for do_settings."""
        msg = self.concat_current_diff_and_mode()
        print(msg)
        mode, diff = self.presenter.get_play_mode_and_diff()
        if mode == PlayMode.ONE_PLAYER.value:
            msg = "To change to TWO_PLAYERS mode, enter 'TWO': "
        else:
            msg = "To change to ONE_PLAYER mode, enter 'ONE': "
        # Loop the user through the change process
        while True:
            value = input(msg)
            if value == 'exit':
                print(self.abort_msg)
                break
            try:
                value = value.strip().lower()
                vlist = [PlayMode.ONE_PLAYER.value, PlayMode.TWO_PLAYERS.value]
                if (len(value) <= 0) or (value not in vlist):
                    raise ValueError
                # Change if correct value given
                if self.presenter.update_setting(DataKey.MODE.name, value):
                    self.has_settings_changed = True
                    break
            except (IndexError, ValueError):
                print("\nUnrecognised input, please try again...")
                print("\tEnter either 'ONE' or 'TWO'")
            continue

    def change_computer_difficulty(self):
        """Change difficulty, helper method for do_settings."""
        print(self.concat_current_diff_and_mode())
        # Loop the user through the change process
        while True:
            value = input("To change computer difficulty, Enter - 'HIGH',\
                           'MID' or 'LOW': ")
            if value == 'exit':
                print(self.abort_msg)
                break
            try:
                # Parse the user input
                value = value.strip().lower()
                validlist = [Difficulty.HIGH.value, Difficulty.MID.value,
                             Difficulty.LOW.value]
                if (len(value) <= 0) or (value not in validlist):
                    raise ValueError
                # Update changes if correct value given
                if self.presenter.update_setting(DataKey.MODE.name, value):
                    self.has_settings_changed = True
                    break
            except (IndexError, ValueError):
                print("\nUnrecognised input, please try again...")
                print("\tEnter either 'HIGH','MID' or 'LOW'")
            continue

    def concat_current_diff_and_mode(self):
        """Return difficulty and mode values concatenated with descriptors."""
        mode, diff = self.presenter.get_play_mode_and_diff()
        # Display either single or two player current setting
        msg = 'Current PlayMode is ' + mode
        if mode == PlayMode.ONE_PLAYER.value:
            msg += ' and Difficulty, ' + diff
        msg += '.'
        return msg

    def print_dictdata_toconsole(self, is_settings):
        """Print dictionary data to console with an appropriate header."""
        print()
        if is_settings:
            print('  SETTINGS')
            a_dict = self.presenter.get_settings_dict()
        else:
            print('  HIGHSCORE')
            a_dict = self.presenter.get_highscore_dict()
        print('-' * 30)
        for k, v in a_dict.items():
            print("{:>13} {:^}".format(k + '\t', v + '\t'))
        print()

    def handle_turn(self):
        """
        Manage turn stats of currentplayer object at end of turn.

        Also checks if this propagates player to 100 points: for the win.
        """
        # print(">>> main.handle_turn: Entered")
        turnscore, rolls_made = self.presenter.manage_turn()
        # If FORCE_EXIT flagged from will_roll, then pass
        if self.presenter.force_exit:
            # print(">>> main.handle_turn: aborting")
            # Pass checks and flag game mode false to simulate return to Menu.
            self.in_game_mode = False
        else:
            # print(">>> main.handle_turn: Else statement")
            self.presenter.update_currentplayer(turnscore, rolls_made)
            # Handle end of game or currentplayer toggle
            player = self.presenter.get_current_player()
            self.has_player_won(player, turnscore, rolls_made)

    def has_player_won(self, player, turnscore, turn_rolls_made):
        """
        Check if the last turn resulted in 100points.

        If so, end game, else toggle to other player and continue game.
        """
        name = player.get_name()
        score = player.get_score()
        if score >= 100:
            msg = '  \n(• ◡ •)' + player.get_name() + " has won with " \
                  + str(score) + ' (• ◡ •)\n'
            print(msg)
            self.presenter.log_highscore(name, score)
            self.in_game_mode = False
            # Simulate return to Main Menu
            self.prompt = '(pig menu) '
            self.do_exit('exit')
        else:
            # Print turn stats before toggling player
            msg = '  ** ' + name + ' bagged ' + str(turnscore) + \
                  ' points after ' + str(turn_rolls_made) + " rolls..." + \
                  ' and now has ' + str(score) + " points. **\n"
            print(msg)
            # Toggle player and show turn prompt
            self.presenter.toggle_current_player()
            self.show_turn_prompt(self.presenter.get_current_player())
            # Propagate the inner will_roll() method of presenter.manage_turn()
            # by calling hook method default(roll) directly.
            self.default('roll')

    def load_or_sync_settings(self):
        """
        Ensure at least default settings is loaded to settings dictionary.

        Attempts to load settings from settings.txt (file) if dictionary is
        null, otherwise it syncs the current content of the dict to file, if
        change flagged. Finally, it tests that all expected keys are present,
        otherwise default values are enforced.
        """
        # Get a copy of the dictionary
        setting_dict = self.presenter.get_settings_dict()
        # Get file obj in 'r' mode, None if file not present
        if setting_dict is None or len(setting_dict) < 1:
            file_obj = self.fileops.get_file_object(
                self.SETTINGS_FILE_NAME, FileMode.READ)
            if file_obj is not None:
                # Load game settings from file
                a_dict = self.fileops.read_file_to_dict(file_obj)
                self.presenter.set_settings_dict(a_dict)
                file_obj.close()
        elif self.has_settings_changed:
            file_obj = self.fileops.get_file_object(
                self.SETTINGS_FILE_NAME, FileMode.WRITE)
            if file_obj is not None:
                self.fileops.write_dict_to_file(file_obj, setting_dict)
                file_obj.close()
            # Flag settings on dictionary and file as synced
            self.has_settings_changed = False
        # Apply default settings if any required key is absent
        key_list = DataKey.values_list()
        # Re-retrieve the current state of settings dict
        setting_dict = self.presenter.get_settings_dict()
        if not self.fileops.dict_contains(setting_dict, key_list):
            self.presenter.set_settings_dict(FileOps.default_setting_dict)
            self.has_settings_changed = True
        self.presenter.update_player_name(PlayerObj.P1)
        self.presenter.update_player_name(PlayerObj.P2)
        # return value indicates is_computer, if true init Intelligence
        self.presenter.apply_single_player_setting()
        return True

    def show_turn_prompt(self, player):
        """Print prompt to console using the passsed players name."""
        # Print the current player's score if they have banked any.
        score = player.get_score()
        score_info = ''
        if score > 0:
            score_info = ', your game score is ' + str(score) + '.'
        print('\n  Your turn, ' + player.get_name() + score_info)
        print('  Enter ROLL to roll, or HOLD to yield turn to opponent.\n')

    # endregion


if __name__ == '__main__':
    print(__doc__)
    MainShell().cmdloop()
