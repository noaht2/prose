#!/usr/bin/env python3
from proseparser import step2
from core import *
from stdlib import *

code = [["defun", "pass", ["x"], ["x"]], "1"]

if __name__ == "__main__":
    print(step2(code)())
