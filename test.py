#!/usr/bin/env python3

import unittest
from doctest import testmod
from prose2 import *

INT = "1"
STR = '"hi"'
VAR = "x"
LIST = [read([]), INT, STR, VAR]


class Test_entry_is_int(unittest.TestCase):
    def test_empty_list(self):
        self.assertFalse(entry_is_int(read([])))
        
    def test_int(self):
        self.assertTrue(entry_is_int(INT))

    def test_str(self):
        self.assertFalse(entry_is_int(STR))

    def test_var(self):
        self.assertFalse(entry_is_int(VAR))

    def test_list(self):
        self.assertFalse(entry_is_int(LIST))


class Test_entry_is_str(unittest.TestCase):
    def test_empty_list(self):
        self.assertFalse(entry_is_str([]))
        
    def test_int(self):
        self.assertFalse(entry_is_str(INT))

    def test_str(self):
        self.assertTrue(entry_is_str(STR))

    def test_var(self):
        self.assertFalse(entry_is_str(VAR))


class Test_read(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(read([]), {"underlying": [], "display": [], "scope": {}})

    def test_int(self):
        self.assertEqual(read(INT), {"underlying": int(INT), "display": INT, "scope": {}})

    def test_str(self):
        self.assertEqual(read(STR), {"underlying": eval(STR), "display": STR, "scope": {}})

    def test_var(self):
        self.assertEqual(read(VAR), {"underlying": VAR, "display": VAR, "scope": {}})

    def test_list(self):
        self.assertEqual(read([[], "1", '"hi"', "x"]),
                         {"underlying": [{'underlying': [], 'display': [], "scope": {}},
                                         {"underlying": 1, "display": "1", "scope": {}},
                                         {"underlying": "hi",
                                          "display": '"hi"',
                                          "scope": {}},
                                         {"underlying": "x", "display": "x", "scope": {}}],
                          "display": [[], "1", '"hi"', "x"], "scope": {}})


class Test_value_is_list(unittest.TestCase):
    def test_empty_list(self):
        self.assertTrue(value_is_list(read([])))

    def test_int(self):
        self.assertFalse(value_is_list(read(INT)))

    def test_str(self):
        self.assertFalse(value_is_list(read(STR)))

    def test_var(self):
        self.assertFalse(value_is_list(read(VAR)))

    def test_list(self):
        self.assertTrue(value_is_list(read(LIST)))


class Test_value_is_int(unittest.TestCase):
    def test_empty_list(self):
        self.assertFalse(value_is_int(read([])))

    def test_int(self):
        self.assertTrue(value_is_int(read(INT)))

    def test_str(self):
        self.assertFalse(value_is_int(read(STR)))

    def test_var(self):
        self.assertFalse(value_is_int(read(VAR)))

    def test_list(self):
        self.assertFalse(value_is_int(read(LIST)))


class Test_value_is_str(unittest.TestCase):
    def test_empty_list(self):
        self.assertFalse(value_is_str(read([])))

    def test_int(self):
        self.assertFalse(value_is_str(read(INT)))

    def test_str(self):
        self.assertTrue(value_is_str(read(STR)))

    def test_var(self):
        self.assertFalse(value_is_str(read(VAR)))

    def test_list(self):
        self.assertFalse(value_is_str(read(LIST)))


class Test_evaluate(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(evaluate(read([])), read([]))

    def test_int(self):
        self.assertEqual(evaluate(read(INT)), read(INT))

    def test_var(self):
        variables[VAR] = evaluate(read(INT))
        self.assertEqual(evaluate(read(VAR)), read(INT))
        del variables[VAR]

    def test_str(self):
        self.assertEqual(evaluate(read(STR)), read(STR))


if __name__ == "__main__":
    unittest.main()
    testmod("prose2")
