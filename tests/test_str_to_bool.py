"""
StrToBoolクラスのテストコード.

@author: Takahiro55555
"""

import unittest

from camera.str_to_bool import StrToBool


class TestStrToBool(unittest.TestCase):
    def test_str_to_bool(self):
        expected = True
        actual = StrToBool.convert('T')
        self.assertEqual(expected, actual)
        actual = StrToBool.convert('True')
        self.assertEqual(expected, actual)
        actual = StrToBool.convert('t')
        self.assertEqual(expected, actual)
        actual = StrToBool.convert('true')
        self.assertEqual(expected, actual)

        expected = False
        actual = StrToBool.convert('F')
        self.assertEqual(expected, actual)
        actual = StrToBool.convert('False')
        self.assertEqual(expected, actual)
        actual = StrToBool.convert('f')
        self.assertEqual(expected, actual)
        actual = StrToBool.convert('false')
        self.assertEqual(expected, actual)

    def test_str_to_bool_error(self):
        with self.assertRaises(ValueError):
            StrToBool.convert('hoge')
