#!/usr/bin/env python3

import unittest
from doctest import testmod
import __init__ as prose

INT = "1"
STR = '"hi"'
VAR = "x"
LIST = (prose.read(()), INT, STR, VAR)


class Test_entry_is_int(unittest.TestCase):
    def test_empty_list(self):
        self.assertFalse(prose.entry_is_int(()))
        
    def test_int(self):
        self.assertTrue(prose.entry_is_int(INT))

    def test_str(self):
        self.assertFalse(prose.entry_is_int(STR))

    def test_var(self):
        self.assertFalse(prose.entry_is_int(VAR))

    def test_list(self):
        self.assertFalse(prose.entry_is_int(LIST))


class Test_entry_is_str(unittest.TestCase):
    def test_empty_list(self):
        self.assertFalse(prose.entry_is_str(()))
        
    def test_int(self):
        self.assertFalse(prose.entry_is_str(INT))

    def test_str(self):
        self.assertTrue(prose.entry_is_str(STR))

    def test_var(self):
        self.assertFalse(prose.entry_is_str(VAR))


class Test_read(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(prose.read(()), {"underlying": (), "display": "()", "scope": {}})

    def test_int(self):
        self.assertEqual(prose.read(INT), {"underlying": int(INT), "display": INT, "scope": {}})

    def test_str(self):
        self.assertEqual(prose.read(STR), {"underlying": eval(STR), "display": STR, "scope": {}})

    def test_var(self):
        self.assertEqual(prose.read(VAR), {"underlying": VAR, "display": VAR, "scope": {}})

    def test_list(self):
        self.assertEqual(prose.read(((), "1", '"hi"', "x")),
                         {"underlying": ({'underlying': (), 'display': "()", "scope": {}},
                                         {"underlying": 1, "display": "1", "scope": {}},
                                         {"underlying": "hi",
                                          "display": '"hi"',
                                          "scope": {}},
                                         {"underlying": "x", "display": "x", "scope": {}}),
                          "display": '(() 1 "hi" x)',
                          "scope": {}})


class Test_value_is_list(unittest.TestCase):
    def test_empty_list(self):
        self.assertTrue(prose.value_is_list(prose.read(())))

    def test_int(self):
        self.assertFalse(prose.value_is_list(prose.read(INT)))

    def test_str(self):
        self.assertFalse(prose.value_is_list(prose.read(STR)))

    def test_var(self):
        self.assertFalse(prose.value_is_list(prose.read(VAR)))

    def test_list(self):
        self.assertTrue(prose.value_is_list(prose.read(LIST)))


class Test_value_is_int(unittest.TestCase):
    def test_empty_list(self):
        self.assertFalse(prose.value_is_int(prose.read(())))

    def test_int(self):
        self.assertTrue(prose.value_is_int(prose.read(INT)))

    def test_str(self):
        self.assertFalse(prose.value_is_int(prose.read(STR)))

    def test_var(self):
        self.assertFalse(prose.value_is_int(prose.read(VAR)))

    def test_list(self):
        self.assertFalse(prose.value_is_int(prose.read(LIST)))


class Test_value_is_str(unittest.TestCase):
    def test_empty_list(self):
        self.assertFalse(prose.value_is_str(prose.read(())))

    def test_int(self):
        self.assertFalse(prose.value_is_str(prose.read(INT)))

    def test_str(self):
        self.assertTrue(prose.value_is_str(prose.read(STR)))

    def test_var(self):
        self.assertFalse(prose.value_is_str(prose.read(VAR)))

    def test_list(self):
        self.assertFalse(prose.value_is_str(prose.read(LIST)))


class Test_evaluate(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(prose.evaluate(prose.read(())), prose.read(()))

    def test_int(self):
        self.assertEqual(prose.evaluate(prose.read(INT)), prose.read(INT))

    def test_var(self):
        prose.variables[VAR] = prose.evaluate(prose.read(INT))
        self.assertEqual(prose.evaluate(prose.read(VAR)), prose.read(INT))
        del prose.variables[VAR]

    def test_str(self):
        self.assertEqual(prose.evaluate(prose.read(STR)), prose.read(STR))


if __name__ == "__main__":
    unittest.main()
    testmod("prose2")
