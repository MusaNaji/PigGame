# PIG DICE GAME

The project is in fulfillment of the DA115A Methods for sustainable programming  course, Part 2.


## Rules of the game

The objective of the game is to be the first player to reach 100 points,

however, highscores are allocated based on the highest scores over 100.

  - If during a turn a player rolls a value other than 1, it is added to turn total and rolling may continue.

  - If a player rolls 1 during a turn, no points are awarded and the turn toggled to the opponent player.

  - If a player holds, the sum of dice rolls during that turn is added to their running total, and the turn toggled.


## Installation and operating instruction

**Notice**

The instructions hereafter have been verfied to work on Python 3.9.0 and a Windows 10 operating system, however,

it is expected that replication of the steps should produce similiar results on other operating systems.


**Virtual enviroment setup**

To install and run the app, you should have a version of Python3 installed on their system.

This is neccessary because versions of Python3 come with a virtual enviroment (venv) feature.

- Make sure that your version of python39 resides on the OS(C:) directory

- On the commandline (cmd is used here), use 'cd ..' to regress the path to 'C:\>'

- From 'C:\>' Create a virtual enviroment with its folder located on your desktop, using  c:\Python39\python -m venv ..\Desktop\my-env

- Verify that a folder with the name **my-env** (or any other root name used as per above comment) is located on the Desktop.


**App download**

- If not already on system, download or fork the pig app from the GitLab repo, https://gitlab.com/bsc-swdev/pig

- Move the pig folder into the vitual enviroment (This is neccessary for the package references within the app to work!)


**Running**

- On the commandline, transition the path to ../Desktop/my-env/pig>

- If you have not already download app dependencies as per ../pig/requirements.txt, enter 'make **install**'

- To verifiy that the requirements are download, enter 'make **installed**'

- Enter 'make **run**' to start the game

## Intelligence implementation

This class main goal is to control how the computer class react with its turn and decide if the computer player is going to play again or hold. The computer decision depends on the player difficulty value , the current turn score and the random play allowed for each difficulty value.

**Functionality:**

The class have 2 main methods that controls the computer player decision during its turn:

  - def _will_roll_impl(self, score):

Returns true or false based on the calculated value, odd ratio : current score / average, and the difficulty value or if the current turn score is >= 90 in HIGH difficulty level will return true as will.

  - def _random_play(self):

Randomising will roll decision further, based on random_value and difficulty value and return True or False based on that.


## Information on how to use the Game Cheat

For the testing purposes, player scores can be staged, this is useful for rapid testing areas such as 'end of game

management', 'highscore registration' etc.

**Syntax**

To do so, when entering PLAY command, add the parameters 'TEST score score'.

- Where 'score' are integer variables, e.g. 'PLAY TEST 78 21'

- It is also possible to enter only one value, e.g. 'PLAY TEST 78'. In this case, 78 is assigned to the Player1 object and the default

score of 0, prevails for Player2.

**Error**

If a value other than of type int is entered for the first 'score' value, e.g. 'PLAY TEST seventy_eight' or 'PLAY TEST seventy_eight 23' or

the keyword 'TEST' is omitted or whitespace is not used to separate the values: None of the score values are applied, and default score of 0,

prevails for both player objects. If the second value is of an incorrect, provided 'TEST' is appended, the first value is applied.


## Running the complete testsuite and getting the coverage report

After navigating to the path ~/Desktop/my-env/pig on the commandline, where my-env represents the  name of the virtual environment,

Use ' **make** [coverage | pylint | flake8] ' to run the coverage, pylint and flake8, respectively.

**The coverage call above does not cover FileOps integration test which involves FileObjects.**

Use The instructions below:

- Transition the path (without any whitespace) to the test directory: Desktop\ **my-env ** \pig\tests>

- Use 'coverage run -m unittest fileops_test_integration' to run the test

- Use 'coverage report' or 'coverage report -m' (with missing lines) to examine the percentage coverage.

- Use 'coverage html' to generate an htmlcov folder with detailed account of the coverage report (hint: the html files are atop).


## Generating the UML class diagram

To generate UML documentation follow the following steps:

- Install Pynsource.com with the corresponding operating system.

- unzip and run setup program.

- Open Pynsource

  - Click on File -> Import Python Code... -> go to Main and mark all the PY-files exept init  -> Open.

  - Click on File -> Import Python Code... -> go to main and interfaces and mark the mainview  -> Open.

  - choose between UML - Ascii Art - (PlantUML).


## Generating API Documentation

To generate api documentation, using pydoc package, follow the following steps:

- open command line and move it to the target module directory.

- run the instructions : python -m pydoc -w module name.

- finally you will find a html documentation file in the same directory of the target module.

Note : pydoc package is a build-in package no need to install it.


## Generating the Package diagram

- Install Chocolatey from https://chocolatey.org/install

- Install graphviz Through the Chocolatey package manager with administrator privileges in CMD.

- run: choco install graphviz

- Pyreverse is inside the Pylint package.

- Use pyreverse to generate UML and HTML documentation.

In cmd, cd to the folder where you put the repo, dose not matter where.

- Run: pyreverse pig/

- you will get two files, one classes. and one packages.

- use this command below to make a package diagram on the same place.

- Run: dot -Tpng packages.dot -o packages.png
