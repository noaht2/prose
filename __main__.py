#!/usr/bin/env python3

__package__ = "prose"

from sys import argv
from . import *

with open(argv[1]) as f:
    print(proseparser.step2(eval("\n".join(f.read().split("\n")[2:])))())