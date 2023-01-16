
"""Contains: FileOps class."""

from io import TextIOWrapper
from pig.main.enums_module import PlayMode
from pig.main.enums_module import FirstMover
from pig.main.enums_module import PlayerObj
from pig.main.enums_module import Difficulty
from pig.main.enums_module import FileMode
from pig.main.enums_module import DataKey


class FileOps():
    """
    An interface class between Dictionary and FileObjects.

    Dictionarys are used to register changes to data, so that, FileObjects are
    only accessed when data has changed during the App's active cycle.
    """

    default_setting_dict = {
        DataKey.MODE.name: PlayMode.TWO_PLAYERS.value,
        DataKey.DIFF.name: Difficulty.MID.value,
        DataKey.MOVER.name: FirstMover.RAND.value,
        DataKey.P1.name: PlayerObj.P1.value,
        DataKey.P2.name: PlayerObj.P2.value
    }

    def get_file_object(self, filename, mode):
        """
        Open a file for READ, WRITE or APPEND operation.

        It is imperative the caller calls close() on file_object after use.
        @ filename is the name or path of the file
        @ return a file_object for filename or None if it does not exist
        @ raises Exeception if other unhandled IO Error raised
        """
        # Enforce mode is of type Mode
        if not isinstance(mode, FileMode):
            raise TypeError('mode should be an Enum of type FileMode')
        try:
            # Return file_object if present, else None to indicate absence
            file_object = open(filename, mode.value)
            # print('get_file_object: File_obj opened for ' + mode.name)
            return file_object
        except FileNotFoundError:
            print('get_file_object: File failed to open for WRITE mode')
            return None
        except Exception:
            # Log other unhandled error
            print("get_file_object: Error openning file for " + mode.name)
            return None

    def read_file_to_dict(self, file_object):
        """
        Read content from file object to dict, and return the dict.

        Auto-close file_object after use.

        Loads record, from file to dict with pass-by-ref, containing a
        record of two values with ':' as delimiter, e.g. score:name, the
        first part, which is used as dictionary key needs to be unique.
        @ param file_object is the return value of open(a_filename, 'r')
        @ return a Dictionary of the key value pair records of the file
        @ raises TypeError of file_object None or not type TextIOWrapper
        """
        # Enforce data types
        self._is_file_object(file_object)
        a_dict = dict()
        for line in file_object:
            line = line.strip()
            if line.count(':') == 1:
                line_list = line.split(':')
                a_dict[line_list[0]] = line_list[1]
        self.close_file_object(file_object)
        return a_dict

    def write_dict_to_file(self, file_object, a_dict):
        """
        Write dict contents to file, and auto-close file_object after use.

        Used ':' as delimiter, in the format 'key:value'.
        @ param file_object is the return value of open(a_filename, 'w')
          or open(a_filename, 'a')
        @ param a_dict is a Dictionary object
        @ return True if no error is encountered
        """
        # Enforce data types
        self._is_file_object_and_dict(file_object, a_dict)
        if file_object.mode != FileMode.WRITE.value:
            raise IOError(file_object.name + ' is not opened in write mode.')
        for key, value in zip(a_dict.keys(), a_dict.values()):
            data = str(key) + ":" + str(value) + "\n"
            file_object.write(data)
        self.close_file_object(file_object)
        return True

    def _is_file_object(self, file_object):
        """
        Private member for enforcing data type.

        @ raises TypeError if file_object is not type TextIOWrapper or None
        """
        if not isinstance(file_object, TextIOWrapper) or file_object is None:
            raise TypeError('file_object does not satify type requirement')
        return True

    def _is_file_object_and_dict(self, file_object, a_dict):
        """
        Private member for enforcing data type.

        @ param file_object is a TextIOWrapper
        @ param a_dict is a Dictionary
        @ raises TypeError if file_object is not type TextIOWrapper or
                 a_dict is not type Dictionary, oe None
        """
        is_null = file_object is None or a_dict is None
        is_not_dict = not isinstance(a_dict, dict)
        is_not_fobj = not isinstance(file_object, TextIOWrapper)
        if is_null or is_not_fobj or is_not_dict:
            raise TypeError('Params do not satify type requirement')
        return True

    def dict_contains(self, a_dict, key_list):
        """Return true if dictionary contains all and only the keys in list."""
        dict_keys_list = a_dict.keys()
        if len(key_list) != len(a_dict):
            return False
        for key in key_list:
            if key not in dict_keys_list:
                return False
        return True

    def close_file_object(self, file_object):
        """Close FileObject if it is still alive."""
        if isinstance(file_object, TextIOWrapper) and not file_object.closed:
            file_object.close()
