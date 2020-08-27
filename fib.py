#!/usr/bin/env python3
from proseparser import step2
from core import *
from stdlib import *
from sys import stderr

code = [
        "listm",
        [
            "1"
        ],
        "2"
]

if __name__ == "__main__":
    print(step2(code)()())
