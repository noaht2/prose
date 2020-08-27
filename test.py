#!/usr/bin/env python3

import unittest
from prose2 import *


class Test_entry_is_int(unittest.TestCase):
    def test_int(self):
        self.assertTrue(entry_is_int("1"))
        
    def test_str(self):
        self.assertFalse(entry_is_int('"hi"'))

    def test_var(self):
        self.assertFalse(entry_is_int("x"))


class Test_entry_is_str(unittest.TestCase):
    def test_int(self):
        self.assertTrue(entry_is_int("1"))
        
    def test_str(self):
        self.assertFalse(entry_is_int('"hi"'))

    def test_var(self):
        self.assertFalse(entry_is_int("x"))


class Test_read(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(read([]), {"underlying": [], "display": [], "scope": {}})

    def test_int(self):
        self.assertEqual(read("1"), {"underlying": 1, "display": "1", "scope": {}})

    def test_str(self):
        self.assertEqual(read('"hi"'), {"underlying": "hi", "display": '"hi"', "scope": {}})

    def test_var(self):
        self.assertEqual(read("x"), {"underlying": "x", "display": "x", "scope": {}})

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
        self.assertFalse(value_is_list(read("1")))

    def test_str(self):
        self.assertFalse(value_is_list(read('"hi"')))

    def test_var(self):
        self.assertFalse(value_is_list(read("x")))

    def test_list(self):
        self.assertTrue(value_is_list(read([[], "1", '"hi"', "x"])))


class Test_value_is_int(unittest.TestCase):
    def test_empty_list(self):
        self.assertFalse(value_is_int(read([])))

    def test_int(self):
        self.assertTrue(value_is_int(read("1")))

    def test_str(self):
        self.assertFalse(value_is_int(read('"hi"')))

    def test_var(self):
        self.assertFalse(value_is_int(read("x")))

    def test_list(self):
        self.assertFalse(value_is_int(read([[], "1", '"hi"', "x"])))


class Test_value_is_str(unittest.TestCase):
    def test_empty_list(self):
        self.assertFalse(value_is_str(read([])))

    def test_int(self):
        self.assertFalse(value_is_str(read("1")))

    def test_str(self):
        self.assertTrue(value_is_str(read('"hi"')))

    def test_var(self):
        self.assertFalse(value_is_str(read("x")))

    def test_list(self):
        self.assertFalse(value_is_str(read([[], "1", '"hi"', "x"])))


class Test_evaluate(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(evaluate(read([])), read([]))

    def test_int(self):
        self.assertEqual(evaluate(read("1")), read("1"))

    def test_var(self):
        variables["x"] = evaluate(read("1"))
        self.assertEqual(evaluate(read("x")), read("1"))
        del variables["x"]

    def test_str(self):
        self.assertEqual(evaluate(read('"hi"')), read('"hi"'))


if __name__ == "__main__":
    unittest.main()
