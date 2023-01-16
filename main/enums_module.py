"""Enum classes modularised into one file."""

from enum import Enum


class PlayMode(Enum):
    """PlayMode Enum with assigned values."""

    ONE_PLAYER = 'one'
    TWO_PLAYERS = 'two'


class Difficulty(Enum):
    """Difficulty Enum with assigned values."""

    LOW = "low"
    MID = "mid"
    HIGH = "high"


class PlayerObj(Enum):
    """For uniquely identifying player objects."""

    P1 = 'Player1'
    P2 = 'Player2'


class FirstMover(Enum):
    """For uniquely identifying first mover."""

    RAND = 'random'
    P1 = PlayerObj.P1.value
    P2 = PlayerObj.P2.value


class FileMode(Enum):
    """Use with FileOps to designate the interaction mode with FileObjects."""

    READ = 'r'
    WRITE = 'w'
    APPEND = 'a'


class DataKey(Enum):
    """Global keys for settings dictionary."""

    MODE = 'mode'
    DIFF = 'diff'
    MOVER = 'mover'
    P1 = 'p1'
    P2 = 'p2'

    @classmethod
    def values_list(cls):
        """Return a list contain all the names of DataKey."""
        return list(cls.__members__.keys())


class Change(Enum):
    """Use with do_settings to decipher and manage change parameters."""

    NAME = 'name'
    MODE = 'mode'
    DIFF = DataKey.DIFF.value
    SINGLE_MODE = PlayMode.ONE_PLAYER.value
    TWO_MODE = PlayMode.TWO_PLAYERS.value
