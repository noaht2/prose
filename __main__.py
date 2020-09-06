#!/usr/bin/env python3

from sys import argv, stdin, stdout

from __init__ import read, write, evaluate 

if len(argv) == 1:
    program = stdin.read()
elif len(argv) == 2:
    with open(argv[1]) as f:
        program = f.read()
    print(write(evaluate(read(eval(program)))))
