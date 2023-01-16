
"""Contains: TestFileOps."""

import unittest
from pig.main.fileops import FileOps
from pig.main.enums_module import FileMode
from pig.main.enums_module import DataKey


class TestFileOps(unittest.TestCase):
    """FileOps class unit tests."""

    def setUp(self):
        """Pre testcases setup."""
        self.fileobj = None
        self.fileops = FileOps()

        self.expected_keys = ['MODE', 'DIFF', 'MOVER', 'P1', 'P2']

        # Populate default dictionary as the basis of the test
        self.values = ['two', 'mid', 'random', 'Player1', 'Player2']
        self.expected_dict = {}
        for i in range(len(self.expected_keys)):
            key = self.expected_keys[i]
            self.expected_dict[key] = self.values[i]

    def tearDown(self):
        """Clean up resources."""
        self.fileops.close_file_object(self.fileobj)

    def test__assert_test_setup(self):
        """
        Assert test setup values are as expected.

        DataKey values of Enum, matches with test values of setup and that
        hardcoded self.values here match values of FileOps.default_setting_dict
        """
        keys = list(self.expected_dict.keys())
        values = list(self.expected_dict.values())

        # Check that dictionary data keys are correctly initialised
        self.assertEqual(DataKey.values_list(), keys)

        # Get the default values for default_setting_dict
        default_values = list(FileOps.default_setting_dict.values())
        self.assertEqual(values, default_values)

    def test__close_file_object(self):
        """File closes."""
        fileobj = self.fileops.get_file_object('test_file.txt', FileMode.WRITE)
        self.assertFalse(fileobj.closed)

        self.fileops.close_file_object(fileobj)
        self.assertTrue(fileobj.closed)

    def test__get_file_object__read_and_write(self):
        """
        Open a file object in a current directory, assert works.

        Use pig/tests/test_file.txt test file for 'w' and 'r' mode.
        """
        self.fileobj = \
            self.fileops.get_file_object('test_file.txt', FileMode.WRITE)
        self.assertIsNotNone(self.fileobj)

        # test_file.txt is created above, should not return None
        self.fileobj = \
            self.fileops.get_file_object('test_file.txt', FileMode.READ)
        self.assertIsNotNone(self.fileobj)

    def test__get_file_object__read_returns_None(self):
        """
        Open a file object, for read, whose name is not present in current dir.

        Throws a FNFE and method returns None.
        """
        self.fileobj = \
            self.fileops.get_file_object('notcreated.txt', FileMode.READ)
        self.assertIsNone(self.fileobj)

    def test__get_file_object__raises_type_error(self):
        """Non-Enum FileMode for mode param raises TypeError."""
        with self.assertRaises(TypeError):
            self.fileops.get_file_object('notcreated.txt', "Illegaltype")

    def test__read_file_to_dict_success(self):
        """
        With file present and the correct data, load to Dictionary.

        Test is dependent on a read_test_file.txt being in the current dir.
        """
        # Enforce that file exists with correct content
        fileobj = self.fileops.get_file_object(
                                          'read_test_file.txt', FileMode.READ)
        self.assertIsNotNone(fileobj)

        a_dict = self.fileops.read_file_to_dict(fileobj)
        # self.assertEqual(len(self.expected_dict), len(a_dict))
        self.assertEqual(self.expected_dict, a_dict)

    def test__write_dict_to_file__in_write_mode(self):
        """
        File object param is in 'w' mode.

        Assertion 1 tests that IOError is raises, and 2 that end of method
        is reached.
        """
        # Assert incorrect Mode
        fileobj = self.fileops.get_file_object('test_file.txt', FileMode.READ)
        with self.assertRaises(IOError):
            self.fileops.write_dict_to_file(fileobj, dict())

    def test__write_dict_to_file__write_and_read(self):
        """
        Write data to a given file then reads back the content.

        Data successfully written.
        """
        # write data to file
        fobj = self.fileops.get_file_object('test_file2.txt', FileMode.WRITE)
        data_to_write = self.expected_dict
        flag = self.fileops.write_dict_to_file(fobj, data_to_write)

        # Assert correct mode of WRITE, returns True
        self.assertTrue(flag)

        # Read data back
        fobj = self.fileops.get_file_object('test_file2.txt', FileMode.READ)
        a_dict = self.fileops.read_file_to_dict(fobj)
        self.assertEqual(self.expected_dict, a_dict)

    def test__is_file_object__bad_type(self):
        """
        Pass an illegal type for file object: raises TypeError.

        Legal data type is tested as a side-effect in test__read_file_to_dict.
        """
        with self.assertRaises(TypeError):
            self.fileops.read_file_to_dict("Illegaltype")
        with self.assertRaises(TypeError):
            self.fileops.read_file_to_dict(None)

    def test__is_file_object_and_dict__bad_type(self):
        """
        Pass an illegal type for file object or dictionary raises TypeError.

        Legal data type is tested as a side-effect in test__write_dict_to_file.
        """
        fobj = self.fileops.get_file_object('test_file.txt', FileMode.READ)
        # Dictionary is None / Illegaltype passed
        with self.assertRaises(TypeError):
            self.fileops._is_file_object_and_dict(fobj, None)
        with self.assertRaises(TypeError):
            self.fileops._is_file_object_and_dict(fobj, "Illegaltype")

        # FileObject is None / Illegaltype passed
        with self.assertRaises(TypeError):
            self.fileops._is_file_object_and_dict(None, dict())
        with self.assertRaises(TypeError):
            self.fileops._is_file_object_and_dict("Illegaltype", dict())

    def test__dict_contains(self):
        """
        Dictionary contains all and only listed keys.

        True when Dictionary size matches List, and each element
        intersects with each Dictionary key, otherwise returns False.
        """
        s_dict = self.expected_dict
        k_list = self.expected_keys

        # Returns False when key_list len does not match dict_obj
        temp_key_list = [DataKey.MODE.name, DataKey.DIFF.name]
        # Dict has 5 keys
        self.assertFalse(self.fileops.dict_contains(s_dict, temp_key_list))

        # Returns False when len match, but list and dict keys do not match
        key0 = None
        value0 = None
        # Remove the first itr k, v pair, make note of it and break
        for k, v in s_dict.items():
            key0 = k
            value0 = v
            break
        # Remove the value from dict
        del s_dict[key0]
        # Add a key that is not in key_list
        s_dict["unmatching_key"] = "temp"
        self.assertFalse(self.fileops.dict_contains(s_dict, k_list))

        # Returns True when len and keys match
        # Remove the offending key, value pair from dict
        del s_dict["unmatching_key"]
        # Re-add key0, value0
        s_dict[key0] = value0
        self.assertTrue(self.fileops.dict_contains(s_dict, k_list))
