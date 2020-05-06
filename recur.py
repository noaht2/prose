#!/usr/bin/env python3
from proseparser import step2
from core import *
from stdlib import *

code = [
        [
            "lambda",
            ["n"],
            "n"
        ],
        "2"
]

if __name__ == "__main__":
    print(step2(code)())