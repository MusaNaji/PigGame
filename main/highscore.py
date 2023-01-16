
"""Contains: Highscore class."""


class Highscore():
    """
    Interface a Dictionary object with a list of Tuple.

    Dictionary require unique keys while values in a Tuple grouping may be
    duplicated.

    Tuples are thus used to first generate an order list of highscores, from
    high to low, slicing at a max length of 5. Then, a dict() of integer keys
    numbered 1 and upto 5 (inclusive), is used to represent the relative
    position of each record on the leaderboard; and the dict() exposed as the
    data structure.

    The values of the dict() are concatenatations of the player name and score,
    e.g. Joe#123. The '#' is used as a delimiter, the first portion is treated
    as string and the latter an int.
    """

    FILE_NAME = 'highscore.txt'

    def __init__(self):
        """Initialise the dictionary."""
        self._highscores_dict = dict()

    def revise_highscore(self, newname, newscore):
        """
        Write score and name into Top5 leader board.

        ...if score is >= to any of the five slots available.
        """
        # Propagate TypeError if data type incorrect
        newname = str(newname)
        newscore = int(newscore)
        if newscore < 100:
            return
        # Tuplelist in the form: [(james, 127), (anna, 124), (issac, 101)]
        tuplelist = self._vet_new_highscore(self.get_dict(), newname, newscore)
        updated_dict = self._tuplelist_to_numkeys_dict(tuplelist)
        self.set_dict(updated_dict)
        return self._highscores_dict

    def set_dict(self, a_dict):
        """
        Assign a_dict param to highscore dictinary.

        Enforce it is sorted in ascending order of keys, i.e. 1 - 5.
        """
        new_dict = dict()
        for key in sorted(a_dict.keys()):
            new_dict[key] = a_dict[key]
        self._highscores_dict = new_dict

    def get_dict(self):
        """Return a copy of the dictionary, bound by reference."""
        return self._highscores_dict

    def _tuplelist_to_numkeys_dict(self, tuplelist):
        """
        Convert a TupleList to dictionary, use tuple elements as values.

        Each element of the List contains (name, score). Pair numbers 1 - 5,
        auto-incremented starting from 1, as keys for each element.
        """
        a_dict = {}
        i = 0
        for namescore in tuplelist:
            name, score = namescore
            i += 1
            a_dict[i] = name + '#' + str(score)
        return a_dict

    def _sort_func(self, namescore_tuple):
        """
        Return the second value, the score, of the tuple.

        @ Exeception raises a TypeError if the second element is not an int
        """
        return int(namescore_tuple[1])

    def _vet_new_highscore(self, highscore_dict, newname, newscore):
        """
        Return a List containing a maximum of 5 Tuple pairs.

        Each tuple pair contains two elements, (name, score), with the newname
        and newscore parameters appended.
        """
        values = self._get_name_and_score_tuplelist(highscore_dict)
        values.append((newname, newscore))
        values = sorted(values, key=self._sort_func, reverse=True)
        return values[:5]

    def _get_name_and_score_tuplelist(self, a_dict):
        """Return a list of tuple containing names, score per element."""
        a_list = []
        for record in a_dict.values():
            name, score = record.split('#')
            name.strip()
            score = int(score)
            a_list.append((name, score))
        return a_list
