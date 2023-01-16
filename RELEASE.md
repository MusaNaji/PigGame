# RELEASE LOG

#### All versioning changes for the project are documented here.


## [3.1.0] - 12-03-2021

- Add UML diagram

- Add api docs

- Update README

- Verify pylint and flake8 adherence.

- Add Instruction on generating the UML to README.md

- Apply flake8 and pylint rules, and finalise Make.

- Add doc strings for Player


## [3.0.1] - 11-03-2021

- Fix bug, inability to start a new game after end of a game.

- Add Highscore and cheat.


## [3.0.0] - 10-03-2021

- Finalise cheat method for rapid testing.


## [2.2.0] - 10-03-2021

- Highscore algorithmn full implemented but not tested, waiting to add cheat test function for ease of testing

- Conclude highscore unittest.

- Fix 'self' bugs

- Migrate Highscore details to anew class

- Fix Enum bug

- Refactor do_setting() for DRY


## [2.1.0] - 09-03-2021

- Computer Intelligence further randomised.


## [2.0.0] - 09-03-2021

- Computer Intelligence added to support single player mode.


## [1.1.1] - 08-03-2021

- Bug fixes on applying single player setting


## [1.1.0] - 07-03-2021

- Add player mode change and persistence functionality.
- Refactor data and files  such that DataKey enum is used for setting_dict
- Update fileops_test.
- Refactor change_name() to catch IndexError.
- Fix m_is_computer bug.
- Enforce name for Player objects as 'Computer' if is_computer True.
- Add name change and persistence functionality.
- Display current player in prompt string


## [1.0.0] - 02-03-2021

- Merge branch '5-develop-gamelogic' into 'master'
- Implement 2 player mode.
- Working TWO_PLAYERS mode with bug
- Disable game mode after quiting a game.
- Test currentplayer is correctly assigned for firstmover.
- MainShell to re-diverts roll, hold and back (RHB) ccommands when in gamemode loop
- Establish MainShell as the only class in main.py.
- Update the generic dice.py presented by the Lecturer
- Assert passing an illegal type for file object or dictionary raises Exception
- Test writing and reading data from file.
- Add all test cases for FileOps.get_file_object()
- Restrict commands to roll, hold and back when game is ongoing
- Develop settings populaton on startup and change.
- Generalise get_file_object() for read, write and append.
- Introduce file reading/write capability, used for storing settings/highscore
- Add do_exit() method for exiting cmd shell.
- Test pig/main.py interface implementation.
- Adopt an MPV setup for main program
- Test gamelogic instantiation state
- Create player class and Player unittest.
- Add assign_turn and will_roll methods
- Add global classes and enum
