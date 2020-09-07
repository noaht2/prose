#!/usr/bin/env python3

from sys import argv, stdin, stdout
from json import loads

from __init__ import main 


if len(argv) == 1:
    program = stdin.read()
elif len(argv) == 2:
    with open(argv[1]) as f:
        program = f.read()

print(main(loads(program)))
